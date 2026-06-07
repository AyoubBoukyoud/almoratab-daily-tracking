import socket
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from .config import settings

# Get URL from settings
db_url = settings.DATABASE_URL

# --- FORCE IPv4 RESOLUTION (Option 1 Proxy Trick) ---
# This overrides the default socket connection to skip IPv6 entirely
async def ipv4_only_connect(*args, **kwargs):
    import asyncpg
    # Force AF_INET (IPv4)
    kwargs["family"] = socket.AF_INET
    return await asyncpg.connect(*args, **kwargs)

# Create engine with async driver (asyncpg)
# We use connect_args to tell asyncpg to prioritize IPv4
engine = create_async_engine(
    db_url,
    echo=settings.APP_ENV == "development",
    future=True,
    connect_args={
        "socket_keys": ["family"],
        # This tells asyncpg to use IPv4 only
        "family": socket.AF_INET
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
