"""
Database models and Pydantic schemas
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String, Text, JSON, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.db import Base


# Database Models
class Problem(Base):
    """Problem model."""
    __tablename__ = "problems"
    
    problem_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(50), nullable=False)
    template_slug = Column(String(100), nullable=False)
    seed = Column(Integer, nullable=False)
    difficulty = Column(String(10), nullable=False)
    title = Column(String(200), nullable=False)
    prompt = Column(Text, nullable=False)
    starter_code_py = Column(Text, nullable=False)
    starter_code_cpp = Column(Text, nullable=False)
    tests_public_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="problem", cascade="all, delete-orphan")


class Submission(Base):
    """Submission model."""
    __tablename__ = "submissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.problem_id"), nullable=False)
    language = Column(String(10), nullable=False)
    code = Column(Text, nullable=False)
    verdict = Column(String(10), nullable=False)
    passed = Column(Integer, nullable=False, default=0)
    total = Column(Integer, nullable=False, default=0)
    runtime_ms = Column(Integer)
    memory_kb = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    problem = relationship("Problem", back_populates="submissions")
    feedback = relationship("Feedback", back_populates="submission", cascade="all, delete-orphan")


class ChatMessage(Base):
    """Chat message model."""
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.problem_id"), nullable=False)
    user_message = Column(Text, nullable=False)
    coach_response = Column(Text, nullable=False)
    code_snippet = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    problem = relationship("Problem", back_populates="chat_messages")


class Feedback(Base):
    """Feedback model."""
    __tablename__ = "feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submissions.id"), nullable=False)
    summary_bullets = Column(ARRAY(Text))
    suggested_improvements = Column(ARRAY(Text))
    complexity_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    submission = relationship("Submission", back_populates="feedback")


# Pydantic Schemas
class ProblemBase(BaseModel):
    """Base problem schema."""
    category: str
    template_slug: str
    seed: int
    difficulty: str
    title: str
    prompt: str
    starter_code_py: str
    starter_code_cpp: str
    tests_public_count: int = 0


class ProblemCreate(ProblemBase):
    """Problem creation schema."""
    pass


class ProblemResponse(ProblemBase):
    """Problem response schema."""
    problem_id: uuid.UUID
    created_at: datetime
    
    model_config = {"from_attributes": True}


class SubmissionBase(BaseModel):
    """Base submission schema."""
    language: str
    code: str


class SubmissionCreate(SubmissionBase):
    """Submission creation schema."""
    problem_id: uuid.UUID


class SubmissionResponse(SubmissionBase):
    """Submission response schema."""
    id: uuid.UUID
    problem_id: uuid.UUID
    verdict: str
    passed: int
    total: int
    runtime_ms: Optional[int] = None
    memory_kb: Optional[int] = None
    details: Optional[Dict[str, Any]] = None
    created_at: datetime
    unlocked_solutions: bool = False
    
    model_config = {"from_attributes": True}


class ChatMessageBase(BaseModel):
    """Base chat message schema."""
    user_message: str
    code_snippet: Optional[str] = None


class ChatMessageCreate(ChatMessageBase):
    """Chat message creation schema."""
    problem_id: uuid.UUID


class ChatMessageResponse(ChatMessageBase):
    """Chat message response schema."""
    id: uuid.UUID
    problem_id: uuid.UUID
    coach_response: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


class FeedbackBase(BaseModel):
    """Base feedback schema."""
    summary_bullets: List[str]
    suggested_improvements: List[str]
    complexity_notes: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    """Feedback creation schema."""
    submission_id: uuid.UUID


class FeedbackResponse(FeedbackBase):
    """Feedback response schema."""
    id: uuid.UUID
    submission_id: uuid.UUID
    created_at: datetime
    
    model_config = {"from_attributes": True}


class TestCase(BaseModel):
    """Test case schema."""
    input: Dict[str, Any]
    expected_output: Any
    description: Optional[str] = None
    is_public: bool = True


class ProblemWithTests(ProblemResponse):
    """Problem with test cases schema."""
    test_cases: List[TestCase]


class SolutionResponse(BaseModel):
    """Solution response schema."""
    python_solution: str
    cpp_solution: str
    explanation: str
    complexity: str
