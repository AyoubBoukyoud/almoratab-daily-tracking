import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from core.config import settings
from core.database import engine

from routers import auth_router, tasks_router, users_router, sprints_router, admin_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify DB connectivity
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection verified successfully")
    except Exception as e:
        logger.error(f"Database connection failed on startup: {e}")
    yield

app = FastAPI(
    title="رحلة البزنس المرتب API",
    description="Backend API for tracking daily task progress, sprints, and user scores.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(sprints_router)
app.include_router(admin_router)

@app.get("/health")
async def health_check():
    """Basic health check (no DB hit) — used by HuggingFace Spaces to keep container alive."""
    return {"status": "ok", "app_env": settings.APP_ENV}

@app.get("/health/db")
async def health_check_db():
    """Deep health check that verifies DB connectivity."""
    from core.database import AsyncSessionLocal
    from sqlalchemy import text
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

