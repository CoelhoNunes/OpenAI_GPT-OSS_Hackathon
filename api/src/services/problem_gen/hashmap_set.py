"""
Hash Map / Hash Set problem generator
"""

import random
from typing import List, Tuple, Any

from src.core.schemas import ProblemCreate, TestCase
from src.services.problem_gen.registry import ProblemGenerator


class HashMapSetGenerator(ProblemGenerator):
    """Generator for Hash Map / Hash Set problems."""
    
    def get_templates(self) -> List[str]:
        """Get available templates."""
        return ["contains_duplicate", "single_number", "intersection", "happy_number", "isomorphic_strings"]
    
    def generate(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem and test cases."""
        random.seed(seed)
        template = random.choice(self.get_templates())
        return self.generate_with_template(template, seed, difficulty)
    
    def generate_with_template(self, template: str, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem with a specific template."""
        if template == "contains_duplicate":
            return self._generate_contains_duplicate(seed, difficulty)
        elif template == "single_number":
            return self._generate_single_number(seed, difficulty)
        elif template == "intersection":
            return self._generate_intersection(seed, difficulty)
        elif template == "happy_number":
            return self._generate_happy_number(seed, difficulty)
        elif template == "isomorphic_strings":
            return self._generate_isomorphic_strings(seed, difficulty)
        else:
            raise ValueError(f"Unknown template: {template}")
    
    def _generate_contains_duplicate(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Contains Duplicate problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Hash Map / Hash Set",
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
                description="Contains duplicate"
            ),
            TestCase(
                input={"nums": [1, 2, 3, 4]},
                expected_output=False,
                description="No duplicates"
            ),
            TestCase(
                input={"nums": [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]},
                expected_output=True,
                description="Multiple duplicates"
            )
        ]
        
        return problem, test_cases
    
    def _generate_single_number(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Single Number problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Hash Map / Hash Set",
            template_slug="single_number",
            seed=seed,
            difficulty=difficulty,
            title="Single Number",
            prompt="Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.\n\nYou must implement a solution with a linear runtime complexity and use only constant extra space.\n\nExample:\nInput: nums = [2,2,1]\nOutput: 1\n\nInput: nums = [4,1,2,1,2]\nOutput: 4\n\nInput: nums = [1]\nOutput: 1",
            starter_code_py="def singleNumber(nums):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    int singleNumber(vector<int>& nums) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"nums": [2, 2, 1]},
                expected_output=1,
                description="Simple case"
            ),
            TestCase(
                input={"nums": [4, 1, 2, 1, 2]},
                expected_output=4,
                description="Single number at end"
            ),
            TestCase(
                input={"nums": [1]},
                expected_output=1,
                description="Single element"
            )
        ]
        
        return problem, test_cases
    
    def _generate_intersection(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Intersection of Two Arrays problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Hash Map / Hash Set",
            template_slug="intersection",
            seed=seed,
            difficulty=difficulty,
            title="Intersection of Two Arrays",
            prompt="Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must be unique and you may return the result in any order.\n\nExample:\nInput: nums1 = [1,2,2,1], nums2 = [2,2]\nOutput: [2]\n\nInput: nums1 = [4,9,5], nums2 = [9,4,9,8,4]\nOutput: [9,4] or [4,9]",
            starter_code_py="def intersection(nums1, nums2):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"nums1": [1, 2, 2, 1], "nums2": [2, 2]},
                expected_output=[2],
                description="Simple intersection"
            ),
            TestCase(
                input={"nums1": [4, 9, 5], "nums2": [9, 4, 9, 8, 4]},
                expected_output=[9, 4],
                description="Multiple intersections"
            ),
            TestCase(
                input={"nums1": [1, 2, 3], "nums2": [4, 5, 6]},
                expected_output=[],
                description="No intersection"
            )
        ]
        
        return problem, test_cases
    
    def _generate_happy_number(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Happy Number problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Hash Map / Hash Set",
            template_slug="happy_number",
            seed=seed,
            difficulty=difficulty,
            title="Happy Number",
            prompt="Write an algorithm to determine if a number n is happy.\n\nA happy number is a number defined by the following process:\n\nStarting with any positive integer, replace the number by the sum of the squares of its digits.\nRepeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.\nThose numbers for which this process ends in 1 are happy.\n\nReturn true if n is a happy number, and false if not.\n\nExample:\nInput: n = 19\nOutput: true\nExplanation:\n1² + 9² = 82\n8² + 2² = 68\n6² + 8² = 100\n1² + 0² + 0² = 1",
            starter_code_py="def isHappy(n):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    bool isHappy(int n) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"n": 19},
                expected_output=True,
                description="Happy number"
            ),
            TestCase(
                input={"n": 2},
                expected_output=False,
                description="Not happy number"
            ),
            TestCase(
                input={"n": 1},
                expected_output=True,
                description="Single digit happy"
            )
        ]
        
        return problem, test_cases
    
    def _generate_isomorphic_strings(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Isomorphic Strings problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Hash Map / Hash Set",
            template_slug="isomorphic_strings",
            seed=seed,
            difficulty=difficulty,
            title="Isomorphic Strings",
            prompt="Given two strings s and t, determine if they are isomorphic.\n\nTwo strings s and t are isomorphic if the characters in s can be replaced to get t.\n\nAll occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character, but a character may map to itself.\n\nExample:\nInput: s = \"egg\", t = \"add\"\nOutput: true\n\nInput: s = \"foo\", t = \"bar\"\nOutput: false\n\nInput: s = \"paper\", t = \"title\"\nOutput: true",
            starter_code_py="def isIsomorphic(s, t):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    bool isIsomorphic(string s, string t) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"s": "egg", "t": "add"},
                expected_output=True,
                description="Isomorphic strings"
            ),
            TestCase(
                input={"s": "foo", "t": "bar"},
                expected_output=False,
                description="Not isomorphic"
            ),
            TestCase(
                input={"s": "paper", "t": "title"},
                expected_output=True,
                description="Complex isomorphic"
            )
        ]
        
        return problem, test_cases