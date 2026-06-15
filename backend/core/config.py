import os
import socket
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
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def __init__(self, **values):
        super().__init__(**values)
        self.DATABASE_URL = self._process_db_url(self.DATABASE_URL)

    def _process_db_url(self, url: str) -> str:
        # 1. Ensure scheme is correct
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        
        try:
            parsed = urlparse(url)
            
            # 2. Aggressively strip ALL query parameters
            # We will pass necessary parameters (like ssl and statement_cache_size) 
            # explicitly in core/database.py via connect_args. 
            # This prevents any 'sslmode' or other incompatible strings from reaching asyncpg.
            parsed = parsed._replace(query="")
            
            # 3. Handle IPv4 Resolution
            hostname = parsed.hostname
            if hostname:
                try:
                    ipv4_address = socket.gethostbyname(hostname)
                    new_netloc = ipv4_address
                    if parsed.port:
                        new_netloc = f"{ipv4_address}:{parsed.port}"
                    if parsed.username:
                        auth = parsed.username
                        if parsed.password:
                            auth = f"{auth}:{parsed.password}"
                        new_netloc = f"{auth}@{new_netloc}"
                    
                    parsed = parsed._replace(netloc=new_netloc)
                except Exception:
                    pass
            
            # 4. Clean up environment for asyncpg
            # Some cloud environments set invalid PGSSLMODE values.
            if "PGSSLMODE" in os.environ:
                val = os.environ["PGSSLMODE"]
                valid_sslmodes = ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"]
                if val not in valid_sslmodes:
                    # Force to a valid value if it's something like 'true'
                    os.environ["PGSSLMODE"] = "require"

            return urlunparse(parsed)
            
        except Exception:
            return url

settings = Settings()
