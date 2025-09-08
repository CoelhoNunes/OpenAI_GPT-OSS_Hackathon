"""
Tests for code submission
"""

import pytest
from unittest.mock import Mock, patch
from src.services.judge import JudgeService


class TestSubmission:
    """Test submission functionality."""
    
    @pytest.fixture
    def mock_problem(self):
        """Create a mock problem for testing."""
        problem = Mock()
        problem.category = "Arrays & Strings"
        problem.template_slug = "two_sum"
        problem.seed = 12345
        problem.difficulty = "Easy"
        return problem
    
    @pytest.fixture
    def judge_service(self):
        """Create a judge service instance."""
        return JudgeService()
    
    @pytest.mark.asyncio
    async def test_judge_service_initialization(self, judge_service):
        """Test that judge service initializes correctly."""
        assert judge_service is not None
        assert judge_service.client is not None
    
    @pytest.mark.asyncio
    async def test_judge_python_submission(self, judge_service, mock_problem):
        """Test judging a Python submission."""
        code = """
def twoSum(nums, target):
    hashmap = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hashmap:
            return [hashmap[complement], i]
        hashmap[num] = i
    return []
"""
        
        with patch.object(judge_service.client, 'post') as mock_post:
            # Mock successful response
            mock_response = Mock()
            mock_response.json.return_value = {
                "verdict": "AC",
                "test_results": [
                    {"status": "PASS", "input": {"nums": [2, 7, 11, 15], "target": 9}, 
                     "expected_output": [0, 1], "actual_output": [0, 1], "runtime_ms": 1},
                    {"status": "PASS", "input": {"nums": [3, 2, 4], "target": 6}, 
                     "expected_output": [1, 2], "actual_output": [1, 2], "runtime_ms": 1},
                    {"status": "PASS", "input": {"nums": [3, 3], "target": 6}, 
                     "expected_output": [0, 1], "actual_output": [0, 1], "runtime_ms": 1}
                ],
                "total_runtime_ms": 3,
                "peak_memory_kb": 1024
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            result = await judge_service.judge_submission(mock_problem, code, "python")
            
            assert result["verdict"] == "AC"
            assert result["passed"] == 3
            assert result["total"] == 3
            assert result["runtime_ms"] == 3
            assert result["memory_kb"] == 1024
    
    @pytest.mark.asyncio
    async def test_judge_wrong_answer(self, judge_service, mock_problem):
        """Test judging a wrong answer submission."""
        code = """
def twoSum(nums, target):
    return [0, 1]  # Always return wrong answer
"""
        
        with patch.object(judge_service.client, 'post') as mock_post:
            # Mock wrong answer response
            mock_response = Mock()
            mock_response.json.return_value = {
                "verdict": "WA",
                "test_results": [
                    {"status": "PASS", "input": {"nums": [2, 7, 11, 15], "target": 9}, 
                     "expected_output": [0, 1], "actual_output": [0, 1], "runtime_ms": 1},
                    {"status": "FAIL", "input": {"nums": [3, 2, 4], "target": 6}, 
                     "expected_output": [1, 2], "actual_output": [0, 1], "runtime_ms": 1},
                    {"status": "FAIL", "input": {"nums": [3, 3], "target": 6}, 
                     "expected_output": [0, 1], "actual_output": [0, 1], "runtime_ms": 1}
                ],
                "total_runtime_ms": 3,
                "peak_memory_kb": 1024
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            result = await judge_service.judge_submission(mock_problem, code, "python")
            
            assert result["verdict"] == "WA"
            assert result["passed"] == 1
            assert result["total"] == 3
    
    @pytest.mark.asyncio
    async def test_judge_timeout(self, judge_service, mock_problem):
        """Test judging a timeout submission."""
        code = """
def twoSum(nums, target):
    import time
    time.sleep(10)  # Cause timeout
    return []
"""
        
        with patch.object(judge_service.client, 'post') as mock_post:
            # Mock timeout response
            mock_response = Mock()
            mock_response.json.return_value = {
                "verdict": "TLE",
                "test_results": [],
                "timeout": True,
                "total_runtime_ms": 2000
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            result = await judge_service.judge_submission(mock_problem, code, "python")
            
            assert result["verdict"] == "TLE"
            assert result["passed"] == 0
            assert result["total"] == 0
    
    @pytest.mark.asyncio
    async def test_judge_runner_error(self, judge_service, mock_problem):
        """Test handling runner service errors."""
        code = "def twoSum(nums, target): return []"
        
        with patch.object(judge_service.client, 'post') as mock_post:
            # Mock HTTP error
            import httpx
            mock_post.side_effect = httpx.HTTPStatusError(
                "Service unavailable", 
                request=Mock(), 
                response=Mock(status_code=500)
            )
            
            result = await judge_service.judge_submission(mock_problem, code, "python")
            
            assert result["verdict"] == "RE"
            assert result["passed"] == 0
            assert "Runner service error" in result["details"]["error"]
    
    @pytest.mark.asyncio
    async def test_judge_network_timeout(self, judge_service, mock_problem):
        """Test handling network timeouts."""
        code = "def twoSum(nums, target): return []"
        
        with patch.object(judge_service.client, 'post') as mock_post:
            # Mock timeout
            import httpx
            mock_post.side_effect = httpx.TimeoutException("Request timeout")
            
            result = await judge_service.judge_submission(mock_problem, code, "python")
            
            assert result["verdict"] == "TLE"
            assert result["passed"] == 0
            assert result["total"] > 0
