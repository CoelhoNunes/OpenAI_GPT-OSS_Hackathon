"""
GPT Coach Service - provides intelligent coding coaching using gpt-oss-20b
"""

import asyncio
import httpx
import structlog
from typing import Optional

logger = structlog.get_logger(__name__)

class GPTCoachService:
    """Service for providing intelligent coding coaching using gpt-oss-20b."""
    
    def __init__(self):
        self.vllm_url = "http://vllm:8000/v1/chat/completions"
        self.timeout = 30.0
        
    async def get_coach_response(
        self, 
        problem_context: str, 
        user_message: str, 
        code_snippet: Optional[str] = None,
        test_results: Optional[str] = None
    ) -> str:
        """Get coaching response from gpt-oss-20b."""
        
        # Build context for the LLM
        context = self._build_context(problem_context, user_message, code_snippet, test_results)
        
        try:
            # Try to get response from local vLLM (gpt-oss only)
            response = await self._call_vllm(context)
            if response:
                # Apply guardrails to ensure we don't give full solutions
                response = self._apply_guardrails(response)
                return response
        except Exception as e:
            logger.warning("vLLM call failed, using fallback", error=str(e))
        
        # Provide fallback coaching response
        return self._get_fallback_response(context)
    
    def _build_context(self, problem_context: str, user_message: str, code_snippet: Optional[str], test_results: Optional[str]) -> str:
        """Build context string for the LLM."""
        context = f"""You are helping with this coding problem: {problem_context}

User question: {user_message}"""
        
        if code_snippet:
            context += f"\n\nUser's current code:\n{code_snippet}"
        
        if test_results:
            context += f"\n\nTest results:\n{test_results}"
        
        return context
    
    async def _call_vllm(self, context: str) -> Optional[str]:
        """Call vLLM service to get coaching response."""
        system_prompt = """You are a friendly and encouraging coding tutor. Your goal is to help students learn and improve their problem-solving skills.

Guidelines:
- Be supportive and encouraging in your tone
- Provide hints and guidance, not full solutions
- Ask questions to help students think through problems
- Focus on understanding concepts and approaches
- Help students debug their code step by step
- Explain complexity analysis when relevant
- Do not use markdown formatting like **bold** or *italic*
- Keep responses conversational and engaging

When students ask questions:
- If they're stuck on approach, guide them to think about the problem step by step
- If they have errors, help them debug systematically
- If they ask about complexity, explain how to analyze it
- If they want hints, provide targeted guidance without giving away the solution

Remember: Your role is to be a helpful tutor who guides learning, not someone who gives away answers."""
        
        payload = {
            "model": "gpt-oss-20b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.vllm_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
        
        return None
    
    def _get_fallback_response(self, context: str) -> str:
        """Provide intelligent fallback coaching response when vLLM is unavailable."""
        # Extract user question from context
        if "User question:" in context:
            user_question = context.split("User question:")[-1].strip().lower()
        else:
            user_question = ""
        
        # Extract problem context
        problem_title = ""
        if "You are helping with this coding problem:" in context:
            problem_part = context.split("You are helping with this coding problem:")[1].split("User question:")[0].strip()
            # Extract just the problem title (first line before colon)
            if ":" in problem_part:
                problem_title = problem_part.split(":")[0].strip()
        
        # Provide intelligent responses based on question type, not specific problems
        if any(word in user_question for word in ["how", "solve", "approach", "strategy"]):
            if problem_title:
                return f"""Let's break down {problem_title} step by step.

Here's how I like to approach problems:

1. Understand the Problem:
   - What is the problem asking you to do?
   - What are the input and output formats?
   - What are the constraints?

2. Think of a Simple Solution First:
   - Don't worry about optimization initially
   - Focus on getting a working solution
   - Use brute force if needed

3. Consider Edge Cases:
   - Empty inputs, single elements, duplicates
   - Boundary values and special cases

4. Optimize if Needed:
   - Can you use a better data structure?
   - Can you reduce the number of operations?

What specific part of {problem_title} are you thinking about? Are you wondering about the algorithm approach or data structures to use?"""
            else:
                return """Let me help you think through this step by step.

Here's how I like to approach problems:

1. Understand the Problem:
   - What is the problem asking you to do?
   - What are the input and output formats?
   - What are the constraints?

2. Think of a Simple Solution First:
   - Don't worry about optimization initially
   - Focus on getting a working solution
   - Use brute force if needed

3. Consider Edge Cases:
   - Empty inputs, single elements, duplicates
   - Boundary values and special cases

4. Optimize if Needed:
   - Can you use a better data structure?
   - Can you reduce the number of operations?

What specific part are you thinking about? Are you wondering about the algorithm approach or data structures to use?"""

        elif any(word in user_question for word in ["complexity", "time", "space", "runtime", "big o"]):
            if problem_title:
                return f"""Let's analyze the complexity for {problem_title}:

Time Complexity: Count the number of operations your algorithm performs
- Single loop: O(n)
- Nested loops: O(n²) 
- Hash map operations: O(1) average
- Sorting: O(n log n)

Space Complexity: Count extra memory used
- Variables: O(1)
- Arrays/lists: O(n)
- Hash maps: O(n)

For {problem_title} specifically, think about:
- How many times do you need to iterate through the data?
- What data structures are you using?
- Are you doing any nested operations?

Try to identify the dominant operation in your approach. What's your current thinking about the algorithm?"""
            else:
                return """Let's analyze the complexity:

Time Complexity: Count the number of operations your algorithm performs
- Single loop: O(n)
- Nested loops: O(n²) 
- Hash map operations: O(1) average
- Sorting: O(n log n)

Space Complexity: Count extra memory used
- Variables: O(1)
- Arrays/lists: O(n)
- Hash maps: O(n)

Try to identify the dominant operation in your approach. What's your current thinking about the algorithm?"""
        
        elif any(word in user_question for word in ["debug", "error", "wrong", "fix"]):
            if problem_title:
                return f"""Let's debug {problem_title} step by step:

1. Check your logic: Walk through your algorithm with a simple example
2. Verify edge cases: Test with empty inputs, single elements, etc.
3. Check your data structures: Are you using the right one for the job?
4. Trace through your code: What happens at each step?

Common issues to look for:
- Off-by-one errors in loops
- Incorrect array/list indexing
- Missing edge case handling
- Wrong data structure choice

What specific error are you seeing with {problem_title}? Can you walk me through what your code is doing?"""
            else:
                return """Let's debug this step by step:

1. Check your logic: Walk through your algorithm with a simple example
2. Verify edge cases: Test with empty inputs, single elements, etc.
3. Check your data structures: Are you using the right one for the job?
4. Trace through your code: What happens at each step?

Common issues to look for:
- Off-by-one errors in loops
- Incorrect array/list indexing
- Missing edge case handling
- Wrong data structure choice

What specific error are you seeing? Can you walk me through what your code is doing?"""
        
        elif any(word in user_question for word in ["hint", "stuck", "help"]):
            if problem_title:
                return f"""Let's work through {problem_title} together:

1. Start with the problem statement:
   - What exactly are you trying to solve?
   - What are the inputs and expected outputs?

2. Think about the approach:
   - What data structures might be useful?
   - Are there any patterns you can recognize?
   - Can you solve a simpler version first?

3. Consider the constraints:
   - What are the time/space limits?
   - How large can the inputs be?

4. Work through an example:
   - Pick a simple test case
   - Walk through it step by step
   - What would your algorithm do?

What part of {problem_title} are you stuck on? Feel free to share what you've tried so far!"""
            else:
                return """Let's work through this together:

1. Start with the problem statement:
   - What exactly are you trying to solve?
   - What are the inputs and expected outputs?

2. Think about the approach:
   - What data structures might be useful?
   - Are there any patterns you can recognize?
   - Can you solve a simpler version first?

3. Consider the constraints:
   - What are the time/space limits?
   - How large can the inputs be?

4. Work through an example:
   - Pick a simple test case
   - Walk through it step by step
   - What would your algorithm do?

What part are you stuck on? Feel free to share what you've tried so far!"""
        
        elif any(word in user_question for word in ["data structure", "structure", "array", "hash", "map", "set", "list"]):
            return """Here are some common data structures and when to use them:

Arrays/Lists:
- Good for: Sequential access, indexing
- Operations: O(1) access, O(n) search
- Use when: You need to access elements by position

Hash Maps/Dictionaries:
- Good for: Fast lookups, counting, grouping
- Operations: O(1) average for insert/lookup
- Use when: You need to find things quickly

Sets:
- Good for: Checking membership, removing duplicates
- Operations: O(1) average for insert/lookup
- Use when: You need to check if something exists

Stacks:
- Good for: Last-in-first-out operations
- Operations: O(1) push/pop
- Use when: You need to process things in reverse order

Queues:
- Good for: First-in-first-out operations
- Operations: O(1) enqueue/dequeue
- Use when: You need to process things in order

What kind of operations do you need to perform? That will help determine the best data structure!"""
        
        elif any(word in user_question for word in ["algorithm", "pattern", "technique"]):
            return """Here are some common algorithmic patterns:

Two Pointers:
- Use when: You need to find pairs or process sorted data
- Example: Finding two numbers that sum to a target

Sliding Window:
- Use when: You need to find subarrays or substrings
- Example: Finding the longest substring with unique characters

Hash Map for Counting:
- Use when: You need to count frequencies or find duplicates
- Example: Finding the most frequent element

Stack for Matching:
- Use when: You need to match or balance things
- Example: Valid parentheses, matching brackets

Recursion:
- Use when: The problem has a recursive structure
- Example: Tree traversals, divide and conquer

What kind of problem are you working on? The pattern often depends on what you're trying to achieve!"""
        
        else:
            if problem_title:
                return f"""Let's work on {problem_title} together! 

Here's how I like to approach problems:

1. Understand the Problem:
- What is {problem_title} asking you to do?
- What are the input and output formats?
- What are the constraints?

2. Think of a Simple Solution First:
- Don't worry about optimization initially
- Focus on getting a working solution
- Use brute force if needed

3. Consider Edge Cases:
- Empty inputs
- Single elements
- Duplicates
- Boundary values

4. Optimize if Needed:
- Can you use a better data structure?
- Can you reduce the number of operations?

What specific part of {problem_title} are you working on? Are you stuck on understanding the requirements, or do you have an approach in mind? Feel free to ask about any specific challenges!"""
            else:
                return """Let's work on this coding problem together! Here's how to approach it:

Problem-Solving Steps:
1. Read and understand the problem requirements
2. Identify the input/output format  
3. Think of a simple approach first
4. Consider edge cases
5. Optimize if needed

Common Approaches:
- Use data structures (arrays, hash maps, sets)
- Apply algorithmic patterns (two pointers, sliding window)
- Consider sorting if order matters

What would you like to work on first? Feel free to ask about the problem statement, approach, or any specific challenges you're facing!"""
    
    def _apply_guardrails(self, response: str) -> str:
        """Apply guardrails to filter out full solutions."""
        
        # Check for full solution patterns
        solution_indicators = [
            "def solution(",
            "class Solution:",
            "public class Solution",
            "int solution(",
            "vector<int> solution(",
            "here's the complete solution",
            "here's the full solution",
            "here's the answer:",
            "the solution is:",
            "complete code:",
            "full code:"
        ]
        
        response_lower = response.lower()
        for indicator in solution_indicators:
            if indicator in response_lower:
                return "I can't provide the complete solution, but I'd be happy to help you work through the problem step by step! What specific part are you struggling with?"
        
        # Check for code blocks that are too long (likely full solutions)
        if "```" in response:
            code_blocks = response.split("```")
            for i in range(1, len(code_blocks), 2):  # Every odd index is a code block
                if len(code_blocks[i].strip()) > 200:  # Arbitrary threshold
                    return "I can't provide the complete solution, but I'd be happy to help you work through the problem step by step! What specific part are you struggling with?"
        
        return response
    
    async def close(self):
        """Clean up resources."""
        pass
