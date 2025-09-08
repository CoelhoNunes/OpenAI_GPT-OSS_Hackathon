'use client'

import { useState, useEffect } from 'react'
import { Play, Send, Code2, FileText } from 'lucide-react'
import { Editor as MonacoEditor } from '@monaco-editor/react'
import { useAppStore } from '@/lib/state'
import { apiClient } from '@/lib/api'

export function Editor() {
  const { currentProblem, selectedLanguage, code, setCode, setSelectedLanguage, setCurrentSubmission, setCurrentRunResult } = useAppStore()
  const [isRunning, setIsRunning] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [runOutput, setRunOutput] = useState<any>(null)
  const [showRunOutput, setShowRunOutput] = useState(false)

  // Initialize code when problem changes
  useEffect(() => {
    if (currentProblem) {
      const starterCode = selectedLanguage === 'python' 
        ? currentProblem.starter_code_py 
        : currentProblem.starter_code_cpp
      setCode(starterCode)
    }
  }, [currentProblem, selectedLanguage, setCode])

  const handleLanguageChange = (language: 'python' | 'cpp') => {
    setSelectedLanguage(language)
    if (currentProblem) {
      const starterCode = language === 'python' 
        ? currentProblem.starter_code_py 
        : currentProblem.starter_code_cpp
      setCode(starterCode)
    }
  }

  const handleRun = async () => {
    if (!currentProblem || !code.trim() || isRunning) return

    setIsRunning(true)
    setShowRunOutput(true)
    try {
      const result = await apiClient.runCode(
        currentProblem.problem_id,
        selectedLanguage,
        code
      )
      setRunOutput(result)
      setCurrentRunResult(result)
    } catch (error) {
      console.error('Run failed:', error)
      setRunOutput({
        verdict: 'RUNTIME_ERROR',
        passed: 0,
        total: 0,
        details: { error: 'Failed to run code: ' + (error as Error).message }
      })
    } finally {
      setIsRunning(false)
    }
  }

  const handleSubmit = async () => {
    if (!currentProblem || !code.trim() || isSubmitting) return

    setIsSubmitting(true)
    try {
      const submission = await apiClient.submitCode(
        currentProblem.problem_id,
        selectedLanguage,
        code
      )
      setCurrentSubmission(submission)
    } catch (error) {
      console.error('Submit failed:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const getLanguageIcon = (language: string) => {
    return language === 'python' ? <Code2 className="h-4 w-4" /> : <FileText className="h-4 w-4" />
  }

  if (!currentProblem) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <Code2 className="h-12 w-12 mx-auto mb-4 text-muted-foreground opacity-50" />
          <h3 className="text-lg font-medium text-muted-foreground">
            No problem selected
          </h3>
          <p className="text-sm text-muted-foreground mt-2">
            Select a problem to start coding
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full editor-container">
      {/* Editor Header */}
      <div className="flex items-center justify-between p-4 border-b border-border bg-gradient-to-r from-slate-50 to-blue-50">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold text-slate-700">Language:</span>
            <div className="flex border-2 border-blue-200 rounded-lg overflow-hidden">
              <button
                onClick={() => handleLanguageChange('python')}
                className={`flex items-center gap-2 px-4 py-2 text-sm font-medium transition-all ${
                  selectedLanguage === 'python'
                    ? 'bg-blue-500 text-white shadow-md'
                    : 'bg-white text-slate-700 hover:bg-blue-50'
                }`}
              >
                <Code2 className="h-4 w-4" />
                Python
              </button>
              <button
                onClick={() => handleLanguageChange('cpp')}
                className={`flex items-center gap-2 px-4 py-2 text-sm font-medium border-l-2 border-blue-200 transition-all ${
                  selectedLanguage === 'cpp'
                    ? 'bg-blue-500 text-white shadow-md'
                    : 'bg-white text-slate-700 hover:bg-blue-50'
                }`}
              >
                <FileText className="h-4 w-4" />
                C++
              </button>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <button
            onClick={handleRun}
            disabled={!code.trim() || isRunning}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium border-2 border-green-300 rounded-lg hover:bg-green-50 hover:border-green-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <Play className="h-4 w-4" />
            {isRunning ? 'Running...' : 'Run'}
          </button>
          <button
            onClick={handleSubmit}
            disabled={!code.trim() || isSubmitting}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md"
          >
            <Send className="h-4 w-4" />
            {isSubmitting ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      </div>

      {/* Monaco Editor */}
      <div className="flex-1 relative">
        <MonacoEditor
          height="100%"
          language={selectedLanguage}
          value={code}
          onChange={(value) => setCode(value || '')}
          theme="vs-dark"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            roundedSelection: false,
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            insertSpaces: true,
            wordWrap: 'on',
            folding: true,
            lineDecorationsWidth: 0,
            lineNumbersMinChars: 0,
            renderLineHighlight: 'line',
            scrollbar: {
              vertical: 'auto',
              horizontal: 'auto',
            },
          }}
        />
      </div>

      {/* Run Output Panel */}
      {showRunOutput && runOutput && (
        <div className="border-t border-border bg-gradient-to-r from-slate-50 to-blue-50">
          <div className="p-3 border-b border-border bg-slate-100">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-slate-700">Run Output</h3>
              <button
                onClick={() => setShowRunOutput(false)}
                className="text-slate-500 hover:text-slate-700 text-sm"
              >
                Hide
              </button>
            </div>
          </div>
          <div className="p-4 max-h-48 overflow-y-auto">
            <div className="space-y-3">
              {/* Verdict */}
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-slate-600">Verdict:</span>
                <span className={`px-2 py-1 text-xs font-bold rounded-full ${
                  runOutput.verdict === 'ACCEPTED' ? 'bg-green-100 text-green-800' :
                  runOutput.verdict === 'WRONG_ANSWER' ? 'bg-red-100 text-red-800' :
                  runOutput.verdict === 'RUNTIME_ERROR' ? 'bg-orange-100 text-orange-800' :
                  runOutput.verdict === 'COMPILE_ERROR' ? 'bg-purple-100 text-purple-800' :
                  runOutput.verdict === 'TIMEOUT' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {runOutput.verdict}
                </span>
              </div>

              {/* Test Results */}
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-slate-600">Tests:</span>
                <span className="text-sm text-slate-700">
                  {runOutput.passed}/{runOutput.total} passed
                </span>
              </div>

              {/* Runtime */}
              {runOutput.runtime_ms && (
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-slate-600">Runtime:</span>
                  <span className="text-sm text-slate-700">{runOutput.runtime_ms}ms</span>
                </div>
              )}

              {/* Error Details */}
              {runOutput.details?.error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                  <div className="text-sm font-medium text-red-800 mb-1">Error:</div>
                  <div className="text-sm text-red-700 font-mono">{runOutput.details.error}</div>
                </div>
              )}

              {/* Test Results Details */}
              {runOutput.details?.test_results && runOutput.details.test_results.length > 0 && (
                <div className="space-y-2">
                  <div className="text-sm font-medium text-slate-600">Test Results:</div>
                  {runOutput.details.test_results.map((test: any, index: number) => (
                    <div key={index} className={`p-2 rounded-lg text-sm ${
                      test.status === 'PASS' ? 'bg-green-50 border border-green-200' :
                      test.status === 'FAIL' ? 'bg-red-50 border border-red-200' :
                      'bg-orange-50 border border-orange-200'
                    }`}>
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`px-2 py-1 text-xs font-bold rounded ${
                          test.status === 'PASS' ? 'bg-green-200 text-green-800' :
                          test.status === 'FAIL' ? 'bg-red-200 text-red-800' :
                          'bg-orange-200 text-orange-800'
                        }`}>
                          {test.status}
                        </span>
                        <span className="text-xs text-slate-600">Test {index + 1}</span>
                      </div>
                      {test.status === 'FAIL' && (
                        <div className="text-xs text-slate-600">
                          Expected: <span className="font-mono">{JSON.stringify(test.expected_output)}</span><br/>
                          Got: <span className="font-mono">{JSON.stringify(test.actual_output)}</span>
                        </div>
                      )}
                      {test.error_message && (
                        <div className="text-xs text-red-600 font-mono">{test.error_message}</div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Editor Footer */}
      <div className="p-3 border-t border-border bg-gradient-to-r from-slate-50 to-blue-50 text-xs text-slate-600">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <span className="font-medium">Lines: {code.split('\n').length}</span>
            <span className="font-medium">Characters: {code.length}</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="bg-blue-100 px-2 py-1 rounded text-blue-700">Ctrl+Enter: Run</span>
            <span className="bg-green-100 px-2 py-1 rounded text-green-700">Shift+Enter: Submit</span>
          </div>
        </div>
      </div>
    </div>
  )
}
