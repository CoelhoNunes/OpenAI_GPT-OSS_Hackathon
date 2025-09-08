-- LeetCoach Database Schema
-- PostgreSQL initialization script

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Problems table
CREATE TABLE IF NOT EXISTS problems (
    problem_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(50) NOT NULL,
    template_slug VARCHAR(100) NOT NULL,
    seed INTEGER NOT NULL,
    difficulty VARCHAR(10) NOT NULL CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
    title VARCHAR(200) NOT NULL,
    prompt TEXT NOT NULL,
    starter_code_py TEXT NOT NULL,
    starter_code_cpp TEXT NOT NULL,
    tests_public_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    problem_id UUID NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    language VARCHAR(10) NOT NULL CHECK (language IN ('python', 'cpp')),
    code TEXT NOT NULL,
    verdict VARCHAR(10) NOT NULL CHECK (verdict IN ('AC', 'WA', 'TLE', 'RE', 'CE')),
    passed INTEGER NOT NULL DEFAULT 0,
    total INTEGER NOT NULL DEFAULT 0,
    runtime_ms INTEGER,
    memory_kb INTEGER,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Chat messages table (for coach conversations)
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    problem_id UUID NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    user_message TEXT NOT NULL,
    coach_response TEXT NOT NULL,
    code_snippet TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    submission_id UUID NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    summary_bullets TEXT[],
    suggested_improvements TEXT[],
    complexity_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_problems_category ON problems(category);
CREATE INDEX IF NOT EXISTS idx_problems_difficulty ON problems(difficulty);
CREATE INDEX IF NOT EXISTS idx_problems_template ON problems(template_slug);
CREATE INDEX IF NOT EXISTS idx_submissions_problem ON submissions(problem_id);
CREATE INDEX IF NOT EXISTS idx_submissions_created ON submissions(created_at);
CREATE INDEX IF NOT EXISTS idx_chat_problem ON chat_messages(problem_id);
CREATE INDEX IF NOT EXISTS idx_feedback_submission ON feedback(submission_id);

-- Insert some sample problems for testing
INSERT INTO problems (category, template_slug, seed, difficulty, title, prompt, starter_code_py, starter_code_cpp, tests_public_count) VALUES
('Arrays & Strings', 'two_sum', 12345, 'Easy', 'Two Sum', 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.', 'def twoSum(nums, target):\n    # Your code here\n    pass', 'class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Your code here\n    }\n};', 3),
('Linked List', 'reverse_list', 67890, 'Easy', 'Reverse Linked List', 'Given the head of a singly linked list, reverse the list and return the reversed list.', 'def reverseList(head):\n    # Your code here\n    pass', 'class Solution {\npublic:\n    ListNode* reverseList(ListNode* head) {\n        // Your code here\n    }\n};', 2),
('Stack & Queue', 'valid_parentheses', 11111, 'Easy', 'Valid Parentheses', 'Given a string s containing just the characters ''('', '')'', ''{'', ''}'', ''['' and '']'', determine if the input string is valid.', 'def isValid(s):\n    # Your code here\n    pass', 'class Solution {\npublic:\n    bool isValid(string s) {\n        // Your code here\n    }\n};', 4);
