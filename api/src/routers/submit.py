"""
Submit router - handles code submission and execution
"""

import uuid
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.db import get_db
from src.core.schemas import SubmissionCreate, SubmissionResponse, Problem
from src.services.judge import JudgeService

router = APIRouter()


@router.post("/", response_model=SubmissionResponse)
async def submit_code(
    submission: SubmissionCreate,
    db: AsyncSession = Depends(get_db)
) -> SubmissionResponse:
    """Submit code for execution and judging."""
    
    # Validate problem exists
    result = await db.execute(
        select(Problem).where(Problem.problem_id == submission.problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Validate language
    if submission.language not in ["python", "cpp"]:
        raise HTTPException(
            status_code=400,
            detail="Language must be 'python' or 'cpp'"
        )
    
    # Create submission record
    from src.core.schemas import Submission
    db_submission = Submission(
        problem_id=submission.problem_id,
        language=submission.language,
        code=submission.code,
        verdict="RUNTIME_ERROR",  # Start with RUNTIME_ERROR, will be updated after judging
        passed=0,
        total=0
    )
    
    db.add(db_submission)
    await db.commit()
    await db.refresh(db_submission)
    
    try:
        # Judge the submission
        judge_service = JudgeService()
        result = await judge_service.judge_submission(
            problem=problem,
            code=submission.code,
            language=submission.language,
            is_test_run=False
        )
        
        # Update submission with results
        db_submission.verdict = result["verdict"]
        db_submission.passed = result["passed"]
        db_submission.total = result["total"]
        db_submission.runtime_ms = result.get("runtime_ms")
        db_submission.memory_kb = result.get("memory_kb")
        db_submission.details = result.get("details")
        
        await db.commit()
        await db.refresh(db_submission)
        
        # Check if solutions should be unlocked
        unlocked_solutions = db_submission.verdict in ["ACCEPTED", "WRONG_ANSWER", "TIMEOUT", "RUNTIME_ERROR"]
        
        return SubmissionResponse(
            id=db_submission.id,
            problem_id=db_submission.problem_id,
            language=db_submission.language,
            code=db_submission.code,
            verdict=db_submission.verdict,
            passed=db_submission.passed,
            total=db_submission.total,
            runtime_ms=db_submission.runtime_ms,
            memory_kb=db_submission.memory_kb,
            details=db_submission.details,
            created_at=db_submission.created_at,
            unlocked_solutions=unlocked_solutions
        )
        
    except Exception as e:
        # Update submission with error
        db_submission.verdict = "RUNTIME_ERROR"
        db_submission.details = {"error": str(e)}
        
        await db.commit()
        await db.refresh(db_submission)
        
        raise HTTPException(
            status_code=500,
            detail=f"Submission failed: {str(e)}"
        )


@router.post("/run", response_model=Dict[str, Any])
async def run_code(
    submission: SubmissionCreate,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Run code without saving submission (for testing)."""
    
    # Validate problem exists
    result = await db.execute(
        select(Problem).where(Problem.problem_id == submission.problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Validate language
    if submission.language not in ["python", "cpp"]:
        raise HTTPException(
            status_code=400,
            detail="Language must be 'python' or 'cpp'"
        )
    
    try:
        # Judge the submission (without saving to DB)
        judge_service = JudgeService()
        result = await judge_service.judge_submission(
            problem=problem,
            code=submission.code,
            language=submission.language,
            is_test_run=True
        )
        
        return {
            "verdict": result["verdict"],
            "passed": result["passed"],
            "total": result["total"],
            "runtime_ms": result.get("runtime_ms"),
            "memory_kb": result.get("memory_kb"),
            "details": result.get("details"),
            "is_test_run": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Code execution failed: {str(e)}"
        )


@router.post("/feedback", response_model=Dict[str, Any])
async def get_submission_feedback(
    submission: SubmissionCreate,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Get AI feedback on a code submission."""
    
    # Validate problem exists
    result = await db.execute(
        select(Problem).where(Problem.problem_id == submission.problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Validate language
    if submission.language not in ["python", "cpp"]:
        raise HTTPException(
            status_code=400,
            detail="Language must be 'python' or 'cpp'"
        )
    
    try:
        # Judge the submission to get test results
        judge_service = JudgeService()
        test_results = await judge_service.judge_submission(
            problem=problem,
            code=submission.code,
            language=submission.language,
            is_test_run=False  # Use all tests for feedback
        )
        
        # Get AI feedback
        from src.services.gpt_coach import GPTCoachService
        coach_service = GPTCoachService()
        try:
            feedback = await coach_service.get_submission_feedback(
                problem_context=f"{problem.title}: {problem.prompt}",
                test_results=test_results,
                code_snippet=submission.code
            )
        finally:
            await coach_service.close()
        
        return {
            "feedback": feedback,
            "test_results": test_results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate feedback: {str(e)}"
        )


@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> SubmissionResponse:
    """Get a specific submission by ID."""
    
    from src.core.schemas import Submission
    
    result = await db.execute(
        select(Submission).where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Check if solutions should be unlocked
    unlocked_solutions = submission.verdict in ["ACCEPTED", "WRONG_ANSWER", "TIMEOUT", "RUNTIME_ERROR"]
    
    return SubmissionResponse(
        id=submission.id,
        problem_id=submission.problem_id,
        language=submission.language,
        code=submission.code,
        verdict=submission.verdict,
        passed=submission.passed,
        total=submission.total,
        runtime_ms=submission.runtime_ms,
        memory_kb=submission.memory_kb,
        details=submission.details,
        created_at=submission.created_at,
        unlocked_solutions=unlocked_solutions
    )
