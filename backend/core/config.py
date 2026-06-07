import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/almoratab"
    SECRET_KEY: str = "dev-secret-key-change-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    APP_ENV: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __init__(self, **values):
        super().__init__(**values)
        # 1. Automatically inject +asyncpg if missing
        if self.DATABASE_URL.startswith("postgresql://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        # 2. Clean up URL for asyncpg (surgical replacement of sslmode)
        if "sslmode=" in self.DATABASE_URL:
            self.DATABASE_URL = self.DATABASE_URL.replace("sslmode=require", "ssl=true")
            self.DATABASE_URL = self.DATABASE_URL.replace("sslmode=prefer", "ssl=true")
            self.DATABASE_URL = self.DATABASE_URL.replace("sslmode=disable", "ssl=false")
        
        # 3. Ensure ssl=true is present for asyncpg if not already specified
        if "ssl=" not in self.DATABASE_URL:
            separator = "&" if "?" in self.DATABASE_URL else "?"
            self.DATABASE_URL += f"{separator}ssl=true"

settings = Settings()
