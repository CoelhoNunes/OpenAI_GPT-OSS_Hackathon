"""
Judge service - handles code execution and testing
"""

import json
import httpx
from typing import Dict, Any, List

import structlog

from src.core.config import settings

logger = structlog.get_logger()


class JudgeService:
    """Service for judging code submissions."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def judge_submission(
        self,
        problem: Any,  # Problem model
        code: str,
        language: str,
        is_test_run: bool = False
    ) -> Dict[str, Any]:
        """Judge a code submission."""
        
        # Generate test cases for the problem
        from src.services.problem_gen.registry import registry
        
        # Generate test cases using the existing problem's template and seed
        _, test_cases = registry.generate_problem(
            problem.category,
            problem.template_slug,
            problem.seed,
            problem.difficulty
        )
        
        # Filter test cases based on run type
        if is_test_run:
            # For test runs, only use public test cases
            filtered_test_cases = [tc for tc in test_cases if tc.is_public]
        else:
            # For submissions, use all test cases (public + private)
            filtered_test_cases = test_cases
        
        # Prepare submission data
        submission_data = {
            "language": language,
            "code": code,
            "test_cases": [
                {
                    "input": tc.input,
                    "expected_output": tc.expected_output,
                    "description": tc.description,
                    "is_public": tc.is_public
                }
                for tc in filtered_test_cases
            ]
        }
        
        try:
            # Send to runner service
            response = await self.client.post(
                f"{settings.RUNNER_URL}/execute",
                json=submission_data
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Process results
            passed = sum(1 for tc in result.get("test_results", []) if tc.get("status") == "PASS")
            total = len(result.get("test_results", []))
            
            # Use the verdict from the runner service if it's already set
            runner_verdict = result.get("verdict")
            if runner_verdict in ["COMPILE_ERROR", "TIMEOUT", "RUNTIME_ERROR"]:
                verdict = runner_verdict
            elif passed == total and total > 0:
                verdict = "ACCEPTED"  # Accepted
            elif result.get("timeout", False):
                verdict = "TIMEOUT"  # Time Limit Exceeded
            elif result.get("memory_exceeded", False):
                verdict = "RUNTIME_ERROR"  # Runtime Error (memory)
            elif result.get("compilation_error", False):
                verdict = "COMPILE_ERROR"  # Compilation Error
            else:
                verdict = "WRONG_ANSWER"  # Wrong Answer
            
            return {
                "verdict": verdict,
                "passed": passed,
                "total": total,
                "runtime_ms": result.get("total_runtime_ms"),
                "memory_kb": result.get("peak_memory_kb"),
                "details": {
                    "test_results": result.get("test_results", []),
                    "compilation_output": result.get("compilation_output"),
                    "runtime_output": result.get("runtime_output")
                }
            }
            
        except httpx.TimeoutException:
            logger.error("Runner service timeout")
            return {
                "verdict": "TIMEOUT",
                "passed": 0,
                "total": len(filtered_test_cases),
                "details": {"error": "Execution timeout"}
            }
        except httpx.HTTPStatusError as e:
            logger.error("Runner service error", status_code=e.response.status_code)
            return {
                "verdict": "RUNTIME_ERROR",
                "passed": 0,
                "total": len(filtered_test_cases),
                "details": {"error": f"Runner service error: {e.response.status_code}"}
            }
        except Exception as e:
            logger.error("Judge service error", error=str(e))
            return {
                "verdict": "RUNTIME_ERROR",
                "passed": 0,
                "total": len(filtered_test_cases),
                "details": {"error": str(e)}
            }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
