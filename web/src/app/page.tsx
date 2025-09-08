'use client'

import { useState, useEffect } from 'react'
import { CheckCircle } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ChatCoach } from '@/components/ChatCoach'
import { ProblemCard } from '@/components/ProblemCard'
import { ProblemHeader } from '@/components/ProblemHeader'
import { Editor } from '@/components/Editor'
import { ResultsTable } from '@/components/ResultsTable'
import { RunResults } from '@/components/RunResults'
import { LockNotice } from '@/components/LockNotice'
import { useAppStore } from '@/lib/state'
import { apiClient, Problem, Submission, Solution } from '@/lib/api'

interface SolutionsContentProps {
  currentSubmission: Submission | null
  currentProblem: Problem | null
}

function SolutionsContent({ currentSubmission, currentProblem }: SolutionsContentProps) {
  const [solution, setSolution] = useState<Solution | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (currentSubmission && currentSubmission.unlocked_solutions && currentProblem) {
      loadSolution()
    }
  }, [currentSubmission, currentProblem])

  const loadSolution = async () => {
    if (!currentProblem) return
    
    setLoading(true)
    setError(null)
    try {
      const solutionData = await apiClient.getSolution(currentProblem.problem_id)
      setSolution(solutionData)
    } catch (err) {
      setError('Failed to load solution')
      console.error('Error loading solution:', err)
    } finally {
      setLoading(false)
    }
  }

  if (!currentSubmission || !currentSubmission.unlocked_solutions) {
    return <LockNotice />
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading solution...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <h3 className="text-lg font-medium text-red-600 mb-2">Error</h3>
          <p className="text-muted-foreground">{error}</p>
        </div>
      </div>
    )
  }

  if (!solution) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <h3 className="text-lg font-medium text-muted-foreground">No solution available</h3>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Reference Solutions</h2>
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center gap-2 mb-2">
          <CheckCircle className="h-5 w-5 text-green-600" />
          <span className="font-medium text-green-800">Solutions Unlocked!</span>
        </div>
        <p className="text-sm text-green-700">
          Great job on your submission! Here are the reference solutions and explanations.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="border rounded-lg p-4">
          <h3 className="font-medium mb-2">Python Solution</h3>
          <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
            <code>{solution.python_solution}</code>
          </pre>
        </div>
        <div className="border rounded-lg p-4">
          <h3 className="font-medium mb-2">C++ Solution</h3>
          <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
            <code>{solution.cpp_solution}</code>
          </pre>
        </div>
      </div>
      <div className="border rounded-lg p-4">
        <h3 className="font-medium mb-2">Explanation</h3>
        <p className="text-sm text-muted-foreground">{solution.explanation}</p>
      </div>
      <div className="border rounded-lg p-4">
        <h3 className="font-medium mb-2">Complexity</h3>
        <p className="text-sm text-muted-foreground">{solution.complexity}</p>
      </div>
    </div>
  )
}

export default function HomePage() {
  const { currentProblem, currentSubmission, currentRunResult } = useAppStore()
  const [activeTab, setActiveTab] = useState('problems')
  const [problems, setProblems] = useState<Problem[]>([])

  const generateNewProblems = async () => {
    try {
      // Generate 3 random problems from different categories
      const categories = ['Arrays & Strings', 'Linked List', 'Stack & Queue']
      const problemsData = await Promise.all(
        categories.map(category => apiClient.getRandomProblem(category, 'Easy'))
      )
      setProblems(problemsData)
    } catch (error) {
      console.error('Failed to generate problems:', error)
    }
  }

  useEffect(() => {
    generateNewProblems()
  }, [])

  return (
    <div className="flex h-screen bg-background">
      {/* Left Panel - GPT-OSS Coach */}
      <div className="w-80 border-r border-border bg-card">
        <ChatCoach />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="border-b border-border bg-card p-4">
          <h1 className="text-2xl font-bold text-foreground">
            LeetCoach
          </h1>
          <p className="text-sm text-muted-foreground">
            GPT-OSS Powered Coding Practice with CUDA Acceleration
          </p>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="problems">Problems</TabsTrigger>
            <TabsTrigger value="editor">Editor</TabsTrigger>
            <TabsTrigger value="results">Results</TabsTrigger>
            <TabsTrigger value="solutions">Solutions</TabsTrigger>
          </TabsList>

          {/* Problems Tab */}
          <TabsContent value="problems" className="flex-1 p-4">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold">Practice Problems</h2>
                <button 
                  onClick={generateNewProblems}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
                >
                  Randomize Problem
                </button>
              </div>
              
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {problems.map((problem) => (
                  <ProblemCard
                    key={problem.problem_id}
                    category={problem.category}
                    difficulty={problem.difficulty}
                    title={problem.title}
                    description={problem.prompt}
                    problemId={problem.problem_id}
                  />
                ))}
              </div>
            </div>
          </TabsContent>

          {/* Editor Tab */}
          <TabsContent value="editor" className="flex-1 flex flex-col">
            {currentProblem ? (
              <>
                <ProblemHeader problem={currentProblem} />
                <div className="flex-1 p-4">
                  <Editor />
                </div>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center">
                  <h3 className="text-lg font-medium text-muted-foreground">
                    Select a problem to start coding
                  </h3>
                  <p className="text-sm text-muted-foreground mt-2">
                    Go to the Problems tab to choose a problem
                  </p>
                </div>
              </div>
            )}
          </TabsContent>

          {/* Results Tab */}
          <TabsContent value="results" className="flex-1 p-4">
            {currentRunResult ? (
              <RunResults result={currentRunResult} />
            ) : currentSubmission ? (
              <ResultsTable submission={currentSubmission} />
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <h3 className="text-lg font-medium text-muted-foreground">
                    No results yet
                  </h3>
                  <p className="text-sm text-muted-foreground mt-2">
                    Run your code or submit it to see results
                  </p>
                </div>
              </div>
            )}
          </TabsContent>

          {/* Solutions Tab */}
          <TabsContent value="solutions" className="flex-1 p-4">
            <SolutionsContent 
              currentSubmission={currentSubmission} 
              currentProblem={currentProblem} 
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
