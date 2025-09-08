"""
Solutions router - handles solution retrieval after submission
"""

import uuid
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from src.core.db import get_db
from src.core.schemas import SolutionResponse, Problem, Submission

router = APIRouter()


@router.get("/{problem_id}", response_model=SolutionResponse)
async def get_solution(
    problem_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> SolutionResponse:
    """Get solution for a problem (only after first submission)."""
    
    # Check if user has made at least one submission
    result = await db.execute(
        select(Submission).where(Submission.problem_id == problem_id).limit(1)
    )
    submission = result.scalar_one_or_none()
    
    if not submission:
        raise HTTPException(
            status_code=403,
            detail="Solutions are locked until you make your first submission"
        )
    
    # Get problem details
    result = await db.execute(
        select(Problem).where(Problem.problem_id == problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Load solution from file system
    from src.services.solutions_store import SolutionsStore
    
    solutions_store = SolutionsStore()
    try:
        solution_data = await solutions_store.get_solution(
            problem.template_slug,
            problem.seed
        )
        
        return SolutionResponse(
            python_solution=solution_data["python_solution"],
            cpp_solution=solution_data["cpp_solution"],
            explanation=solution_data["explanation"],
            complexity=solution_data["complexity"]
        )
        
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Solution not found for this problem instance"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading solution: {str(e)}"
        )
