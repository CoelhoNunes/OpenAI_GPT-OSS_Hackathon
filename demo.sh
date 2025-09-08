#!/bin/bash

# LeetCoach Demo Script
# This script demonstrates the key features of LeetCoach

set -e

echo "🚀 LeetCoach Demo Script"
echo "========================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_status "Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Check if services are healthy
check_services() {
    print_status "Checking service health..."
    
    # Check web service
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_success "Web service is healthy"
    else
        print_warning "Web service is not responding"
    fi
    
    # Check API service
    if curl -f http://localhost:8000/healthz > /dev/null 2>&1; then
        print_success "API service is healthy"
    else
        print_warning "API service is not responding"
    fi
    
    # Check runner service
    if curl -f http://localhost:8002/health > /dev/null 2>&1; then
        print_success "Runner service is healthy"
    else
        print_warning "Runner service is not responding"
    fi
    
    # Check CUDA service
    if curl -f http://localhost:8001/health > /dev/null 2>&1; then
        print_success "CUDA acceleration service is healthy"
    else
        print_warning "CUDA acceleration service is not responding"
    fi
}

# Start services if not running
start_services() {
    print_status "Starting LeetCoach services..."
    
    if ! docker compose ps | grep -q "Up"; then
        print_status "Services not running, starting them..."
        make up
        print_status "Waiting for services to be ready..."
        sleep 30
    else
        print_success "Services are already running"
    fi
}

# Demo problem selection
demo_problem_selection() {
    print_status "Demo: Problem Selection"
    echo ""
    echo "1. Open your browser and go to: http://localhost:3000"
    echo "2. You'll see the LeetCoach interface with:"
    echo "   - Left panel: GPT-OSS Coach (currently inactive)"
    echo "   - Main area: Problems tab with sample problems"
    echo ""
    echo "3. Click on any problem card to select it:"
    echo "   - 'Two Sum' (Arrays & Strings, Easy)"
    echo "   - 'Reverse Linked List' (Linked List, Easy)"
    echo "   - 'Valid Parentheses' (Stack & Queue, Easy)"
    echo ""
    echo "4. Notice how the GPT-OSS coach panel activates"
    echo ""
    read -p "Press Enter when you've selected a problem..."
}

# Demo GPT-OSS coaching
demo_coaching() {
    print_status "Demo: GPT-OSS Coaching"
    echo ""
    echo "1. In the left coach panel, try these questions:"
    echo "   - 'What's the best approach for this problem?'"
    echo "   - 'What edge cases should I consider?'"
    echo "   - 'What's the time complexity of a hash map approach?'"
    echo ""
    echo "2. Notice how the coach:"
    echo "   - Provides helpful hints without giving away the solution"
    echo "   - Suggests strategies and approaches"
    echo "   - Points out edge cases and complexity considerations"
    echo "   - Never provides complete code solutions"
    echo ""
    echo "3. Try asking for the full solution - the coach will refuse"
    echo "   and direct you to the Solutions tab (which is locked)"
    echo ""
    read -p "Press Enter when you've tried the coaching features..."
}

# Demo code editing
demo_editing() {
    print_status "Demo: Code Editing"
    echo ""
    echo "1. Switch to the Editor tab"
    echo "2. Notice the Monaco editor with:"
    echo "   - Syntax highlighting for Python/C++"
    echo "   - Auto-completion and IntelliSense"
    echo "   - Language toggle (Python/C++)"
    echo ""
    echo "3. Try writing some code:"
    echo "   - For Two Sum: def twoSum(nums, target):"
    echo "   - For Reverse List: def reverseList(head):"
    echo "   - For Valid Parentheses: def isValid(s):"
    echo ""
    echo "4. Use keyboard shortcuts:"
    echo "   - Ctrl+Enter: Run code"
    echo "   - Shift+Enter: Submit code"
    echo ""
    read -p "Press Enter when you've tried the editor..."
}

# Demo code submission
demo_submission() {
    print_status "Demo: Code Submission"
    echo ""
    echo "1. Write a simple solution (even if incorrect)"
    echo "2. Click Submit to run your code"
    echo "3. Switch to the Results tab to see:"
    echo "   - Test case results (Pass/Fail/Error)"
    echo "   - Runtime and memory usage"
    echo "   - Detailed error messages if any"
    echo ""
    echo "4. Notice the verdict:"
    echo "   - AC: Accepted (all tests pass)"
    echo "   - WA: Wrong Answer (some tests fail)"
    echo "   - TLE: Time Limit Exceeded"
    echo "   - RE: Runtime Error"
    echo "   - CE: Compilation Error"
    echo ""
    read -p "Press Enter when you've submitted code and viewed results..."
}

