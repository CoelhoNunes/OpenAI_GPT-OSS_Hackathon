"""
Tests for problem generation
"""

import pytest
from src.services.problem_gen.registry import registry
from src.services.problem_gen.arrays_strings import ArraysStringsGenerator


class TestProblemGeneration:
    """Test problem generation functionality."""
    
    def test_registry_categories(self):
        """Test that all categories are registered."""
        categories = registry.get_categories()
        expected_categories = [
            "Arrays & Strings",
            "Linked List", 
            "Stack & Queue",
            "Hash Map / Hash Set",
            "Binary Tree / BST"
        ]
        
        for category in expected_categories:
            assert category in categories
    
    def test_arrays_strings_templates(self):
        """Test Arrays & Strings templates."""
        templates = registry.get_templates("Arrays & Strings")
        expected_templates = [
            "two_sum", "rotate_array", "group_anagrams", 
            "longest_substring", "product_except_self"
        ]
        
        for template in expected_templates:
            assert template in templates
    
    def test_deterministic_generation(self):
        """Test that same seed produces same problem."""
        problem1, _ = registry.generate_problem(
            "Arrays & Strings", "two_sum", 12345, "Easy"
        )
        problem2, _ = registry.generate_problem(
            "Arrays & Strings", "two_sum", 12345, "Easy"
        )
        
        assert problem1.seed == problem2.seed
        assert problem1.title == problem2.title
        assert problem1.prompt == problem2.prompt
    
    def test_different_seeds_produce_different_problems(self):
        """Test that different seeds produce different problems."""
        problem1, _ = registry.generate_problem(
            "Arrays & Strings", "two_sum", 12345, "Easy"
        )
        problem2, _ = registry.generate_problem(
            "Arrays & Strings", "two_sum", 67890, "Easy"
        )
        
        assert problem1.seed != problem2.seed
    
    def test_arrays_strings_generator(self):
        """Test ArraysStringsGenerator directly."""
        generator = ArraysStringsGenerator()
        templates = generator.get_templates()
        
        assert len(templates) >= 3
        assert "two_sum" in templates
        
        # Test generation
        problem, test_cases = generator.generate(12345, "Easy")
        
        assert problem.category == "Arrays & Strings"
        assert problem.difficulty == "Easy"
        assert problem.seed == 12345
        assert len(test_cases) > 0
        
        # Test that test cases have required fields
        for test_case in test_cases:
            assert test_case.input is not None
            assert test_case.expected_output is not None
            assert test_case.description is not None
    
    def test_invalid_category(self):
        """Test that invalid category raises error."""
        with pytest.raises(ValueError):
            registry.get_generator("Invalid Category")
    
    def test_invalid_template(self):
        """Test that invalid template raises error."""
        with pytest.raises(ValueError):
            registry.generate_problem(
                "Arrays & Strings", "invalid_template", 12345, "Easy"
            )
