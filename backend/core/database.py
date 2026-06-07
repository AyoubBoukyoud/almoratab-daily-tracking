import socket
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from .config import settings

# Get URL from settings
db_url = settings.DATABASE_URL

# Create engine with async driver (asyncpg)
# We use connect_args to tell asyncpg to prioritize IPv4 and disable statement caching
# We use NullPool because Supabase already provides a connection pooler
engine = create_async_engine(
    db_url,
    echo=settings.APP_ENV == "development",
    future=True,
    poolclass=pool.NullPool,
    prepared_statement_cache_size=0,
    connect_args={
        "socket_keys": ["family"],
        # This tells asyncpg to use IPv4 only
        "family": socket.AF_INET,
        # CRITICAL: Disable statement cache for Supabase/PgBouncer compatibility
        "statement_cache_size": 0
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
