import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

// Types
export interface Problem {
  problem_id: string
  category: string
  template_slug: string
  seed: number
  difficulty: string
  title: string
  prompt: string
  starter_code_py: string
  starter_code_cpp: string
  tests_public_count: number
  created_at: string
}

export interface Submission {
  id: string
  problem_id: string
  language: string
  code: string
  verdict: string
  passed: number
  total: number
  runtime_ms?: number
  memory_kb?: number
  details?: any
  created_at: string
  unlocked_solutions: boolean
}

export interface ChatMessage {
  id: string
  problem_id: string
  user_message: string
  coach_response: string
  code_snippet?: string
  created_at: string
}

export interface Solution {
  python_solution: string
  cpp_solution: string
  explanation: string
  complexity: string
}

// API functions
export const apiClient = {
  // Problems
  async getRandomProblem(category?: string, difficulty?: string): Promise<Problem> {
    const params = new URLSearchParams()
    if (category) params.append('category', category)
    if (difficulty) params.append('difficulty', difficulty)
    
    const response = await api.get(`/problems/random?${params}`)
    return response.data
  },

  async getProblem(problemId: string): Promise<Problem> {
    const response = await api.get(`/problems/${problemId}`)
    return response.data
  },

  async listProblems(category?: string, difficulty?: string, limit = 20, offset = 0): Promise<Problem[]> {
    const params = new URLSearchParams()
    if (category) params.append('category', category)
    if (difficulty) params.append('difficulty', difficulty)
    params.append('limit', limit.toString())
    params.append('offset', offset.toString())
    
    const response = await api.get(`/problems/?${params}`)
    return response.data
  },

  async getCategories(): Promise<string[]> {
    const response = await api.get('/problems/categories/')
    return response.data
  },

  // Submissions
  async submitCode(problemId: string, language: string, code: string): Promise<Submission> {
    const response = await api.post('/submit/', {
      problem_id: problemId,
      language,
      code
    })
    return response.data
  },

  async runCode(problemId: string, language: string, code: string): Promise<any> {
    const response = await api.post('/submit/run', {
      problem_id: problemId,
      language,
      code
    })
    return response.data
  },

  async getSubmission(submissionId: string): Promise<Submission> {
    const response = await api.get(`/submit/${submissionId}`)
    return response.data
  },

  // Chat
  async sendChatMessage(problemId: string, userMessage: string, codeSnippet?: string): Promise<ChatMessage> {
    const response = await api.post('/chat/', {
      problem_id: problemId,
      user_message: userMessage,
      code_snippet: codeSnippet
    })
    return response.data
  },

  async getChatHistory(problemId: string, limit = 50): Promise<ChatMessage[]> {
    const response = await api.get(`/chat/${problemId}/history?limit=${limit}`)
    return response.data
  },

  // Solutions
  async getSolution(problemId: string): Promise<Solution> {
    const response = await api.get(`/solutions/${problemId}`)
    return response.data
  },

  // Feedback
  async generateFeedback(submissionId: string): Promise<any> {
    const response = await api.post('/feedback/', {
      submission_id: submissionId
    })
    return response.data
  },

  async getSubmissionFeedback(problemId: string, language: string, code: string): Promise<any> {
    const response = await api.post('/submit/feedback', {
      problem_id: problemId,
      language,
      code
    })
    return response.data
  }
}

// Extend the api object with the client methods
Object.assign(api, apiClient)
