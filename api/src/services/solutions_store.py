"""
Solutions store - manages reference solutions
"""

import os
import json
from typing import Dict, Any
from pathlib import Path

import structlog

logger = structlog.get_logger()


class SolutionsStore:
    """Store for reference solutions."""
    
    def __init__(self):
        self.solutions_dir = Path("src/data/solutions")
        self.solutions_dir.mkdir(parents=True, exist_ok=True)
    
    async def get_solution(self, template_slug: str, seed: int) -> Dict[str, Any]:
        """Get solution for a specific template and seed."""
        
        solution_file = self.solutions_dir / f"{template_slug}_{seed}.json"
        
        if not solution_file.exists():
            # Try to generate solution if it doesn't exist
            await self._generate_solution(template_slug, seed)
        
        with open(solution_file, 'r') as f:
            return json.load(f)
    
    async def _generate_solution(self, template_slug: str, seed: int) -> None:
        """Generate a solution for a template and seed."""
        
        # This would typically call the CUDA acceleration service
        # or use a reference implementation
        # For now, we'll create placeholder solutions
        
        solution_data = {
            "python_solution": self._get_python_solution(template_slug),
            "cpp_solution": self._get_cpp_solution(template_slug),
            "explanation": self._get_explanation(template_slug),
            "complexity": self._get_complexity(template_slug)
        }
        
        solution_file = self.solutions_dir / f"{template_slug}_{seed}.json"
        with open(solution_file, 'w') as f:
            json.dump(solution_data, f, indent=2)
    
    def _get_python_solution(self, template_slug: str) -> str:
        """Get Python solution for template."""
        solutions = {
            "two_sum": '''def twoSum(nums, target):
    hashmap = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hashmap:
            return [hashmap[complement], i]
        hashmap[num] = i
    return []''',
            "reverse_list": '''def reverseList(head):
    prev = None
    current = head
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    return prev''',
            "contains_duplicate": '''def containsDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False'''
        }
        return solutions.get(template_slug, "# Solution not available")
    
    def _get_cpp_solution(self, template_slug: str) -> str:
        """Get C++ solution for template."""
        solutions = {
            "two_sum": '''class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> hashmap;
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            if (hashmap.find(complement) != hashmap.end()) {
                return {hashmap[complement], i};
            }
            hashmap[nums[i]] = i;
        }
        return {};
    }
};''',
            "reverse_list": '''class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* current = head;
        while (current) {
            ListNode* next = current->next;
            current->next = prev;
            prev = current;
            current = next;
        }
        return prev;
    }
};''',
            "contains_duplicate": '''class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> seen;
        for (int num : nums) {
            if (seen.find(num) != seen.end()) {
                return true;
            }
            seen.insert(num);
        }
        return false;
    }
};'''
        }
        return solutions.get(template_slug, "// Solution not available")
    
    def _get_explanation(self, template_slug: str) -> str:
        """Get explanation for template."""
        explanations = {
            "two_sum": "Use a hash map to store each number and its index. For each number, check if its complement (target - number) exists in the map. If found, return the indices.",
            "reverse_list": "Use three pointers: prev, current, and next. Iterate through the list, reversing the next pointer of each node to point to the previous node.",
            "contains_duplicate": "Use a hash set to track seen numbers. For each number, check if it's already in the set. If found, return true. Otherwise, add it to the set."
        }
        return explanations.get(template_slug, "Explanation not available")
    
    def _get_complexity(self, template_slug: str) -> str:
        """Get complexity analysis for template."""
        complexities = {
            "two_sum": "Time: O(n), Space: O(n) - Single pass through array with hash map storage",
            "reverse_list": "Time: O(n), Space: O(1) - Single pass through list with constant extra space",
            "contains_duplicate": "Time: O(n), Space: O(n) - Single pass through array with hash set storage"
        }
        return complexities.get(template_slug, "Complexity analysis not available")
