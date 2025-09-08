"""
Problem generator utilities
"""

import random
from typing import List, Any

from src.core.schemas import TestCase


def generate_test_cases(template_slug: str, seed: int, difficulty: str) -> List[TestCase]:
    """Generate test cases for a template."""
    # This is a placeholder - actual test case generation would be more sophisticated
    random.seed(seed)
    
    # Basic test cases based on template
    if template_slug == "two_sum":
        return [
            TestCase(
                input={"nums": [2, 7, 11, 15], "target": 9},
                expected_output=[0, 1],
                description="Basic example"
            ),
            TestCase(
                input={"nums": [3, 2, 4], "target": 6},
                expected_output=[1, 2],
                description="Different indices"
            ),
            TestCase(
                input={"nums": [3, 3], "target": 6},
                expected_output=[0, 1],
                description="Duplicate elements"
            )
        ]
    elif template_slug == "reverse_list":
        return [
            TestCase(
                input={"head": [1, 2, 3, 4, 5]},
                expected_output=[5, 4, 3, 2, 1],
                description="Basic reversal"
            ),
            TestCase(
                input={"head": [1, 2]},
                expected_output=[2, 1],
                description="Two nodes"
            ),
            TestCase(
                input={"head": []},
                expected_output=[],
                description="Empty list"
            )
        ]
    else:
        # Generic test cases
        return [
            TestCase(
                input={"input": "test"},
                expected_output="expected",
                description="Test case 1"
            )
        ]


def validate_test_case(test_case: TestCase) -> bool:
    """Validate a test case."""
    return (
        test_case.input is not None and
        test_case.expected_output is not None and
        test_case.description is not None
    )


def generate_random_array(size: int, min_val: int = -100, max_val: int = 100) -> List[int]:
    """Generate a random array of integers."""
    return [random.randint(min_val, max_val) for _ in range(size)]


def generate_random_string(length: int, charset: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    """Generate a random string."""
    return ''.join(random.choice(charset) for _ in range(length))


def generate_random_tree(size: int) -> List[Any]:
    """Generate a random binary tree representation."""
    if size == 0:
        return []
    
    tree = [random.randint(1, 100)]
    for i in range(1, size):
        if random.random() < 0.7:  # 70% chance of non-null
            tree.append(random.randint(1, 100))
        else:
            tree.append(None)
    
    return tree
