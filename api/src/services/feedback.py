"""
Feedback service - generates post-submission feedback using GPT-OSS
"""

from typing import Dict, Any, List

import httpx
import structlog

from src.core.config import settings

logger = structlog.get_logger()


class FeedbackService:
    """Service for generating feedback on submissions."""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def generate_feedback(
        self,
        code: str,
        language: str,
        problem_id: str,
        verdict: str,
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate feedback for a submission."""
        
        # Build context for GPT-OSS
        context = self._build_feedback_context(code, language, verdict, results)
        
        # Get feedback from GPT-OSS
        feedback_text = await self._call_gpt_oss(context)
        
        # Parse feedback into structured format
        return self._parse_feedback(feedback_text)
    
    def _build_feedback_context(
        self,
        code: str,
        language: str,
        verdict: str,
        results: Dict[str, Any]
    ) -> str:
        """Build context for feedback generation."""
        
        context = f"""Analyze this code submission and provide constructive feedback:

Language: {language}
Verdict: {verdict}

Code:
{code}

Test Results: {results}

Please provide:
1. Summary bullets (2-3 key points)
2. Suggested improvements (specific, actionable)
3. Complexity notes (time/space analysis)

Focus on helping the student learn and improve. Be encouraging but honest about issues."""

        return context
    
    async def _call_gpt_oss(self, context: str) -> str:
        """Call GPT-OSS for feedback generation."""
        
        system_prompt = """You are an expert programming tutor. Analyze code submissions and provide constructive, educational feedback. Focus on:
1. Code correctness and logic
2. Algorithm efficiency
3. Code style and best practices
4. Learning opportunities

Be encouraging but honest. Provide specific, actionable suggestions."""
        
        # Single path: vLLM OpenAI-compatible endpoint
        return await self._call_vllm(system_prompt, context)
    
    async def _call_vllm(self, system_prompt: str, context: str) -> str:
        """Call vLLM API."""
        try:
            response = await self.client.post(
                f"{settings.VLLM_BASE_URL}/v1/chat/completions",
                json={
                    "model": settings.GPT_OSS_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error("vLLM API call failed", error=str(e))
            return "Unable to generate feedback at this time."
    
    # Removed Ollama and HF paths to enforce single provider
    
    def _parse_feedback(self, feedback_text: str) -> Dict[str, Any]:
        """Parse feedback text into structured format."""
        
        # Simple parsing - in a real implementation, you might use more sophisticated parsing
        lines = feedback_text.split('\n')
        
        summary_bullets = []
        suggested_improvements = []
        complexity_notes = ""
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "summary" in line.lower() or "key points" in line.lower():
                current_section = "summary"
            elif "improvement" in line.lower() or "suggestion" in line.lower():
                current_section = "improvements"
            elif "complexity" in line.lower() or "time" in line.lower() or "space" in line.lower():
                current_section = "complexity"
            elif line.startswith('-') or line.startswith('•') or line.startswith('*'):
                bullet = line[1:].strip()
                if current_section == "summary":
                    summary_bullets.append(bullet)
                elif current_section == "improvements":
                    suggested_improvements.append(bullet)
            elif current_section == "complexity":
                complexity_notes += line + " "
        
        # Fallback if parsing didn't work well
        if not summary_bullets:
            summary_bullets = ["Code analysis completed"]
        if not suggested_improvements:
            suggested_improvements = ["Review the solution approach"]
        if not complexity_notes:
            complexity_notes = "Consider time and space complexity"
        
        return {
            "summary_bullets": summary_bullets[:3],  # Limit to 3 bullets
            "suggested_improvements": suggested_improvements[:5],  # Limit to 5 suggestions
            "complexity_notes": complexity_notes.strip()
        }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
