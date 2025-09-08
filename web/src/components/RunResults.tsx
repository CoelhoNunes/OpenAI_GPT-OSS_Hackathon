'use client'

import { CheckCircle, XCircle, AlertCircle, Clock, Zap, Play } from 'lucide-react'
import { RunResult } from '@/lib/state'

interface RunResultsProps {
  result: RunResult
}

export function RunResults({ result }: RunResultsProps) {
  const getVerdictIcon = (verdict: string) => {
    switch (verdict) {
      case 'AC':
        return <CheckCircle className="h-5 w-5 text-green-600" />
      case 'WA':
        return <XCircle className="h-5 w-5 text-red-600" />
      case 'TLE':
        return <Clock className="h-5 w-5 text-yellow-600" />
      case 'RE':
      case 'CE':
        return <AlertCircle className="h-5 w-5 text-orange-600" />
      default:
        return <AlertCircle className="h-5 w-5 text-gray-600" />
    }
  }

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case 'AC':
        return 'text-green-600 bg-green-50 border-green-200'
      case 'WA':
        return 'text-red-600 bg-red-50 border-red-200'
      case 'TLE':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'RE':
      case 'CE':
        return 'text-orange-600 bg-orange-50 border-orange-200'
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getVerdictText = (verdict: string) => {
    switch (verdict) {
      case 'AC':
        return 'Accepted'
      case 'WA':
        return 'Wrong Answer'
      case 'TLE':
        return 'Time Limit Exceeded'
      case 'RE':
        return 'Runtime Error'
      case 'CE':
        return 'Compilation Error'
      default:
        return verdict
    }
  }

  const testResults = result.details?.test_results || []

  return (
    <div className="space-y-6">
      {/* Run Summary */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center gap-2 mb-2">
          <Play className="h-5 w-5 text-blue-600" />
          <span className="font-medium text-blue-800">Test Run Results</span>
        </div>
        <p className="text-sm text-blue-700">
          This is a test run. Your code was executed but not submitted.
        </p>
      </div>

      {/* Results Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card border rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            {getVerdictIcon(result.verdict)}
            <span className="font-medium">Verdict</span>
          </div>
          <span className={`px-2 py-1 text-sm font-medium rounded border ${getVerdictColor(result.verdict)}`}>
            {getVerdictText(result.verdict)}
          </span>
        </div>

        <div className="bg-card border rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="h-5 w-5 text-blue-600" />
            <span className="font-medium">Test Cases</span>
          </div>
          <span className="text-lg font-semibold">
            {result.passed} / {result.total}
          </span>
        </div>

        {result.runtime_ms && (
          <div className="bg-card border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-5 w-5 text-purple-600" />
              <span className="font-medium">Runtime</span>
            </div>
            <span className="text-lg font-semibold">
              {result.runtime_ms}ms
            </span>
          </div>
        )}

        {result.memory_kb && (
          <div className="bg-card border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="h-5 w-5 text-indigo-600" />
              <span className="font-medium">Memory</span>
            </div>
            <span className="text-lg font-semibold">
              {result.memory_kb}KB
            </span>
          </div>
        )}
      </div>

      {/* Test Results */}
      {testResults.length > 0 && (
        <div className="bg-card border rounded-lg">
          <div className="p-4 border-b border-border">
            <h3 className="text-lg font-semibold">Test Case Results</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="results-table w-full">
              <thead>
                <tr>
                  <th>Case</th>
                  <th>Status</th>
                  <th>Input</th>
                  <th>Expected</th>
                  <th>Actual</th>
                  <th>Runtime</th>
                </tr>
              </thead>
              <tbody>
                {testResults.map((testResult: any, index: number) => (
                  <tr key={index}>
                    <td className="font-medium">#{index + 1}</td>
                    <td>
                      <span className={`px-2 py-1 text-xs font-medium rounded ${
                        testResult.status === 'PASS' 
                          ? 'text-green-600 bg-green-50' 
                          : testResult.status === 'FAIL'
                          ? 'text-red-600 bg-red-50'
                          : 'text-orange-600 bg-orange-50'
                      }`}>
                        {testResult.status}
                      </span>
                    </td>
                    <td className="font-mono text-xs">
                      {JSON.stringify(testResult.input).slice(0, 50)}
                      {JSON.stringify(testResult.input).length > 50 && '...'}
                    </td>
                    <td className="font-mono text-xs">
                      {JSON.stringify(testResult.expected_output).slice(0, 50)}
                      {JSON.stringify(testResult.expected_output).length > 50 && '...'}
                    </td>
                    <td className="font-mono text-xs">
                      {testResult.actual_output !== undefined 
                        ? JSON.stringify(testResult.actual_output).slice(0, 50)
                        : 'N/A'
                      }
                      {testResult.actual_output !== undefined && JSON.stringify(testResult.actual_output).length > 50 && '...'}
                    </td>
                    <td className="text-xs">
                      {testResult.runtime_ms ? `${testResult.runtime_ms}ms` : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Error Details */}
      {result.details?.compilation_output && (
        <div className="bg-card border rounded-lg">
          <div className="p-4 border-b border-border">
            <h3 className="text-lg font-semibold">Compilation Output</h3>
          </div>
          <div className="p-4">
            <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
              {result.details.compilation_output}
            </pre>
          </div>
        </div>
      )}

      {result.details?.runtime_output && (
        <div className="bg-card border rounded-lg">
          <div className="p-4 border-b border-border">
            <h3 className="text-lg font-semibold">Runtime Output</h3>
          </div>
          <div className="p-4">
            <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
              {result.details.runtime_output}
            </pre>
          </div>
        </div>
      )}

      {result.details?.error && (
        <div className="bg-card border rounded-lg">
          <div className="p-4 border-b border-border">
            <h3 className="text-lg font-semibold">Error</h3>
          </div>
          <div className="p-4">
            <pre className="bg-red-50 text-red-800 p-3 rounded text-sm overflow-x-auto">
              {result.details.error}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
