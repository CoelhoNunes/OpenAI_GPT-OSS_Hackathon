# LeetCoach — Your AI Coding Mentor

LeetCoach is not just another coding practice app — it’s your **personal AI-powered mentor** for mastering data structures and algorithms.  
Built **exclusively on GPT-OSS** with **CUDA acceleration**, it delivers a **fully local, high-performance coaching experience** — no internet calls, no distractions, just pure coding growth.  

---

## Why LeetCoach?  
- **Interactive Coaching**: GPT-OSS guides you with tailored hints, strategy tips, and complexity analysis.  
- **LeetCode-Style Problems**: Fresh, randomized challenges every session — no boring repeats.  
- **GPU-Powered Speed**: CUDA acceleration generates and validates problems at scale.  
- **Local & Private**: 100% local inference with gpt-oss, keeping your work safe and offline.  

LeetCoach is designed to feel like **pair-programming with a senior engineer**, but one who never sleeps, never judges, and always pushes you to think deeper.  

---

## Features  

### Core Functionality  
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

---

🔥 **LeetCoach is here to make practicing algorithms fun, fast, and fearless.**  
Train smarter, code faster, and let **GPT-OSS + CUDA** take your interview prep to the next level.  

---

## 🖼️ Visuals & Badges  

![Build](https://img.shields.io/badge/build-passing-brightgreen)  
![CUDA](https://img.shields.io/badge/CUDA-Accelerated-blue)  
![Model](https://img.shields.io/badge/GPT--OSS-20b-orange)  
![License](https://img.shields.io/badge/license-Apache%202.0-green)  
![Made With](https://img.shields.io/badge/Made%20With-%E2%9D%A4%20and%20GPT--OSS-red)  

---

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

## 🛡️ GPT-OSS Guardrails

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
## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run linting: `make lint`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 🙏 Acknowledgments

- **GPT-OSS Community**: For open-weight language models
- **NVIDIA**: For CUDA acceleration capabilities
- **FastAPI**: For the excellent Python web framework
- **Next.js**: For the React framework
- **Monaco Editor**: For the code editing experience
