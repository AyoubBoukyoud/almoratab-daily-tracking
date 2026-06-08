import socket
import ssl
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from .config import settings

# Get URL from settings (which is now stripped of all query params)
db_url = settings.DATABASE_URL

# Create a custom SSL context that enables encryption but skips certificate verification.
# This is necessary because some cloud environments (like Hugging Face) don't have
# the root certificates required to verify Supabase/PgBouncer's SSL chain.
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create engine with async driver (asyncpg)
# We pass ALL driver-specific arguments explicitly in connect_args 
# to avoid any incompatible parameters being passed from the DSN.
engine = create_async_engine(
    db_url,
    echo=settings.APP_ENV == "development",
    future=True,
    poolclass=pool.NullPool,
    connect_args={
        # Use the custom SSL context
        "ssl": ssl_context,
        # CRITICAL: Disable statement cache for Supabase/PgBouncer compatibility
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0
    }
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Dependency to get db session in FastAPI routes
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
