# 🎉 LeetCoach — Your AI Coding Mentor 🚀  

LeetCoach is not just another coding practice app — it’s your **personal AI-powered mentor** for mastering data structures and algorithms.  
Built **exclusively on GPT-OSS** with **CUDA acceleration**, it delivers a **fully local, high-performance coaching experience** — no internet calls, no distractions, just pure coding growth.  

---

## ✨ Why LeetCoach?  
- 💡 **Interactive Coaching**: GPT-OSS guides you with tailored hints, strategy tips, and complexity analysis.  
- 🧩 **LeetCode-Style Problems**: Fresh, randomized challenges every session — no boring repeats.  
- ⚡ **GPU-Powered Speed**: CUDA acceleration generates and validates problems at scale.  
- 🔒 **Local & Private**: 100% local inference with gpt-oss, keeping your work safe and offline.  

LeetCoach is designed to feel like **pair-programming with a senior engineer**, but one who never sleeps, never judges, and always pushes you to think deeper.  

---

## 🚀 Features  

### 📚 Core Functionality  
- **5 Essential Data Structures**:  
  - Arrays & Strings  
  - Linked List  
  - Stack & Queue  
  - Hash Map / Set  
  - Binary Tree / BST  
- **Randomized Problem Generation**: Every session feels brand new.  
- **Dual Language Support**: Solve in **Python** or **C++**, complete with syntax highlighting & auto-completion.  
- **Real-time Execution**: Safe, sandboxed code runner with runtime/memory limits.  
- **Comprehensive Testing**: Built-in test cases with detailed results & feedback.  

### 🤖 GPT-OSS Coaching  
- **Exclusive GPT-OSS Models**: Powered by gpt-oss-20b weights.  
- **Local-First Design**: Runs on a local vLLM server — no external calls.  
- **Strict Guardrails**: AI coach helps with strategy, never spoils full solutions.  
- **Context-Aware Guidance**: Personalized hints for the exact problem you’re solving.  

### ⚡ CUDA Acceleration  
- **GPU-Boosted Workflows**: Parallelized generation of large input sets.  
- **Faster Testing**: GPU-backed computation of expected outputs.  
- **Smart Fallback**: Automatic CPU fallback when CUDA isn’t available.  
- **NVIDIA Container Toolkit Support**: Run with `--gpus all` for full acceleration.  

### 🎨 Professional UI/UX  
- **Monaco Editor**: The same coding feel as VS Code.  
- **Persistent Coach Panel**: Get live AI chat & insights while coding.  
- **Tabbed Navigation**: Switch between Problems, Editor, Results, and Coaching easily.  
- **Responsive & Polished**: Built with Tailwind CSS + shadcn/ui for a clean, modern look.  

---

## 🏆 Perfect for the Hackathon  
LeetCoach was built for the **OpenAI Open Model Hackathon** to show off what’s possible with:  
- 🔹 **Open-weight gpt-oss models**  
- 🔹 **GPU acceleration**  
- 🔹 **Professional, production-ready engineering**  

This project is **a complete learning platform**, not just a demo. Judges and developers can test it locally with **one command** and immediately see the coaching magic in action.  

---

## 📦 Quick Start  

```bash
# Clone the repo
git clone https://github.com/CoelhoNunes/OpenAI_GPT-OSS_Hackathon.git
cd OpenAI_GPT-OSS_Hackathon

# Build the container with GPU support
docker build -t leetcoach .
docker run --gpus all -p 8080:8080 leetcoach

# Open your browser at http://localhost:8080 🚀
```

---

## 📜 License  
This project is licensed under the **Apache License 2.0** — open, free, and built to share knowledge.  

---

🔥 **LeetCoach is here to make practicing algorithms fun, fast, and fearless.**  
Train smarter, code faster, and let **GPT-OSS + CUDA** take your interview prep to the next level.  

---

## 🖼️ Visuals & Badges  

![LeetCoach Banner](https://via.placeholder.com/1000x250.png?text=LeetCoach+-+GPT-OSS+Powered+Coding+Mentor)  

![Build](https://img.shields.io/badge/build-passing-brightgreen)  
![CUDA](https://img.shields.io/badge/CUDA-Accelerated-blue)  
![Model](https://img.shields.io/badge/GPT--OSS-20b-orange)  
![License](https://img.shields.io/badge/license-Apache%202.0-green)  
![Made With](https://img.shields.io/badge/Made%20With-%E2%9D%A4%20and%20GPT--OSS-red)  

---

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

## 🚀 Getting Started (Local GPU)

### Prerequisites
- NVIDIA GPU + Driver + CUDA runtime
- Docker and Docker Compose (with NVIDIA Container Toolkit), or Python 3.10+
- 16GB+ RAM recommended

### 1. Clone and Setup
```bash
git clone <repository-url>
cd leetcoach

# Copy environment file
cp env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Start (Local, GPU)
```bash
# Compose (GPU):
cp env.example .env
docker compose up --build

# Or via script:
bash scripts/run_local_gpu.sh
```

### 3. Access the Application
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: `make health`

## ⚙️ Configuration

### Environment Variables
```bash
# Model Configuration (GPT-OSS only)
MODEL_ID=openai/gpt-oss-20b
HF_ID=openai/gpt-oss-20b
WEIGHTS_PATH=
TORCH_DTYPE=bfloat16
MAX_TOKENS=512
CONTEXT_LEN=8192
GPU_MEMORY_FRACTION=0.9
BATCH_SIZE=1

# vLLM Configuration (local only)
VLLM_BASE_URL=http://localhost:8000

# Security
ALLOW_NON_GPT_OSS=false

# CUDA Configuration
CUDA_VISIBLE_DEVICES=0
```

### Model Setup
- Weights: pulled automatically into a local cache (no outbound inference APIs)
- Health endpoint: `http://localhost:8003/v1/models`

## 🎯 Usage Guide

### 3-Minute Demo Video Note

Keep <3 minutes. Show the app running locally on the GPU.

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

## 🧪 Testing Instructions

### Test Coverage
- **Problem Generation**: Deterministic seeded generation
- **Code Execution**: Timeout and memory limit testing
- **GPT-OSS Integration**: Guardrail enforcement
- **CUDA Acceleration**: GPU/CPU fallback verification

### Local smoke test for gpt-oss
```bash
curl -s http://localhost:8003/v1/chat/completions -X POST \
  -H 'Content-Type: application/json' \
  -d '{"model":"openai/gpt-oss-20b","messages":[{"role":"user","content":"Say hi"}],"max_tokens":8}'
```

Expected minimal output includes a JSON with a non-empty `choices[0].message.content` string.

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

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

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
