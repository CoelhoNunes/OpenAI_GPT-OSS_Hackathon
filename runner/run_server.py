"""
Code execution server - sandboxed code runner
"""

import asyncio
import json
import subprocess
import tempfile
import os
import time
import psutil
from typing import Dict, Any, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="LeetCoach Runner", version="1.0.0")


class ExecutionRequest(BaseModel):
    language: str
    code: str
    test_cases: List[Dict[str, Any]]


class TestResult(BaseModel):
    status: str  # PASS, FAIL, ERROR
    input: Dict[str, Any]
    expected_output: Any
    actual_output: Any
    error_message: str = ""
    runtime_ms: int = 0


class ExecutionResponse(BaseModel):
    verdict: str
    test_results: List[TestResult]
    total_runtime_ms: int
    peak_memory_kb: int
    compilation_output: str = ""
    runtime_output: str = ""


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "leetcoach-runner"}


@app.post("/execute", response_model=ExecutionResponse)
async def execute_code(request: ExecutionRequest):
    """Execute code with test cases."""
    
    if request.language not in ["python", "cpp"]:
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    try:
        if request.language == "python":
            return await execute_python(request)
        elif request.language == "cpp":
            return await execute_cpp(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


async def execute_python(request: ExecutionRequest) -> ExecutionResponse:
    """Execute Python code."""
    
    test_results = []
    total_runtime = 0
    peak_memory = 0
    
    # Create temporary file for code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(request.code)
        temp_file = f.name
    
    try:
        # Compile and check syntax
        compile_result = subprocess.run(
            ['python3', '-m', 'py_compile', temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if compile_result.returncode != 0:
            return ExecutionResponse(
                verdict="COMPILE_ERROR",
                test_results=[],
                total_runtime_ms=0,
                peak_memory_kb=0,
                compilation_output=compile_result.stderr
            )
        
        # Run test cases
        for i, test_case in enumerate(request.test_cases):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024  # KB
            
            try:
                # Create test runner script
                test_script = f"""
import sys
import json
import traceback

# Load the user's code
exec(open('{temp_file}').read())

# Get test case
test_input = {json.dumps(test_case['input'])}
expected = {json.dumps(test_case['expected_output'])}

try:
    # Find the main function (look for common function names first)
    import inspect
    functions = [name for name, obj in globals().items() 
                if inspect.isfunction(obj) and not name.startswith('_')]
    
    if not functions:
        print(json.dumps({{"error": "No function found"}}))
        sys.exit(1)
    
    # Try to find a function that matches common patterns
    main_func = None
    function_names = [f for f in functions if f.lower() in ['twosum', 'twosum', 'solution', 'main']]
    if function_names:
        main_func = globals()[function_names[0]]
    else:
        # Fall back to first function
        main_func = globals()[functions[0]]
    
    # Call the function
    if isinstance(test_input, dict):
        result = main_func(**test_input)
    else:
        result = main_func(test_input)
    
    # Check result - handle different comparison cases
    def deep_compare(a, b):
        if isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                return False
            # For lists, check if they contain the same elements (order might matter)
            return sorted(a) == sorted(b) or a == b
        return a == b
    
    if deep_compare(result, expected):
        print(json.dumps({{"status": "PASS", "result": result}}))
    else:
        print(json.dumps({{"status": "FAIL", "result": result, "expected": expected}}))
        
except Exception as e:
    print(json.dumps({{"status": "ERROR", "error": str(e), "traceback": traceback.format_exc()}}))
"""
                
                # Execute test
                result = subprocess.run(
                    ['python3', '-c', test_script],
                    capture_output=True,
                    text=True,
                    timeout=2  # 2 second timeout per test
                )
                
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024
                
                runtime_ms = int((end_time - start_time) * 1000)
                memory_kb = int(end_memory - start_memory)
                
                total_runtime += runtime_ms
                peak_memory = max(peak_memory, memory_kb)
                
                # Parse result
                if result.returncode == 0:
                    try:
                        result_data = json.loads(result.stdout.strip())
                        status = result_data.get("status", "ERROR")
                        
                        if status == "PASS":
                            test_results.append(TestResult(
                                status="PASS",
                                input=test_case['input'],
                                expected_output=test_case['expected_output'],
                                actual_output=result_data.get("result"),
                                runtime_ms=runtime_ms
                            ))
                        elif status == "FAIL":
                            test_results.append(TestResult(
                                status="FAIL",
                                input=test_case['input'],
                                expected_output=test_case['expected_output'],
                                actual_output=result_data.get("result"),
                                runtime_ms=runtime_ms
                            ))
                        else:
                            test_results.append(TestResult(
                                status="ERROR",
                                input=test_case['input'],
                                expected_output=test_case['expected_output'],
                                actual_output=None,
                                error_message=result_data.get("error", "Unknown error"),
                                runtime_ms=runtime_ms
                            ))
                    except json.JSONDecodeError:
                        test_results.append(TestResult(
                            status="ERROR",
                            input=test_case['input'],
                            expected_output=test_case['expected_output'],
                            actual_output=None,
                            error_message="Invalid output format",
                            runtime_ms=runtime_ms
                        ))
                else:
                    test_results.append(TestResult(
                        status="ERROR",
                        input=test_case['input'],
                        expected_output=test_case['expected_output'],
                        actual_output=None,
                        error_message=result.stderr or "Runtime error",
                        runtime_ms=runtime_ms
                    ))
                    
            except subprocess.TimeoutExpired:
                test_results.append(TestResult(
                    status="ERROR",
                    input=test_case['input'],
                    expected_output=test_case['expected_output'],
                    actual_output=None,
                    error_message="Time limit exceeded",
                    runtime_ms=2000
                ))
                total_runtime += 2000
    
    finally:
        # Clean up
        os.unlink(temp_file)
    
    # Determine verdict
    passed = sum(1 for tr in test_results if tr.status == "PASS")
    total = len(test_results)
    
    if passed == total:
        verdict = "ACCEPTED"
    elif any(tr.status == "ERROR" for tr in test_results):
        verdict = "RUNTIME_ERROR"
    else:
        verdict = "WRONG_ANSWER"
    
    return ExecutionResponse(
        verdict=verdict,
        test_results=test_results,
        total_runtime_ms=total_runtime,
        peak_memory_kb=peak_memory,
        compilation_output=""
    )


async def execute_cpp(request: ExecutionRequest) -> ExecutionResponse:
    """Execute C++ code."""
    
    test_results = []
    total_runtime = 0
    peak_memory = 0
    
    # Determine the problem type based on the test case input
    first_test_case = request.test_cases[0] if request.test_cases else {}
    input_keys = list(first_test_case.get('input', {}).keys())
    
    # Create a complete C++ program with main function
    if 'nums' in input_keys and 'target' in input_keys:
        # Two Sum problem
        cpp_program = f"""
#include <iostream>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <string>
using namespace std;

{request.code}

// Helper function to parse vector from string
vector<int> parseVector(const string& s) {{
    vector<int> result;
    stringstream ss(s);
    string item;
    while (getline(ss, item, ',')) {{
        if (item.find('[') != string::npos) {{
            item = item.substr(item.find('[') + 1);
        }}
        if (item.find(']') != string::npos) {{
            item = item.substr(0, item.find(']'));
        }}
        if (!item.empty()) {{
            result.push_back(stoi(item));
        }}
    }}
    return result;
}}

// Helper function to print vector
void printVector(const vector<int>& v) {{
    cout << "[";
    for (int i = 0; i < v.size(); i++) {{
        if (i > 0) cout << ",";
        cout << v[i];
    }}
    cout << "]";
}}

int main() {{
    string line;
    while (getline(cin, line)) {{
        // Parse input format: nums=[1,2,3], target=4
        size_t nums_start = line.find("nums=[");
        size_t nums_end = line.find("], target=");
        size_t target_start = line.find("target=");
        
        if (nums_start != string::npos && nums_end != string::npos && target_start != string::npos) {{
            string nums_str = line.substr(nums_start + 6, nums_end - nums_start - 6);
            string target_str = line.substr(target_start + 7);
            
            vector<int> nums = parseVector(nums_str);
            int target = stoi(target_str);
            
            Solution sol;
            vector<int> result = sol.twoSum(nums, target);
            printVector(result);
            cout << endl;
        }}
    }}
    return 0;
}}
"""
    elif 'head' in input_keys:
        # Linked List problem (like Reverse Linked List)
        cpp_program = f"""
#include <iostream>
#include <vector>
#include <sstream>
#include <string>
using namespace std;

// Definition for singly-linked list
struct ListNode {{
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {{}}
    ListNode(int x) : val(x), next(nullptr) {{}}
    ListNode(int x, ListNode *next) : val(x), next(next) {{}}
}};

{request.code}

// Helper function to create linked list from vector
ListNode* createList(const vector<int>& values) {{
    if (values.empty()) return nullptr;
    
    ListNode* head = new ListNode(values[0]);
    ListNode* current = head;
    
    for (int i = 1; i < values.size(); i++) {{
        current->next = new ListNode(values[i]);
        current = current->next;
    }}
    
    return head;
}}

// Helper function to convert linked list to vector
vector<int> listToVector(ListNode* head) {{
    vector<int> result;
    ListNode* current = head;
    
    while (current != nullptr) {{
        result.push_back(current->val);
        current = current->next;
    }}
    
    return result;
}}

// Helper function to print vector
void printVector(const vector<int>& v) {{
    cout << "[";
    for (int i = 0; i < v.size(); i++) {{
        if (i > 0) cout << ",";
        cout << v[i];
    }}
    cout << "]";
}}

int main() {{
    string line;
    while (getline(cin, line)) {{
        // Parse input format: head=[1,2,3]
        size_t head_start = line.find("head=[");
        size_t head_end = line.find("]");
        
        if (head_start != string::npos && head_end != string::npos) {{
            string head_str = line.substr(head_start + 6, head_end - head_start - 6);
            
            vector<int> values;
            if (!head_str.empty()) {{
                stringstream ss(head_str);
                string item;
                while (getline(ss, item, ',')) {{
                    if (!item.empty()) {{
                        values.push_back(stoi(item));
                    }}
                }}
            }}
            
            ListNode* head = createList(values);
            Solution sol;
            ListNode* result = sol.reverseList(head);
            vector<int> result_vec = listToVector(result);
            printVector(result_vec);
            cout << endl;
        }}
    }}
    return 0;
}}
"""
    elif 'nums' in input_keys and len(input_keys) == 1:
        # Array problem (like Contains Duplicate)
        cpp_program = f"""
#include <iostream>
#include <vector>
#include <unordered_set>
#include <sstream>
#include <string>
using namespace std;

{request.code}

// Helper function to parse vector from string
vector<int> parseVector(const string& s) {{
    vector<int> result;
    stringstream ss(s);
    string item;
    while (getline(ss, item, ',')) {{
        if (item.find('[') != string::npos) {{
            item = item.substr(item.find('[') + 1);
        }}
        if (item.find(']') != string::npos) {{
            item = item.substr(0, item.find(']'));
        }}
        if (!item.empty()) {{
            result.push_back(stoi(item));
        }}
    }}
    return result;
}}

int main() {{
    string line;
    while (getline(cin, line)) {{
        // Parse input format: nums=[1,2,3,1]
        size_t nums_start = line.find("nums=[");
        size_t nums_end = line.find("]");
        
        if (nums_start != string::npos && nums_end != string::npos) {{
            string nums_str = line.substr(nums_start + 6, nums_end - nums_start - 6);
            vector<int> nums = parseVector(nums_str);
            
            Solution sol;
            bool result = sol.containsDuplicate(nums);
            cout << (result ? "true" : "false") << endl;
        }}
    }}
    return 0;
}}
"""
    else:
        # Generic fallback - just try to compile the code as-is
        cpp_program = f"""
#include <iostream>
#include <vector>
#include <unordered_map>
#include <sstream>
#include <string>
using namespace std;

{request.code}

int main() {{
    // Generic main function - may need customization for specific problems
    return 0;
}}
"""
    
    # Create temporary file for the complete C++ program
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
        f.write(cpp_program)
        cpp_file = f.name
    
    try:
        # Compile C++ code
        compile_result = subprocess.run(
            ['g++', '-O2', '-std=c++17', '-o', cpp_file.replace('.cpp', ''), cpp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if compile_result.returncode != 0:
            return ExecutionResponse(
                verdict="COMPILE_ERROR",
                test_results=[],
                total_runtime_ms=0,
                peak_memory_kb=0,
                compilation_output=compile_result.stderr
            )
        
        # Run test cases
        for test_case in request.test_cases:
            start_time = time.time()
            
            try:
                # Create input in the format expected by our C++ program
                input_data = test_case['input']
                
                if 'nums' in input_data and 'target' in input_data:
                    # Two Sum problem
                    nums = input_data.get('nums', [])
                    target = input_data.get('target', 0)
                    input_str = f"nums=[{','.join(map(str, nums))}], target={target}\n"
                elif 'nums' in input_data and len(input_data) == 1:
                    # Array problem (like Contains Duplicate)
                    nums = input_data.get('nums', [])
                    input_str = f"nums=[{','.join(map(str, nums))}]\n"
                elif 'head' in input_data:
                    # Linked List problem
                    head = input_data.get('head', [])
                    input_str = f"head=[{','.join(map(str, head))}]\n"
                elif 's' in input_data:
                    # String problem (like Valid Parentheses)
                    s = input_data.get('s', '')
                    input_str = f's=\\"{s}\\"\n'
                else:
                    # Generic fallback
                    input_str = f"{input_data}\n"
                
                # Execute
                result = subprocess.run(
                    [cpp_file.replace('.cpp', '')],
                    input=input_str,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                end_time = time.time()
                runtime_ms = int((end_time - start_time) * 1000)
                total_runtime += runtime_ms
                
                # Parse result
                if result.returncode == 0:
                    try:
                        # Parse the output vector
                        output_str = result.stdout.strip()
                        if output_str.startswith('[') and output_str.endswith(']'):
                            # Extract numbers from [1,2,3] format
                            content = output_str[1:-1]
                            if content:
                                actual_output = [int(x.strip()) for x in content.split(',')]
                            else:
                                actual_output = []
                        else:
                            actual_output = []
                        
                        # Handle different comparison cases for C++
                        def deep_compare(a, b):
                            if isinstance(a, list) and isinstance(b, list):
                                if len(a) != len(b):
                                    return False
                                # For lists, check if they contain the same elements (order might matter)
                                return sorted(a) == sorted(b) or a == b
                            return a == b
                        
                        if deep_compare(actual_output, test_case['expected_output']):
                            test_results.append(TestResult(
                                status="PASS",
                                input=test_case['input'],
                                expected_output=test_case['expected_output'],
                                actual_output=actual_output,
                                runtime_ms=runtime_ms
                            ))
                        else:
                            test_results.append(TestResult(
                                status="FAIL",
                                input=test_case['input'],
                                expected_output=test_case['expected_output'],
                                actual_output=actual_output,
                                runtime_ms=runtime_ms
                            ))
                    except (ValueError, IndexError) as e:
                        test_results.append(TestResult(
                            status="ERROR",
                            input=test_case['input'],
                            expected_output=test_case['expected_output'],
                            actual_output=None,
                            error_message=f"Invalid output format: {str(e)}",
                            runtime_ms=runtime_ms
                        ))
                else:
                    test_results.append(TestResult(
                        status="ERROR",
                        input=test_case['input'],
                        expected_output=test_case['expected_output'],
                        actual_output=None,
                        error_message=result.stderr or "Runtime error",
                        runtime_ms=runtime_ms
                    ))
                
            except subprocess.TimeoutExpired:
                test_results.append(TestResult(
                    status="ERROR",
                    input=test_case['input'],
                    expected_output=test_case['expected_output'],
                    actual_output=None,
                    error_message="Time limit exceeded",
                    runtime_ms=2000
                ))
                total_runtime += 2000
    
    finally:
        # Clean up
        os.unlink(cpp_file)
        if os.path.exists(cpp_file.replace('.cpp', '')):
            os.unlink(cpp_file.replace('.cpp', ''))
    
    # Determine verdict
    passed = sum(1 for tr in test_results if tr.status == "PASS")
    total = len(test_results)
    
    if passed == total:
        verdict = "ACCEPTED"
    elif any(tr.status == "ERROR" for tr in test_results):
        verdict = "RUNTIME_ERROR"
    else:
        verdict = "WRONG_ANSWER"
    
    return ExecutionResponse(
        verdict=verdict,
        test_results=test_results,
        total_runtime_ms=total_runtime,
        peak_memory_kb=peak_memory,
        compilation_output=""
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
