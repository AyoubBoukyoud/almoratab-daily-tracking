from .auth import router as auth_router
from .tasks import router as tasks_router
from .users import router as users_router
from .sprints import router as sprints_router
from .admin import router as admin_router

__all__ = [
    "auth_router",
    "tasks_router",
    "users_router",
    "sprints_router",
    "admin_router",
]
