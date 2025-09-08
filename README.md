# LeetCoach - GPT-OSS Powered Coding Practice

A professional, containerized LeetCode-style practice app that teaches data structures and algorithms with **GPT-OSS exclusively** as the coaching AI and **CUDA acceleration** for large-scale problem generation.

## 🚀 Features

### Core Functionality
- **5 Data Structure Categories**: Arrays & Strings, Linked List, Stack & Queue, Hash Map/Set, Binary Tree/BST
- **Randomized Problems**: Seeded problem generation ensures unique instances every time
- **Dual Language Support**: Python and C++ with syntax highlighting and auto-completion
- **Real-time Execution**: Sandboxed code runner with time/memory limits
- **Comprehensive Testing**: Automated test case execution with detailed results

### GPT-OSS Integration
- **Exclusive GPT-OSS Models**: Uses only `gpt-oss-20b` or `gpt-oss-120b` weights
- **Local-First Architecture**: vLLM (GPT-OSS only)
- **Strict Guardrails**: Server-enforced coaching that never reveals full solutions
- **Context-Aware Coaching**: Problem-specific hints, strategy guidance, and complexity analysis

### CUDA Acceleration
- **GPU-Accelerated Generation**: Large-N input generation for array/string problems
- **Expected Output Computation**: Parallel computation of reference solutions
- **Automatic Fallback**: Seamless CPU fallback when GPU unavailable
- **NVIDIA Container Toolkit**: Full GPU support with `--gpus all`

### Professional UI/UX
- **Monaco Editor**: VS Code-like editing experience with IntelliSense
- **Persistent Coach Panel**: Left-side GPT-OSS coaching with real-time chat
- **Tabbed Interface**: Problems, Editor, Results, and Solutions tabs
- **Responsive Design**: Clean Tailwind CSS with shadcn/ui components

## 🏗️ Architecture

### 5-Service Docker Compose Setup
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Web      │    │     API     │    │   Runner    │
│  (Next.js)  │◄──►│  (FastAPI)  │◄──►│ (Sandbox)   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Database  │    │ CUDA Accel  │
                   │ (PostgreSQL)│    │ (C++/CUDA)  │
                   └─────────────┘    └─────────────┘
```

### Service Responsibilities
- **Web**: Next.js 14 frontend with Monaco editor and real-time chat
- **API**: FastAPI backend with problem generation, GPT-OSS integration, and guardrails
- **Runner**: Sandboxed Python/C++ execution with resource limits
- **CUDA Accel**: GPU-accelerated input generation and expected output computation
- **Database**: PostgreSQL for problems, submissions, and chat history

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- NVIDIA Container Toolkit (for GPU support)
- 8GB+ RAM recommended

### 1. Clone and Setup
```bash
git clone <repository-url>
cd leetcoach

# Copy environment file
cp env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Start Services
```bash
# Standard startup
make up

# With GPU support
make up-gpu

# Or manually
docker compose up --build
```

### 3. Access the Application
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: `make health`

## ⚙️ Configuration

### Environment Variables
```bash
# Model Configuration (GPT-OSS only)
GPT_OSS_MODEL=openai/gpt-oss-20b             # pinned to gpt-oss-20b
ALLOW_NON_GPT_OSS=false                      # Strict GPT-OSS enforcement

# vLLM Configuration
VLLM_BASE_URL=http://localhost:8000

# Hugging Face Token (optional if model is gated)
HF_TOKEN=

# CUDA Configuration
CUDA_VISIBLE_DEVICES=0
```

### Model Setup

#### vLLM Server (Used by Compose)
```bash
# The compose file starts vLLM automatically and exposes port 8003 -> 8000
# Health endpoint used: http://localhost:8003/v1/models
```

## 🎯 Usage Guide

### 3-Minute Demo Script

1. **Start the Application**
   ```bash
   make up
   ```

2. **Select a Problem**
   - Go to Problems tab
   - Click on any problem card
   - Notice the GPT-OSS coach activates

3. **Get Coaching**
   - Ask the coach: "What's the best approach for this problem?"
   - Try: "What edge cases should I consider?"
   - Ask: "What's the time complexity of a hash map approach?"

4. **Write Code**
   - Switch to Editor tab
   - Choose Python or C++
   - Write your solution

5. **Submit and Review**
   - Click Submit to run your code
   - Check Results tab for test case outcomes
   - Solutions tab unlocks after first submission

### Problem Categories

#### Arrays & Strings
- Two Sum, Rotate Array, Group Anagrams
- Longest Substring, Product Except Self

#### Linked List  
- Reverse List, Merge Two Lists, Detect Cycle
- Remove Nth Node, Palindrome List

