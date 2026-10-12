import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Adaptive Lightweight NIDS"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Security & JWT
    SECRET_KEY: str = "development-super-secret-cyber-soc-jwt-key-change-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # MongoDB Database Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "nids_db"
    
    # CORS Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "https://*.vercel.app",
        "*"
    ]
    
    # ML & Feature Selection Settings
    SELECTED_FEATURE_COUNT: int = 15
    ANOMALY_THRESHOLD: float = 0.65
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
