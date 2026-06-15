from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.proxy_headers import ProxyHeadersMiddleware
from core.config import settings

from routers import auth_router, tasks_router, users_router, sprints_router, admin_router

app = FastAPI(
    title="رحلة البزنس المرتب API",
    description="Backend API for tracking daily task progress, sprints, and user scores.",
    version="1.0.0"
)

# Handle proxy headers (for HTTPS)
# Starlette (which FastAPI is built on) provides this.
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# CORS configuration
origins = list(settings.ALLOWED_ORIGINS)
if settings.FRONTEND_URL not in origins:
    origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    return {"status": "ok", "app_env": settings.APP_ENV}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