#### Stack & Queue
- Valid Parentheses, Min Stack, Daily Temperatures
- Largest Rectangle, Sliding Window Max

#### Hash Map / Hash Set
- Contains Duplicate, Single Number, Intersection
- Happy Number, Isomorphic Strings

#### Binary Tree / BST
- Max Depth, Invert Tree, Path Sum
- Lowest Common Ancestor, Validate BST

## 🛡️ GPT-OSS Guardrails

### Server-Enforced Restrictions
- **No Full Solutions**: Coach never provides complete implementations
- **Code Snippet Limit**: Maximum 6 lines of illustrative code
- **Response Filtering**: Server-side truncation of long responses
- **Solution Locking**: Reference solutions only unlock after first submission

### Coaching Behavior
- **Strategy Guidance**: High-level approach suggestions
- **Edge Case Hints**: Pointing out important test cases
- **Complexity Analysis**: Time/space complexity discussions
- **Syntax Reminders**: Small code snippets for syntax help

## 🔧 Development

### Project Structure
```
leetcoach/
├── api/                    # FastAPI backend
│   ├── src/
│   │   ├── core/          # Configuration, database, schemas
│   │   ├── routers/       # API endpoints
│   │   └── services/      # Business logic
│   └── Dockerfile
├── web/                   # Next.js frontend
│   ├── src/
│   │   ├── app/          # App router pages
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities and state
│   └── Dockerfile
├── runner/               # Code execution service
│   ├── run_server.py     # Sandboxed execution
│   └── Dockerfile
├── cuda_accel/          # CUDA acceleration
│   ├── src/             # CUDA kernels and bindings
│   ├── CMakeLists.txt   # Build configuration
│   └── Dockerfile
├── db/                  # Database initialization
└── docker-compose.yml   # Service orchestration
```

### Development Commands
```bash
# Start development environment
make dev

# Run tests
make test

# Lint code
make lint

# View logs
make logs

# Clean up
make clean
```

### Adding New Problem Templates

1. **Create Generator**
   ```python
   # api/src/services/problem_gen/new_category.py
   class NewCategoryGenerator(ProblemGenerator):
       def get_templates(self) -> List[str]:
           return ["template1", "template2"]
       
       def generate(self, seed: int, difficulty: str):
           # Implementation
   ```

2. **Register Generator**
   ```python
   # api/src/services/problem_gen/__init__.py
   registry.register("New Category", NewCategoryGenerator())
   ```

3. **Add CUDA Support** (Optional)
   ```cpp
   // cuda_accel/src/kernels.cu
   void cuda_new_template_generate(/* params */) {
       // CUDA implementation
   }
   ```

## 🧪 Testing

### Test Coverage
- **Problem Generation**: Deterministic seeded generation
- **Code Execution**: Timeout and memory limit testing
- **GPT-OSS Integration**: Guardrail enforcement
- **CUDA Acceleration**: GPU/CPU fallback verification

### Running Tests
```bash
# API tests
cd api && python -m pytest tests/ -v

# CUDA tests  
cd cuda_accel && python -m pytest tests/ -v

# Web tests
cd web && npm test

# All tests
make test
```

## 🚀 Deployment

### Production Setup
```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Deploy with GPU support
docker compose -f docker-compose.prod.yml up -d

# Scale services
docker compose -f docker-compose.prod.yml up -d --scale api=3
```

### Environment Variables for Production
```bash
# Security
SECRET_KEY=your-secure-secret-key
ALLOWED_ORIGINS=https://yourdomain.com

# Database
DATABASE_URL=postgresql://user:pass@db:5432/leetcoach

# Model Configuration
GPT_OSS_MODEL=openai/gpt-oss-20b
VLLM_BASE_URL=http://vllm-server:8000
```

## 📊 Performance

### Benchmarks
- **Problem Generation**: <100ms for standard templates
- **Code Execution**: 2s timeout per test case
- **GPT-OSS Response**: <2s for coaching messages
- **CUDA Acceleration**: 10x speedup for large-N generation

### Resource Requirements
- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB RAM, 4 CPU cores, NVIDIA GPU
- **Production**: 16GB RAM, 8 CPU cores, RTX 3080+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run linting: `make lint`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style
- **Python**: Black, Ruff, MyPy
- **TypeScript**: ESLint, Prettier
- **C++/CUDA**: clang-format, cppcheck

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GPT-OSS Community**: For open-weight language models
- **NVIDIA**: For CUDA acceleration capabilities
- **FastAPI**: For the excellent Python web framework
- **Next.js**: For the React framework
- **Monaco Editor**: For the code editing experience

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)

---

**Built with ❤️ using GPT-OSS exclusively for AI coaching and CUDA for acceleration**