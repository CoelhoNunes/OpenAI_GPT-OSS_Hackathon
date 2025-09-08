"""
Problems router - handles problem generation and retrieval
"""

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.db import get_db
from src.core.schemas import ProblemResponse, ProblemWithTests
from src.services.problem_gen.registry import registry
from src.services.problem_gen.utils import generate_test_cases

router = APIRouter()


@router.get("/random", response_model=ProblemWithTests)
async def get_random_problem(
    category: Optional[str] = Query(None, description="Problem category filter"),
    difficulty: Optional[str] = Query(None, description="Difficulty filter (Easy, Medium, Hard)"),
    db: AsyncSession = Depends(get_db)
) -> ProblemWithTests:
    """Get a random problem with test cases."""
    
    # Get available categories
    available_categories = registry.get_categories()
    
    # Validate category
    if category and category not in available_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Available: {available_categories}"
        )
    
    # Validate difficulty
    valid_difficulties = ["Easy", "Medium", "Hard"]
    if difficulty and difficulty not in valid_difficulties:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid difficulty. Available: {valid_difficulties}"
        )
    
    # Select category if not specified
    if not category:
        import random
        category = random.choice(available_categories)
    
    # Select difficulty if not specified
    if not difficulty:
        import random
        difficulty = random.choice(valid_difficulties)
    
    # Get available templates for category
    templates = registry.get_templates(category)
    
    # Generate random seed and template
    import random
    seed = random.randint(1, 1000000)
    template = random.choice(templates)
    
    # Generate problem and test cases
    problem_create, test_cases = registry.generate_problem(category, template, seed, difficulty)
    
    # Save problem to database
    from src.core.schemas import Problem
    problem = Problem(**problem_create.dict())
    db.add(problem)
    await db.commit()
    await db.refresh(problem)
    
    # Convert to response format
    problem_response = ProblemResponse.model_validate(problem)
    
    return ProblemWithTests(
        **problem_response.model_dump(),
        test_cases=test_cases
    )


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
    problem_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> ProblemResponse:
    """Get a specific problem by ID."""
    
    from src.core.schemas import Problem
    
    result = await db.execute(
        select(Problem).where(Problem.problem_id == problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    return ProblemResponse.model_validate(problem)


@router.get("/", response_model=List[ProblemResponse])
async def list_problems(
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    limit: int = Query(20, ge=1, le=100, description="Number of problems to return"),
    offset: int = Query(0, ge=0, description="Number of problems to skip"),
    db: AsyncSession = Depends(get_db)
) -> List[ProblemResponse]:
    """List problems with optional filtering."""
    
    from src.core.schemas import Problem
    
    query = select(Problem)
    
    if category:
        query = query.where(Problem.category == category)
    
    if difficulty:
        query = query.where(Problem.difficulty == difficulty)
    
    query = query.offset(offset).limit(limit).order_by(Problem.created_at.desc())
    
    result = await db.execute(query)
    problems = result.scalars().all()
    
    return [ProblemResponse.model_validate(problem) for problem in problems]


@router.get("/categories/", response_model=List[str])
async def get_categories() -> List[str]:
    """Get all available problem categories."""
    return registry.get_categories()


@router.get("/categories/{category}/templates/", response_model=List[str])
async def get_templates(category: str) -> List[str]:
    """Get available templates for a category."""
    try:
        return registry.get_templates(category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
