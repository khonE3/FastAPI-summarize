"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "FastAPI Summarize"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API สำหรับสรุปข้อความด้วย AI"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Model
    MODEL_NAME: str = "facebook/bart-large-cnn"
    MAX_INPUT_LENGTH: int = 1024
    MAX_OUTPUT_LENGTH: int = 150
    MIN_OUTPUT_LENGTH: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()


settings = get_settings()
