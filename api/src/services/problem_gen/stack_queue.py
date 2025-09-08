"""
Stack & Queue problem generator
"""

import random
from typing import List, Tuple, Any

from src.core.schemas import ProblemCreate, TestCase
from src.services.problem_gen.registry import ProblemGenerator


class StackQueueGenerator(ProblemGenerator):
    """Generator for Stack & Queue problems."""
    
    def get_templates(self) -> List[str]:
        """Get available templates."""
        return ["contains_duplicate", "min_stack", "daily_temperatures", "largest_rectangle", "sliding_window_max"]
    
    def generate(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem and test cases."""
        random.seed(seed)
        template = random.choice(self.get_templates())
        return self.generate_with_template(template, seed, difficulty)
    
    def generate_with_template(self, template: str, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem with a specific template."""
        if template == "contains_duplicate":
            return self._generate_contains_duplicate(seed, difficulty)
        elif template == "min_stack":
            return self._generate_min_stack(seed, difficulty)
        elif template == "daily_temperatures":
            return self._generate_daily_temperatures(seed, difficulty)
        elif template == "largest_rectangle":
            return self._generate_largest_rectangle(seed, difficulty)
        elif template == "sliding_window_max":
            return self._generate_sliding_window_max(seed, difficulty)
        else:
            raise ValueError(f"Unknown template: {template}")
    
    def _generate_contains_duplicate(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Contains Duplicate problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Stack & Queue",
            template_slug="contains_duplicate",
            seed=seed,
            difficulty=difficulty,
            title="Contains Duplicate",
            prompt="Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.\n\nExample:\nInput: nums = [1,2,3,1]\nOutput: true\n\nInput: nums = [1,2,3,4]\nOutput: false\n\nInput: nums = [1,1,1,3,3,4,3,2,4,2]\nOutput: true",
            starter_code_py="def containsDuplicate(nums):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    bool containsDuplicate(vector<int>& nums) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"nums": [1, 2, 3, 1]},
                expected_output=True,
                description="Contains duplicate",
                is_public=True
            ),
            TestCase(
                input={"nums": [1, 2, 3, 4]},
                expected_output=False,
                description="No duplicates",
                is_public=True
            ),
            TestCase(
                input={"nums": [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]},
                expected_output=True,
                description="Multiple duplicates",
                is_public=True
            ),
            TestCase(
                input={"nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
                expected_output=False,
                description="Large array no duplicates",
                is_public=False
            ),
            TestCase(
                input={"nums": [1, 1]},
                expected_output=True,
                description="Two identical elements",
                is_public=False
            )
        ]
        
        return problem, test_cases
    
    def _generate_min_stack(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Min Stack problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Stack & Queue",
            template_slug="min_stack",
            seed=seed,
            difficulty=difficulty,
            title="Min Stack",
            prompt="Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.\n\nImplement the MinStack class:\n- MinStack() initializes the stack object.\n- void push(int val) pushes the element val onto the stack.\n- void pop() removes the element on the top of the stack.\n- int top() gets the top element of the stack.\n- int getMin() retrieves the minimum element in the stack.\n\nYou must implement a solution with O(1) time complexity for each function.\n\nExample:\nInput\n[\"MinStack\",\"push\",\"push\",\"push\",\"getMin\",\"pop\",\"top\",\"getMin\"]\n[[],[-2],[0],[-3],[],[],[],[]]\n\nOutput\n[null,null,null,null,-3,null,0,-2]",
            starter_code_py="class MinStack:\n    def __init__(self):\n        # Your code here\n        pass\n    \n    def push(self, val: int) -> None:\n        # Your code here\n        pass\n    \n    def pop(self) -> None:\n        # Your code here\n        pass\n    \n    def top(self) -> int:\n        # Your code here\n        pass\n    \n    def getMin(self) -> int:\n        # Your code here\n        pass",
            starter_code_cpp="class MinStack {\npublic:\n    MinStack() {\n        // Your code here\n    }\n    \n    void push(int val) {\n        // Your code here\n    }\n    \n    void pop() {\n        // Your code here\n    }\n    \n    int top() {\n        // Your code here\n    }\n    \n    int getMin() {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"operations": ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"], "values": [[], [-2], [0], [-3], [], [], [], []]},
                expected_output=[None, None, None, None, -3, None, 0, -2],
                description="Main test case"
            ),
            TestCase(
                input={"operations": ["MinStack", "push", "push", "getMin", "pop", "getMin"], "values": [[], [1], [2], [], [], []]},
                expected_output=[None, None, None, 1, None, 1],
                description="Simple case"
            ),
            TestCase(
                input={"operations": ["MinStack", "push", "getMin", "push", "getMin"], "values": [[], [0], [], [1], []]},
                expected_output=[None, None, 0, None, 0],
                description="Single element"
            )
        ]
        
        return problem, test_cases
    
    def _generate_daily_temperatures(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Daily Temperatures problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Stack & Queue",
            template_slug="daily_temperatures",
            seed=seed,
            difficulty=difficulty,
            title="Daily Temperatures",
            prompt="Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.\n\nExample:\nInput: temperatures = [73,74,75,71,69,72,76,73]\nOutput: [1,1,4,2,1,1,0,0]\n\nExample:\nInput: temperatures = [30,40,50,60]\nOutput: [1,1,1,0]",
            starter_code_py="def dailyTemperatures(temperatures):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    vector<int> dailyTemperatures(vector<int>& temperatures) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"temperatures": [73, 74, 75, 71, 69, 72, 76, 73]},
                expected_output=[1, 1, 4, 2, 1, 1, 0, 0],
                description="Main test case"
            ),
            TestCase(
                input={"temperatures": [30, 40, 50, 60]},
                expected_output=[1, 1, 1, 0],
                description="Increasing temperatures"
            ),
            TestCase(
                input={"temperatures": [30, 60, 90]},
                expected_output=[1, 1, 0],
                description="Simple case"
            )
        ]
        
        return problem, test_cases
    
    def _generate_largest_rectangle(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Largest Rectangle in Histogram problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Stack & Queue",
            template_slug="largest_rectangle",
            seed=seed,
            difficulty=difficulty,
            title="Largest Rectangle in Histogram",
            prompt="Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.\n\nExample:\nInput: heights = [2,1,5,6,2,3]\nOutput: 10\nExplanation: The above is a histogram where width of each bar is 1.\nThe largest rectangle is shown in the red area, which has an area = 10 units.",
            starter_code_py="def largestRectangleArea(heights):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    int largestRectangleArea(vector<int>& heights) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"heights": [2, 1, 5, 6, 2, 3]},
                expected_output=10,
                description="Main test case"
            ),
            TestCase(
                input={"heights": [2, 4]},
                expected_output=4,
                description="Simple case"
            ),
            TestCase(
                input={"heights": [1, 1, 1, 1]},
                expected_output=4,
                description="All same height"
            )
        ]
        
        return problem, test_cases
    
    def _generate_sliding_window_max(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Sliding Window Maximum problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Stack & Queue",
            template_slug="sliding_window_max",
            seed=seed,
            difficulty=difficulty,
            title="Sliding Window Maximum",
            prompt="You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.\n\nReturn the max sliding window.\n\nExample:\nInput: nums = [1,3,-1,-3,5,3,6,7], k = 3\nOutput: [3,3,5,5,6,7]\nExplanation:\nWindow position                Max\n---------------               -----\n[1  3  -1] -3  5  3  6  7       3\n 1 [3  -1  -3] 5  3  6  7       3\n 1  3 [-1  -3  5] 3  6  7       5\n 1  3  -1 [-3  5  3] 6  7       5\n 1  3  -1  -3 [5  3  6] 7       6\n 1  3  -1  -3  5 [3  6  7]      7",
            starter_code_py="def maxSlidingWindow(nums, k):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    vector<int> maxSlidingWindow(vector<int>& nums, int k) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"nums": [1, 3, -1, -3, 5, 3, 6, 7], "k": 3},
                expected_output=[3, 3, 5, 5, 6, 7],
                description="Main test case"
            ),
            TestCase(
                input={"nums": [1], "k": 1},
                expected_output=[1],
                description="Single element"
            ),
            TestCase(
                input={"nums": [1, -1], "k": 1},
                expected_output=[1, -1],
                description="Two elements"
            )
        ]
        
        return problem, test_cases