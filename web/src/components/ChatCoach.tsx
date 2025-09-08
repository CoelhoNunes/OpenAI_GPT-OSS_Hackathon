'use client'

import { useState, useEffect, useRef } from 'react'
import { Send, Bot, User } from 'lucide-react'
import { useAppStore } from '@/lib/state'
import { apiClient } from '@/lib/api'

export function ChatCoach() {
  const { currentProblem, chatMessages, addChatMessage, code } = useAppStore()
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chatMessages])

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading) return

    const userMessage = message.trim()
    setMessage('')
    setIsLoading(true)

    try {
      if (currentProblem) {
        // Send to API if problem is selected
        const response = await apiClient.sendChatMessage(
          currentProblem.problem_id,
          userMessage,
          code // Pass current code to coach for context
        )
        addChatMessage(response)
      } else {
        // Provide fallback response when no problem is selected
        const fallbackResponse = {
          id: Date.now().toString(),
          problem_id: 'general',
          user_message: userMessage,
          coach_response: `I'd be happy to help you with coding questions! However, I work best when you have a specific problem selected. 

Here are some general tips:
- Select a problem from the Problems tab to get contextual help
- I can help with problem understanding, approach strategies, and debugging
- I provide hints and guidance without giving away complete solutions

What would you like to work on?`,
          created_at: new Date().toISOString()
        }
        addChatMessage(fallbackResponse)
      }
    } catch (error) {
      console.error('Failed to send message:', error)
      // Add error message to chat
      addChatMessage({
        id: Date.now().toString(),
        problem_id: currentProblem?.problem_id || 'general',
        user_message: userMessage,
        coach_response: 'Sorry, I encountered an error. Please try again.',
        created_at: new Date().toISOString()
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-2">
          <Bot className="h-5 w-5 text-primary" />
          <h2 className="font-semibold">GPT-OSS Coach</h2>
        </div>
        <p className="text-xs text-muted-foreground mt-1">
          Ask for hints, strategy, or complexity analysis
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {!currentProblem ? (
          <div className="text-center text-muted-foreground">
            <Bot className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">Select a problem to start chatting with the coach</p>
          </div>
        ) : chatMessages.length === 0 ? (
          <div className="text-center text-muted-foreground">
            <Bot className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">Ask me anything about this problem!</p>
            <div className="mt-4 space-y-2 text-xs">
              <p>💡 "What's the best approach for this problem?"</p>
              <p>🔍 "What edge cases should I consider?"</p>
              <p>⚡ "What's the time complexity of this approach?"</p>
            </div>
          </div>
        ) : (
          chatMessages.map((msg) => (
            <div key={msg.id} className="space-y-2">
              {/* User message */}
              <div className="flex items-start gap-2">
                <User className="h-4 w-4 mt-1 text-primary" />
                <div className="bg-primary/10 rounded-lg p-2 max-w-[80%]">
                  <p className="text-sm">{msg.user_message}</p>
                </div>
              </div>
              
              {/* Coach response */}
              <div className="flex items-start gap-2">
                <Bot className="h-4 w-4 mt-1 text-muted-foreground" />
                <div className="bg-muted rounded-lg p-2 max-w-[80%]">
                  <p className="text-sm whitespace-pre-wrap">{msg.coach_response}</p>
                </div>
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="flex items-start gap-2">
            <Bot className="h-4 w-4 mt-1 text-muted-foreground" />
            <div className="bg-muted rounded-lg p-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-border">
        <div className="flex gap-2">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask the coach..."
            disabled={isLoading}
            className="flex-1 min-h-[40px] max-h-[120px] p-2 border border-border rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
          />
          <button
            onClick={handleSendMessage}
            disabled={!message.trim() || isLoading}
            className="px-3 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <p className="text-xs text-muted-foreground mt-2">
          Press Enter to send, Shift+Enter for new line
        </p>
      </div>
    </div>
  )
}
