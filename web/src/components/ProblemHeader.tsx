'use client'

import { Clock, Target, Code, FileText } from 'lucide-react'
import { Problem } from '@/lib/state'

interface ProblemHeaderProps {
  problem: Problem
}

export function ProblemHeader({ problem }: ProblemHeaderProps) {
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

  return (
    <div className="border-b border-border bg-card p-4">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-2xl font-bold text-foreground">{problem.title}</h1>
            <span className={`px-3 py-1 text-sm font-medium rounded border ${getDifficultyColor(problem.difficulty)}`}>
              {problem.difficulty}
            </span>
          </div>
          
          <div className="flex items-center gap-4 text-sm text-muted-foreground mb-3">
            <div className="flex items-center gap-1">
              <Code className="h-4 w-4" />
              <span>{problem.category}</span>
            </div>
            <div className="flex items-center gap-1">
              <Target className="h-4 w-4" />
              <span>{problem.tests_public_count} test cases</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span>2s time limit</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="prose prose-sm max-w-none">
        <div className="whitespace-pre-wrap text-foreground leading-relaxed">
          {problem.prompt}
        </div>
      </div>
    </div>
  )
}