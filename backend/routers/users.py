from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from dependencies.auth import get_current_user
from models.user import User
from schemas.user import UserOut
from schemas.admin import UserProgressOut
from services.points_service import get_user_progress_detail

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/stats", response_model=UserProgressOut)
async def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Returns their own stats (total points + per-sprint breakdown)
    stats = await get_user_progress_detail(db, current_user)
    return stats
