"""
Binary Tree / BST problem generator
"""

import random
from typing import List, Tuple, Any

from src.core.schemas import ProblemCreate, TestCase
from src.services.problem_gen.registry import ProblemGenerator


class BinaryTreeBSTGenerator(ProblemGenerator):
    """Generator for Binary Tree / BST problems."""
    
    def get_templates(self) -> List[str]:
        """Get available templates."""
        return ["max_depth", "invert_tree", "path_sum", "lowest_common_ancestor", "validate_bst"]
    
    def generate(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem and test cases."""
        random.seed(seed)
        template = random.choice(self.get_templates())
        return self.generate_with_template(template, seed, difficulty)
    
    def generate_with_template(self, template: str, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem with a specific template."""
        if template == "max_depth":
            return self._generate_max_depth(seed, difficulty)
        elif template == "invert_tree":
            return self._generate_invert_tree(seed, difficulty)
        elif template == "path_sum":
            return self._generate_path_sum(seed, difficulty)
        elif template == "lowest_common_ancestor":
            return self._generate_lowest_common_ancestor(seed, difficulty)
        elif template == "validate_bst":
            return self._generate_validate_bst(seed, difficulty)
        else:
            raise ValueError(f"Unknown template: {template}")
    
    def _generate_max_depth(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Maximum Depth of Binary Tree problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Binary Tree / BST",
            template_slug="max_depth",
            seed=seed,
            difficulty=difficulty,
            title="Maximum Depth of Binary Tree",
            prompt="Given the root of a binary tree, return its maximum depth.\n\nA binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.\n\nExample:\nInput: root = [3,9,20,null,null,15,7]\nOutput: 3\n\nInput: root = [1,null,2]\nOutput: 2",
            starter_code_py="def maxDepth(root):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    int maxDepth(TreeNode* root) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"root": [3, 9, 20, None, None, 15, 7]},
                expected_output=3,
                description="Main test case"
            ),
            TestCase(
                input={"root": [1, None, 2]},
                expected_output=2,
                description="Simple case"
            ),
            TestCase(
                input={"root": []},
                expected_output=0,
                description="Empty tree"
            )
        ]
        
        return problem, test_cases
    
    def _generate_invert_tree(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Invert Binary Tree problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Binary Tree / BST",
            template_slug="invert_tree",
            seed=seed,
            difficulty=difficulty,
            title="Invert Binary Tree",
            prompt="Given the root of a binary tree, invert the tree, and return its root.\n\nExample:\nInput: root = [4,2,7,1,3,6,9]\nOutput: [4,7,2,9,6,3,1]\n\nInput: root = [2,1,3]\nOutput: [2,3,1]\n\nInput: root = []\nOutput: []",
            starter_code_py="def invertTree(root):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    TreeNode* invertTree(TreeNode* root) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"root": [4, 2, 7, 1, 3, 6, 9]},
                expected_output=[4, 7, 2, 9, 6, 3, 1],
                description="Main test case"
            ),
            TestCase(
                input={"root": [2, 1, 3]},
                expected_output=[2, 3, 1],
                description="Simple case"
            ),
            TestCase(
                input={"root": []},
                expected_output=[],
                description="Empty tree"
            )
        ]
        
        return problem, test_cases
    
    def _generate_path_sum(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Path Sum problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Binary Tree / BST",
            template_slug="path_sum",
            seed=seed,
            difficulty=difficulty,
            title="Path Sum",
            prompt="Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.\n\nA leaf is a node with no children.\n\nExample:\nInput: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22\nOutput: true\nExplanation: The root-to-leaf path with the target sum is shown.\n\nInput: root = [1,2,3], targetSum = 5\nOutput: false\nExplanation: There two root-to-leaf paths in the tree:\n(1 --> 2): The sum is 3.\n(1 --> 3): The sum is 4.\nThere is no root-to-leaf path with sum = 5.",
            starter_code_py="def hasPathSum(root, targetSum):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    bool hasPathSum(TreeNode* root, int targetSum) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"root": [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], "targetSum": 22},
                expected_output=True,
                description="Path exists"
            ),
            TestCase(
                input={"root": [1, 2, 3], "targetSum": 5},
                expected_output=False,
                description="No path exists"
            ),
            TestCase(
                input={"root": [], "targetSum": 0},
                expected_output=False,
                description="Empty tree"
            )
        ]
        
        return problem, test_cases
    
    def _generate_lowest_common_ancestor(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Lowest Common Ancestor of a Binary Search Tree problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Binary Tree / BST",
            template_slug="lowest_common_ancestor",
            seed=seed,
            difficulty=difficulty,
            title="Lowest Common Ancestor of a Binary Search Tree",
            prompt="Given a binary search tree (BST), find the lowest common ancestor (LCA) of two given nodes in the BST.\n\nAccording to the definition of LCA on Wikipedia: \"The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).\"\n\nExample:\nInput: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8\nOutput: 6\nExplanation: The LCA of nodes 2 and 8 is 6.\n\nInput: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4\nOutput: 2\nExplanation: The LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself according to the LCA definition.",
            starter_code_py="def lowestCommonAncestor(root, p, q):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 8},
                expected_output=6,
                description="LCA in different subtrees"
            ),
            TestCase(
                input={"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 4},
                expected_output=2,
                description="LCA is one of the nodes"
            ),
            TestCase(
                input={"root": [2, 1], "p": 2, "q": 1},
                expected_output=2,
                description="Simple case"
            )
        ]
        
        return problem, test_cases
    
    def _generate_validate_bst(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate Validate Binary Search Tree problem."""
        random.seed(seed)
        
        problem = ProblemCreate(
            category="Binary Tree / BST",
            template_slug="validate_bst",
            seed=seed,
            difficulty=difficulty,
            title="Validate Binary Search Tree",
            prompt="Given the root of a binary tree, determine if it is a valid binary search tree (BST).\n\nA valid BST is defined as follows:\n\nThe left subtree of a node contains only nodes with keys less than the node's key.\nThe right subtree of a node contains only nodes with keys greater than the node's key.\nBoth the left and right subtrees must also be binary search trees.\n\nExample:\nInput: root = [2,1,3]\nOutput: true\n\nInput: root = [5,1,4,null,null,3,6]\nOutput: false\nExplanation: The root node's value is 5 but its right child's value is 4.",
            starter_code_py="def isValidBST(root):\n    # Your code here\n    pass",
            starter_code_cpp="class Solution {\npublic:\n    bool isValidBST(TreeNode* root) {\n        // Your code here\n    }\n};",
            tests_public_count=3
        )
        
        test_cases = [
            TestCase(
                input={"root": [2, 1, 3]},
                expected_output=True,
                description="Valid BST"
            ),
            TestCase(
                input={"root": [5, 1, 4, None, None, 3, 6]},
                expected_output=False,
                description="Invalid BST"
            ),
            TestCase(
                input={"root": [1, 1]},
                expected_output=False,
                description="Duplicate values"
            )
        ]
        
        return problem, test_cases