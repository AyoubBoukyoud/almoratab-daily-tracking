from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from .config import settings

# Get URL from settings
db_url = settings.DATABASE_URL

# CRITICAL FIX: Double check sslmode for asyncpg compatibility
if "sslmode=" in db_url:
    db_url = db_url.replace("sslmode=require", "ssl=true")
    db_url = db_url.replace("sslmode=prefer", "ssl=true")
    db_url = db_url.replace("sslmode=disable", "ssl=false")

# Create engine with async driver (asyncpg)
engine = create_async_engine(
    db_url,
    echo=settings.APP_ENV == "development",
    future=True
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
