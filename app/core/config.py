from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings): 
    APP_NAME: str = "FastAPI Project"
    DEBUG: bool 
 
    API_V1_STR: str = "/api/v1"
 
    SECRET_KEY: str  
    ALGORITHM: str 
   
    ACCESS_TOKEN_EXPIRE_MINUTES: int  
    REFRESH_TOKEN_EXPIRE_DAYS: int  
 
    BACKEND_CORS_ORIGINS: List[str]  
    DATABASE_URL : str
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
