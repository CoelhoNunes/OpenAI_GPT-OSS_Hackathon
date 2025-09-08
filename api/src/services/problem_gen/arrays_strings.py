"""
Arrays & Strings problem generator
"""

import random
from typing import List, Tuple, Any, Dict

from src.core.schemas import ProblemCreate, TestCase
from src.services.problem_gen.registry import ProblemGenerator


class ArraysStringsGenerator(ProblemGenerator):
    """Generator for Arrays & Strings problems."""
    
    def get_templates(self) -> List[str]:
        """Get available templates."""
        return ["two_sum", "rotate_array", "group_anagrams", "longest_substring", "product_except_self"]
    
    def generate(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem and test cases."""
        random.seed(seed)
        template = random.choice(self.get_templates())
        return self.generate_with_template(template, seed, difficulty)
    
    def generate_with_template(self, template: str, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem with a specific template."""
        if template == "two_sum":
            return self._generate_two_sum(seed, difficulty)
        elif template == "rotate_array":
            return self._generate_rotate_array(seed, difficulty)
        elif template == "group_anagrams":
            return self._generate_group_anagrams(seed, difficulty)
        elif template == "longest_substring":
            return self._generate_longest_substring(seed, difficulty)
        elif template == "product_except_self":
            return self._generate_product_except_self(seed, difficulty)
        else:
            raise ValueError(f"Unknown template: {template}")
    
    def _generate_two_sum(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Two Sum problem."""
        random.seed(seed)
        
        # Generate array and target
        n = random.randint(8, 15) if difficulty == "Easy" else random.randint(15, 25)
        nums = [random.randint(-20, 20) for _ in range(n)]
        
        # Ensure there's a valid solution
        i, j = random.sample(range(n), 2)
        target = nums[i] + nums[j]
        
        problem = ProblemCreate(
            category="Arrays & Strings",
            template_slug="two_sum",
            seed=seed,
            difficulty=difficulty,
            title="Two Sum",
            prompt=f"Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].",
            starter_code_py="def twoSum(nums, target):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            # Public test cases (visible to user)
            TestCase(
                input={"nums": [3, 2, 4], "target": 6},
                expected_output=[1, 2],
                description="Simple case",
                is_public=True
            ),
            TestCase(
                input={"nums": [3, 3], "target": 6},
                expected_output=[0, 1],
                description="Duplicate elements",
                is_public=True
            ),
            TestCase(
                input={"nums": [2, 7, 11, 15], "target": 9},
                expected_output=[0, 1],
                description="Example case",
                is_public=True
            ),
            # Private test cases (hidden from user)
            TestCase(
                input={"nums": nums, "target": target},
                expected_output=[i, j] if i < j else [j, i],
                description="Generated test case",
                is_public=False
            ),
            TestCase(
                input={"nums": [1, 2, 3, 4, 5], "target": 8},
                expected_output=[2, 4],
                description="Edge case with larger array",
                is_public=False
            ),
            TestCase(
                input={"nums": [-1, -2, -3, -4, -5], "target": -8},
                expected_output=[2, 4],
                description="Negative numbers",
                is_public=False
            )
        ]
        
        return problem, test_cases
    
    def _generate_rotate_array(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Rotate Array problem."""
        random.seed(seed)
        
        n = random.randint(5, 10) if difficulty == "Easy" else random.randint(10, 20)
        nums = [random.randint(1, 100) for _ in range(n)]
        k = random.randint(1, n)
        
        problem = ProblemCreate(
            category="Arrays & Strings",
            template_slug="rotate_array",
            seed=seed,
            difficulty=difficulty,
            title="Rotate Array",
            prompt=f"Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.\n\nExample:\nInput: nums = [1,2,3,4,5,6,7], k = 3\nOutput: [5,6,7,1,2,3,4]\nExplanation:\nrotate 1 steps to the right: [7,1,2,3,4,5,6]\nrotate 2 steps to the right: [6,7,1,2,3,4,5]\nrotate 3 steps to the right: [5,6,7,1,2,3,4]",
            starter_code_py="def rotate(nums, k):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    void rotate(vector<int>& nums, int k) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        # Calculate expected result
        expected = nums[-k:] + nums[:-k]
        
        test_cases = [
            TestCase(
                input={"nums": nums.copy(), "k": k},
                expected_output=expected,
                description="Main test case"
            ),
            TestCase(
                input={"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3},
                expected_output=[5, 6, 7, 1, 2, 3, 4],
                description="Example case"
            ),
            TestCase(
                input={"nums": [-1, -100, 3, 99], "k": 2},
                expected_output=[3, 99, -1, -100],
                description="Negative numbers"
            )
        ]
        
        return problem, test_cases
    
    def _generate_group_anagrams(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Group Anagrams problem."""
        random.seed(seed)
        
        words = ["eat", "tea", "tan", "ate", "nat", "bat"]
        
        problem = ProblemCreate(
            category="Arrays & Strings",
            template_slug="group_anagrams",
            seed=seed,
            difficulty=difficulty,
            title="Group Anagrams",
            prompt="Given an array of strings strs, group the anagrams together. You can return the answer in any order.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.\n\nExample:\nInput: strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]\nOutput: [[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]",
            starter_code_py="def groupAnagrams(strs):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    vector<vector<string>> groupAnagrams(vector<string>& strs) {\n        // Your code here\n    }\n};",
            tests_public_count=2
        )
        
        test_cases = [
            TestCase(
                input={"strs": words},
                expected_output=[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
                description="Main test case"
            ),
            TestCase(
                input={"strs": [""]},
                expected_output=[[""]],
                description="Empty string"
            )
        ]
        
        return problem, test_cases
    
    def _generate_longest_substring(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Longest Substring Without Repeating Characters problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Arrays & Strings",
            template_slug="longest_substring",
            seed=seed,
            difficulty=difficulty,
            title="Longest Substring Without Repeating Characters",
            prompt="Given a string s, find the length of the longest substring without repeating characters.\n\nExample:\nInput: s = \"abcabcbb\"\nOutput: 3\nExplanation: The answer is \"abc\", with the length of 3.",
            starter_code_py="def lengthOfLongestSubstring(s):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    int lengthOfLongestSubstring(string s) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"s": "abcabcbb"},
                expected_output=3,
                description="Main test case"
            ),
            TestCase(
                input={"s": "bbbbb"},
                expected_output=1,
                description="All same characters"
            ),
            TestCase(
                input={"s": "pwwkew"},
                expected_output=3,
                description="Mixed case"
            )
        ]
        
        return problem, test_cases
    
    def _generate_product_except_self(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Product of Array Except Self problem."""
        random.seed(seed)
        
        nums = [1, 2, 3, 4]
        
        problem = ProblemCreate(
            category="Arrays & Strings",
            template_slug="product_except_self",
            seed=seed,
            difficulty=difficulty,
            title="Product of Array Except Self",
            prompt="Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].\n\nThe product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.\n\nYou must write an algorithm that runs in O(n) time and without using the division operator.\n\nExample:\nInput: nums = [1,2,3,4]\nOutput: [24,12,8,6]",
            starter_code_py="def productExceptSelf(nums):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    vector<int> productExceptSelf(vector<int>& nums) {\n        // Your code here\n    }\n};",
            tests_public_count=2
        )
        
        test_cases = [
            TestCase(
                input={"nums": nums},
                expected_output=[24, 12, 8, 6],
                description="Main test case"
            ),
            TestCase(
                input={"nums": [-1, 1, 0, -3, 3]},
                expected_output=[0, 0, 9, 0, 0],
                description="With zeros"
            )
        ]
        
        return problem, test_cases
