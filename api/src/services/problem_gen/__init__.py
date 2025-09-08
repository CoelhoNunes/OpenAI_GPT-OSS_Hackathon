"""
Problem generation package initialization
"""

from .registry import registry, ProblemGenerator
from .arrays_strings import ArraysStringsGenerator
from .linked_list import LinkedListGenerator
from .stack_queue import StackQueueGenerator
from .hashmap_set import HashMapSetGenerator
from .binary_tree_bst import BinaryTreeBSTGenerator

# Register all generators
registry.register("Arrays & Strings", ArraysStringsGenerator())
registry.register("Linked List", LinkedListGenerator())
registry.register("Stack & Queue", StackQueueGenerator())
registry.register("Hash Map / Hash Set", HashMapSetGenerator())
registry.register("Binary Tree / BST", BinaryTreeBSTGenerator())

__all__ = [
    "registry",
    "ProblemGenerator",
    "ArraysStringsGenerator",
    "LinkedListGenerator", 
    "StackQueueGenerator",
    "HashMapSetGenerator",
    "BinaryTreeBSTGenerator"
]
