import os
from urllib.parse import urlparse, urlunparse
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/almoratab"
    SECRET_KEY: str = "dev-secret-key-change-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    APP_ENV: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"
    # Comma-separated string so it's easy to set in env vars (e.g. HuggingFace Spaces)
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse ALLOWED_ORIGINS comma-separated string into a list."""
        origins = [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]
        if self.FRONTEND_URL and self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)
        return origins

    def __init__(self, **values):
        super().__init__(**values)
        self.DATABASE_URL = self._process_db_url(self.DATABASE_URL)

    def _process_db_url(self, url: str) -> str:
        # 1. Ensure scheme is correct for asyncpg
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

        try:
            parsed = urlparse(url)

            # 2. Strip ALL query parameters — we pass ssl/cache settings
            # explicitly in core/database.py via connect_args.
            parsed = parsed._replace(query="")

            # 3. Clean up environment for asyncpg
            if "PGSSLMODE" in os.environ:
                val = os.environ["PGSSLMODE"]
                valid_sslmodes = ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"]
                if val not in valid_sslmodes:
                    os.environ["PGSSLMODE"] = "require"

            return urlunparse(parsed)

        except Exception:
            return url

settings = Settings()
