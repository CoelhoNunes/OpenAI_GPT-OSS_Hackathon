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
    
    # Model Configuration (hard-pinned to vLLM + GPT-OSS only)
    GPT_OSS_MODEL: str = "openai/gpt-oss-20b"
    ALLOW_NON_GPT_OSS: bool = False
    
    # vLLM Configuration
    VLLM_BASE_URL: str = "http://vllm:8000"
    
    # Hugging Face Configuration (optional)
    HF_TOKEN: str = ""
    
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
        
        # Only allow GPT-OSS with vLLM path (ALLOW_NON_GPT_OSS should be False)
        if v:
            raise ValueError("Only GPT-OSS models are allowed")
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# Global settings instance
settings = Settings()
