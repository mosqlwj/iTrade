from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "宏观经济指标分析平台"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./itrade.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # CORS
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # Data cache
    cache_ttl: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
