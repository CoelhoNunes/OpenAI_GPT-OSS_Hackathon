"""
Configuration settings for LeetCoach API
"""

import os
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str = "postgresql://leetcoach:leetcoach123@localhost:5432/leetcoach"

    # Model Configuration (GPT-OSS local only)
    MODEL_ID: str = "openai/gpt-oss-20b"
    HF_ID: str = "openai/gpt-oss-20b"
    WEIGHTS_PATH: str = ""
    TORCH_DTYPE: str = "bfloat16"
    MAX_TOKENS: int = 512
    CONTEXT_LEN: int = 8192
    GPU_MEMORY_FRACTION: float = 0.9
    BATCH_SIZE: int = 1
    ALLOW_NON_GPT_OSS: bool = False

    # vLLM Configuration (local-only, no external endpoints)
    VLLM_BASE_URL: str = "http://vllm:8000"

    # CUDA Acceleration
    CUDA_ACCEL_URL: str = "http://cuda_accel:8001"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # Runner Configuration
    RUNNER_URL: str = "http://runner:8002"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Coach Configuration
    MAX_COACH_RESPONSE_LENGTH: int = 200  # Max tokens for generation
    MAX_CODE_SNIPPET_LINES: int = 6
    
    @field_validator("ALLOW_NON_GPT_OSS")
    @classmethod
    def validate_gpt_oss_only(cls, v) -> bool:
        """Ensure only GPT-OSS models are allowed."""
        # Convert string to boolean if needed
        if isinstance(v, str):
            v = v.lower() in ('true', '1', 'yes', 'on')
        
        # Only allow GPT-OSS (ALLOW_NON_GPT_OSS must remain False)
        if v:
            raise ValueError("Only GPT-OSS models are allowed")
        return v
    
    model_config = {"env_file": ".env", "case_sensitive": True}


# Global settings instance
settings = Settings()
