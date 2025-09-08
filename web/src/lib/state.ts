import { create } from 'zustand'

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

export interface RunResult {
  verdict: string
  passed: number
  total: number
  runtime_ms?: number
  memory_kb?: number
  details?: any
  is_test_run: boolean
}

export interface ChatMessage {
  id: string
  problem_id: string
  user_message: string
  coach_response: string
  code_snippet?: string
  created_at: string
}

interface AppState {
  currentProblem: Problem | null
  currentSubmission: Submission | null
  currentRunResult: RunResult | null
  chatMessages: ChatMessage[]
  selectedLanguage: 'python' | 'cpp'
  code: string
  
  // Actions
  setCurrentProblem: (problem: Problem | null) => void
  setCurrentSubmission: (submission: Submission | null) => void
  setCurrentRunResult: (result: RunResult | null) => void
  addChatMessage: (message: ChatMessage) => void
  setSelectedLanguage: (language: 'python' | 'cpp') => void
  setCode: (code: string) => void
  clearChat: () => void
}

export const useAppStore = create<AppState>((set) => ({
  currentProblem: null,
  currentSubmission: null,
  currentRunResult: null,
  chatMessages: [],
  selectedLanguage: 'python',
  code: '',
  
  setCurrentProblem: (problem) => set({ currentProblem: problem }),
  setCurrentSubmission: (submission) => set({ currentSubmission: submission }),
  setCurrentRunResult: (result) => set({ currentRunResult: result }),
  addChatMessage: (message) => set((state) => ({ 
    chatMessages: [...state.chatMessages, message] 
  })),
  setSelectedLanguage: (language) => set({ selectedLanguage: language }),
  setCode: (code) => set({ code }),
  clearChat: () => set({ chatMessages: [] }),
}))
