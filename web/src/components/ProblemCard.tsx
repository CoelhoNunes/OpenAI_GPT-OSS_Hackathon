'use client'

import { useState } from 'react'
import { Clock, Target, Code } from 'lucide-react'
import { useAppStore } from '@/lib/state'
import { apiClient } from '@/lib/api'

interface ProblemCardProps {
  category: string
  difficulty: string
  title: string
  description: string
  problemId?: string
}

export function ProblemCard({ category, difficulty, title, description, problemId }: ProblemCardProps) {
  const { setCurrentProblem } = useAppStore()
  const [isSelected, setIsSelected] = useState(false)

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'text-green-600 bg-green-50 border-green-200'
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'hard':
        return 'text-red-600 bg-red-50 border-red-200'
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const handleSelect = async () => {
    setIsSelected(true)
    if (problemId) {
      try {
        // Fetch the full problem data from the API
        const fullProblem = await apiClient.getProblem(problemId)
        setCurrentProblem(fullProblem)
      } catch (error) {
        console.error('Failed to fetch problem:', error)
        // Fallback to mock data if API fails
        const mockProblem = {
          problem_id: problemId,
          category,
          template_slug: 'mock-template',
          seed: 12345,
          difficulty,
          title,
          prompt: description,
          starter_code_py: `def ${title.toLowerCase().replace(/\s+/g, '_')}():\n    # Your code here\n    pass`,
          starter_code_cpp: `class Solution {\npublic:\n    // Your code here\n};`,
          tests_public_count: 3,
          created_at: new Date().toISOString()
        }
        setCurrentProblem(mockProblem)
      }
    }
  }

  return (
    <div
      className={`
        relative p-4 bg-card border-2 rounded-xl cursor-pointer transition-all duration-200 
        hover:shadow-lg hover:scale-[1.02] hover:border-blue-400 hover:bg-blue-50/50
        ${isSelected 
          ? 'border-blue-500 bg-blue-50 shadow-md ring-2 ring-blue-200' 
          : 'border-blue-200 hover:border-blue-400'
        }
        group
      `}
      onClick={handleSelect}
    >
      {/* Clickable indicator */}
      <div className="absolute top-2 right-2 w-3 h-3 rounded-full bg-blue-400 opacity-60 group-hover:opacity-100 transition-opacity"></div>
      
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-foreground text-lg group-hover:text-blue-700 transition-colors">
          {title}
        </h3>
        <span className={`px-3 py-1 text-xs font-bold rounded-full border-2 ${getDifficultyColor(difficulty)}`}>
          {difficulty}
        </span>
      </div>
      
      <p className="text-sm text-muted-foreground mb-4 line-clamp-2 leading-relaxed">
        {description}
      </p>
      
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <div className="flex items-center gap-2 bg-blue-100 px-2 py-1 rounded-md">
          <Code className="h-3 w-3 text-blue-600" />
          <span className="font-medium text-blue-700">{category}</span>
        </div>
        <div className="flex items-center gap-2 bg-green-100 px-2 py-1 rounded-md">
          <Target className="h-3 w-3 text-green-600" />
          <span className="font-medium text-green-700">3 test cases</span>
        </div>
      </div>
    </div>
  )
}
