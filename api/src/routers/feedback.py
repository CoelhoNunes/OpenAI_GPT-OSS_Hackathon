"""
Feedback router - handles post-submission feedback generation
"""

import uuid
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.db import get_db
from src.core.schemas import FeedbackCreate, FeedbackResponse, Submission
from src.services.feedback import FeedbackService

router = APIRouter()


@router.post("/", response_model=FeedbackResponse)
async def generate_feedback(
    feedback_data: FeedbackCreate,
    db: AsyncSession = Depends(get_db)
) -> FeedbackResponse:
    """Generate feedback for a submission."""
    
    # Validate submission exists
    result = await db.execute(
        select(Submission).where(Submission.id == feedback_data.submission_id)
    )
    submission = result.scalar_one_or_none()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Generate feedback using GPT-OSS
    feedback_service = FeedbackService()
    try:
        feedback_result = await feedback_service.generate_feedback(
            code=submission.code,
            language=submission.language,
            problem_id=submission.problem_id,
            verdict=submission.verdict,
            results=submission.details
        )
        
        # Create feedback record
        from src.core.schemas import Feedback
        feedback = Feedback(
            submission_id=feedback_data.submission_id,
            summary_bullets=feedback_result["summary_bullets"],
            suggested_improvements=feedback_result["suggested_improvements"],
            complexity_notes=feedback_result["complexity_notes"]
        )
        
        db.add(feedback)
        await db.commit()
        await db.refresh(feedback)
        
        return FeedbackResponse.model_validate(feedback)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating feedback: {str(e)}"
        )
    finally:
        await feedback_service.close()


@router.get("/{submission_id}", response_model=FeedbackResponse)
async def get_feedback(
    submission_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> FeedbackResponse:
    """Get feedback for a submission."""
    
    from src.core.schemas import Feedback
    
    result = await db.execute(
        select(Feedback).where(Feedback.submission_id == submission_id)
    )
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return FeedbackResponse.model_validate(feedback)