# Demo solutions unlock
demo_solutions() {
    print_status "Demo: Solutions Unlock"
    echo ""
    echo "1. After your first submission, switch to the Solutions tab"
    echo "2. Notice that solutions are now unlocked and show:"
    echo "   - Python reference solution"
    echo "   - C++ reference solution"
    echo "   - Detailed explanation of the approach"
    echo "   - Time and space complexity analysis"
    echo ""
    echo "3. This demonstrates the learning-focused approach:"
    echo "   - Solutions are locked until you attempt the problem"
    echo "   - Encourages independent problem-solving"
    echo "   - Provides reference implementations for learning"
    echo ""
    read -p "Press Enter when you've viewed the solutions..."
}

# Demo problem randomization
demo_randomization() {
    print_status "Demo: Problem Randomization"
    echo ""
    echo "1. Go back to the Problems tab"
    echo "2. Click 'Randomize Problem' to get a new instance"
    echo "3. Notice how:"
    echo "   - The problem title stays the same"
    echo "   - But the test cases and inputs are different"
    echo "   - This prevents copying solutions from other platforms"
    echo ""
    echo "4. Try multiple randomizations to see the variety"
    echo ""
    read -p "Press Enter when you've tried randomization..."
}

# Demo CUDA acceleration
demo_cuda() {
    print_status "Demo: CUDA Acceleration"
    echo ""
    echo "1. The CUDA acceleration service runs in the background"
    echo "2. It provides:"
    echo "   - GPU-accelerated input generation for large test cases"
    echo "   - Parallel computation of expected outputs"
    echo "   - Automatic CPU fallback when GPU is unavailable"
    echo ""
    echo "3. Check the service status:"
    echo "   curl http://localhost:8001/health"
    echo ""
    echo "4. The service is used automatically by the API for:"
    echo "   - Generating large arrays for array problems"
    echo "   - Computing complex expected outputs"
    echo "   - Accelerating problem template generation"
    echo ""
    read -p "Press Enter to continue..."
}

# Show API documentation
demo_api() {
    print_status "Demo: API Documentation"
    echo ""
    echo "1. Open the API documentation: http://localhost:8000/docs"
    echo "2. Explore the endpoints:"
    echo "   - /problems/random - Get random problem"
    echo "   - /submit/ - Submit code for execution"
    echo "   - /chat/ - Send message to GPT-OSS coach"
    echo "   - /solutions/{id} - Get reference solutions"
    echo ""
    echo "3. Try the interactive API explorer"
    echo "4. Notice the comprehensive request/response schemas"
    echo ""
    read -p "Press Enter when you've explored the API docs..."
}

# Main demo flow
main() {
    echo "Welcome to the LeetCoach demo!"
    echo ""
    echo "This demo will walk you through the key features:"
    echo "1. Problem selection and GPT-OSS coaching"
    echo "2. Code editing with Monaco editor"
    echo "3. Code submission and results"
    echo "4. Solutions unlock after submission"
    echo "5. Problem randomization"
    echo "6. CUDA acceleration"
    echo "7. API documentation"
    echo ""
    
    read -p "Press Enter to start the demo..."
    
    # Check prerequisites
    check_docker
    start_services
    check_services
    
    echo ""
    print_success "All services are ready! Starting demo..."
    echo ""
    
    # Run demo steps
    demo_problem_selection
    demo_coaching
    demo_editing
    demo_submission
    demo_solutions
    demo_randomization
    demo_cuda
    demo_api
    
    echo ""
    print_success "Demo completed!"
    echo ""
    echo "Key takeaways:"
    echo "✅ GPT-OSS provides helpful coaching without revealing solutions"
    echo "✅ Monaco editor offers professional coding experience"
    echo "✅ Sandboxed execution ensures security"
    echo "✅ Solutions unlock after first attempt encourages learning"
    echo "✅ Problem randomization prevents solution copying"
    echo "✅ CUDA acceleration improves performance"
    echo "✅ Comprehensive API enables integration"
    echo ""
    echo "Next steps:"
    echo "1. Explore more problem categories"
    echo "2. Try different difficulty levels"
    echo "3. Experiment with the GPT-OSS coach"
    echo "4. Check out the API documentation"
    echo "5. Review the source code and architecture"
    echo ""
    echo "Thank you for trying LeetCoach! 🎉"
}

# Run the demo
main "$@"
