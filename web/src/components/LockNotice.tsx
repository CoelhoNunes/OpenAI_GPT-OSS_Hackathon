'use client'

import { Lock, CheckCircle } from 'lucide-react'

export function LockNotice() {
  return (
    <div className="flex items-center justify-center h-full">
      <div className="text-center max-w-md">
        <div className="mb-6">
          <Lock className="h-16 w-16 mx-auto text-muted-foreground opacity-50" />
        </div>
        
        <h3 className="text-xl font-semibold text-foreground mb-3">
          Solutions Locked
        </h3>
        
        <p className="text-muted-foreground mb-6">
          Solutions are locked until you make your first submission. This encourages you to think through the problem yourself first.
        </p>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="h-5 w-5 text-blue-600" />
            <span className="font-medium text-blue-800">How to unlock solutions:</span>
          </div>
          <div className="text-sm text-blue-700 space-y-1">
            <p>1. Go to the Editor tab</p>
            <p>2. Write your solution in Python or C++</p>
            <p>3. Click Submit to run your code</p>
            <p>4. Solutions will unlock after your first submission</p>
          </div>
        </div>
        
        <div className="text-sm text-muted-foreground">
          <p className="mb-2">💡 <strong>Tip:</strong> Don't worry about getting it right the first time!</p>
          <p>The goal is to learn and improve. Even a wrong submission helps you understand the problem better.</p>
        </div>
      </div>
    </div>
  )
}