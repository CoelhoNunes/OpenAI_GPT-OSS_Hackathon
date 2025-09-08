"""
Problem generator registry and factory
"""

import random
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple

from src.core.schemas import ProblemCreate, TestCase


class ProblemGenerator(ABC):
    """Abstract base class for problem generators."""
    
    @abstractmethod
    def generate(self, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem and test cases."""
        pass
    
    @abstractmethod
    def generate_with_template(self, template: str, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem with a specific template."""
        pass
    
    @abstractmethod
    def get_templates(self) -> List[str]:
        """Get available templates for this category."""
        pass


class ProblemRegistry:
    """Registry for problem generators."""
    
    def __init__(self):
        self._generators: Dict[str, ProblemGenerator] = {}
    
    def register(self, category: str, generator: ProblemGenerator) -> None:
        """Register a problem generator for a category."""
        self._generators[category] = generator
    
    def get_generator(self, category: str) -> ProblemGenerator:
        """Get generator for a category."""
        if category not in self._generators:
            raise ValueError(f"No generator registered for category: {category}")
        return self._generators[category]
    
    def get_categories(self) -> List[str]:
        """Get all registered categories."""
        return list(self._generators.keys())
    
    def get_templates(self, category: str) -> List[str]:
        """Get templates for a category."""
        generator = self.get_generator(category)
        return generator.get_templates()
    
    def generate_problem(self, category: str, template: str, seed: int, difficulty: str) -> Tuple[ProblemCreate, List[TestCase]]:
        """Generate a problem using the specified template."""
        generator = self.get_generator(category)
        templates = generator.get_templates()
        
        if template not in templates:
            raise ValueError(f"Template '{template}' not found in category '{category}'")
        
        # Set random seed for deterministic generation
        random.seed(seed)
        
        # Generate problem with specific template
        return generator.generate_with_template(template, seed, difficulty)


# Global registry instance
registry = ProblemRegistry()
