#!/usr/bin/env python3
"""
CUDA acceleration server for problem generation.
Provides GPU-accelerated input generation and expected output computation.
"""

import os
import sys
import asyncio
import logging
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request/Response models
class GenerateInputsRequest(BaseModel):
    sizes: List[int] = Field(..., description="Sizes of input arrays to generate")
    seed: int = Field(..., description="Random seed for reproducible generation")

class GenerateInputsResponse(BaseModel):
    inputs: List[List[int]] = Field(..., description="Generated input arrays")
    success: bool = Field(..., description="Whether generation was successful")
    error: Optional[str] = Field(None, description="Error message if generation failed")

class ComputeExpectedRequest(BaseModel):
    inputs: List[List[int]] = Field(..., description="Input arrays")
    problem_type: str = Field(..., description="Type of problem to compute expected outputs for")

class ComputeExpectedResponse(BaseModel):
    expected: List[List[int]] = Field(..., description="Expected output arrays")
    success: bool = Field(..., description="Whether computation was successful")
    error: Optional[str] = Field(None, description="Error message if computation failed")

# Global state
cuda_available = False
cuda_module = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    global cuda_available, cuda_module
    
    # Try to import CUDA module
    try:
        import cuda_accel
        cuda_module = cuda_accel
        cuda_available = True
        logger.info("CUDA acceleration module loaded successfully")
    except ImportError as e:
        logger.warning(f"CUDA acceleration module not available: {e}")
        cuda_available = False
    
    yield
    
    # Cleanup
    logger.info("CUDA acceleration server shutting down")

# Create FastAPI app
app = FastAPI(
    title="CUDA Acceleration Server",
    description="GPU-accelerated problem generation and computation",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "cuda_available": cuda_available,
        "service": "cuda_accel"
    }

@app.post("/generate-inputs", response_model=GenerateInputsResponse)
async def generate_inputs(request: GenerateInputsRequest):
    """Generate test inputs using CUDA acceleration."""
    try:
        if not cuda_available:
            # Fallback to CPU generation
            inputs = []
            for size in request.sizes:
                import random
                random.seed(request.seed)
                inputs.append([random.randint(0, 999) for _ in range(size)])
            
            return GenerateInputsResponse(
                inputs=inputs,
                success=True
            )
        
        # Use CUDA acceleration
        inputs = []
        for size in request.sizes:
            # Generate inputs using CUDA
            result = cuda_module.generate_inputs([size], request.seed)
            inputs.append(result.tolist())
        
        return GenerateInputsResponse(
            inputs=inputs,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error generating inputs: {e}")
        return GenerateInputsResponse(
            inputs=[],
            success=False,
            error=str(e)
        )

@app.post("/compute-expected", response_model=ComputeExpectedResponse)
async def compute_expected(request: ComputeExpectedRequest):
    """Compute expected outputs using CUDA acceleration."""
    try:
        if not cuda_available:
            # Fallback to CPU computation
            expected = []
            for input_array in request.inputs:
                # Placeholder computation
                expected.append([x * 2 for x in input_array])
            
            return ComputeExpectedResponse(
                expected=expected,
                success=True
            )
        
        # Use CUDA acceleration
        expected = []
        for input_array in request.inputs:
            # Compute expected outputs using CUDA
            result = cuda_module.compute_expected(input_array, [0] * len(input_array))
            expected.append(result.tolist())
        
        return ComputeExpectedResponse(
            expected=expected,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error computing expected outputs: {e}")
        return ComputeExpectedResponse(
            expected=[],
            success=False,
            error=str(e)
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8003))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting CUDA acceleration server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)