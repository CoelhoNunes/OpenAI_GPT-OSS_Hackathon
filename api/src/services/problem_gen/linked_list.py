"""
Linked List problem generator
"""

import random
from typing import List, Tuple, Any

from src.core.schemas import ProblemCreate, TestCase
from src.services.problem_gen.registry import ProblemGenerator


class LinkedListGenerator(ProblemGenerator):
    """Generator for Linked List problems."""
    
    def get_templates(self) -> List[str]:
        """Get available templates."""
        return ["reverse_list", "merge_two_lists", "detect_cycle", "remove_nth_node", "palindrome_list"]
    
    def generate(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem and test cases."""
        random.seed(seed)
        template = random.choice(self.get_templates())
        return self.generate_with_template(template, seed, difficulty)
    
    def generate_with_template(self, template: str, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem with a specific template."""
        if template == "reverse_list":
            return self._generate_reverse_list(seed, difficulty)
        elif template == "merge_two_lists":
            return self._generate_merge_two_lists(seed, difficulty)
        elif template == "detect_cycle":
            return self._generate_detect_cycle(seed, difficulty)
        elif template == "remove_nth_node":
            return self._generate_remove_nth_node(seed, difficulty)
        elif template == "palindrome_list":
            return self._generate_palindrome_list(seed, difficulty)
        else:
            raise ValueError(f"Unknown template: {template}")
    
    def _generate_reverse_list(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Reverse Linked List problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Linked List",
            template_slug="reverse_list",
            seed=seed,
            difficulty=difficulty,
            title="Reverse Linked List",
            prompt="Given the head of a singly linked list, reverse the list and return the reversed list.\n\nExample:\nInput: head = [1,2,3,4,5]\nOutput: [5,4,3,2,1]",
            starter_code_py="def reverseList(head):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    ListNode* reverseList(ListNode* head) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            # Public test cases
            TestCase(
                input={"head": [1, 2]},
                expected_output=[2, 1],
                description="Two nodes",
                is_public=True
            ),
            TestCase(
                input={"head": []},
                expected_output=[],
                description="Empty list",
                is_public=True
            ),
            TestCase(
                input={"head": [1]},
                expected_output=[1],
                description="Single node",
                is_public=True
            ),
            # Private test cases
            TestCase(
                input={"head": [1, 2, 3, 4, 5]},
                expected_output=[5, 4, 3, 2, 1],
                description="Main test case",
                is_public=False
            ),
            TestCase(
                input={"head": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
                expected_output=[10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
                description="Longer list",
                is_public=False
            )
        ]
        
        return problem, test_cases
    
    def _generate_merge_two_lists(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Merge Two Sorted Lists problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Linked List",
            template_slug="merge_two_lists",
            seed=seed,
            difficulty=difficulty,
            title="Merge Two Sorted Lists",
            prompt="You are given the heads of two sorted linked lists list1 and list2.\n\nMerge the two lists in a one sorted list. The list should be made by splicing together the nodes of the first two lists.\n\nReturn the head of the merged linked list.\n\nExample:\nInput: list1 = [1,2,4], list2 = [1,3,4]\nOutput: [1,1,2,3,4,4]",
            starter_code_py="def mergeTwoLists(list1, list2):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"list1": [1, 2, 4], "list2": [1, 3, 4]},
                expected_output=[1, 1, 2, 3, 4, 4],
                description="Main test case"
            ),
            TestCase(
                input={"list1": [], "list2": []},
                expected_output=[],
                description="Empty lists"
            ),
            TestCase(
                input={"list1": [], "list2": [0]},
                expected_output=[0],
                description="One empty list"
            )
        ]
        
        return problem, test_cases
    
    def _generate_detect_cycle(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Linked List Cycle problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Linked List",
            template_slug="detect_cycle",
            seed=seed,
            difficulty=difficulty,
            title="Linked List Cycle",
            prompt="Given head, the head of a linked list, determine if the linked list has a cycle in it.\n\nThere is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.\n\nReturn true if there is a cycle in the linked list. Otherwise, return false.\n\nExample:\nInput: head = [3,2,0,-4], pos = 1\nOutput: true\nExplanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).",
            starter_code_py="def hasCycle(head):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    bool hasCycle(ListNode *head) {\n        // Your code here\n    }\n};",
            tests_public_count=2
        )
        
        test_cases = [
            TestCase(
                input={"head": [3, 2, 0, -4], "pos": 1},
                expected_output=True,
                description="Cycle exists"
            ),
            TestCase(
                input={"head": [1, 2], "pos": 0},
                expected_output=True,
                description="Simple cycle"
            )
        ]
        
        return problem, test_cases
    
    def _generate_remove_nth_node(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Remove Nth Node From End of List problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Linked List",
            template_slug="remove_nth_node",
            seed=seed,
            difficulty=difficulty,
            title="Remove Nth Node From End of List",
            prompt="Given the head of a linked list, remove the nth node from the end of the list and return its head.\n\nExample:\nInput: head = [1,2,3,4,5], n = 2\nOutput: [1,2,3,5]",
            starter_code_py="def removeNthFromEnd(head, n):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    ListNode* removeNthFromEnd(ListNode* head, int n) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"head": [1, 2, 3, 4, 5], "n": 2},
                expected_output=[1, 2, 3, 5],
                description="Main test case"
            ),
            TestCase(
                input={"head": [1], "n": 1},
                expected_output=[],
                description="Single node"
            ),
            TestCase(
                input={"head": [1, 2], "n": 1},
                expected_output=[1],
                description="Remove last node"
            )
        ]
        
        return problem, test_cases
    
    def _generate_palindrome_list(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Palindrome Linked List problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Linked List",
            template_slug="palindrome_list",
            seed=seed,
            difficulty=difficulty,
            title="Palindrome Linked List",
            prompt="Given the head of a singly linked list, return true if it is a palindrome or false otherwise.\n\nExample:\nInput: head = [1,2,2,1]\nOutput: true",
            starter_code_py="def isPalindrome(head):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    bool isPalindrome(ListNode* head) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"head": [1, 2, 2, 1]},
                expected_output=True,
                description="Palindrome list"
            ),
            TestCase(
                input={"head": [1, 2]},
                expected_output=False,
                description="Not palindrome"
            ),
            TestCase(
                input={"head": [1]},
                expected_output=True,
                description="Single node"
            )
        ]
        
        return problem, test_cases
