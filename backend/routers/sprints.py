from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from dependencies.auth import get_current_user
from models.sprint import Sprint
from models.user import User
from schemas.sprint import SprintOut
from schemas.admin import SprintLeaderboardEntry
from services.points_service import get_sprint_leaderboard
from sqlalchemy import select, and_
from datetime import date
from typing import List
from uuid import UUID

router = APIRouter(prefix="/sprints", tags=["sprints"])

@router.get("/", response_model=List[SprintOut])
async def list_sprints(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Sprint).order_by(Sprint.sprint_number))
    return result.scalars().all()

@router.get("/current", response_model=SprintOut)
async def get_current_sprint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    # 1. Try date-based lookup
    result = await db.execute(
        select(Sprint).where(
            and_(
                Sprint.start_date <= today,
                Sprint.end_date >= today
            )
        )
    )
    sprint = result.scalar_one_or_none()

    # 2. If not found by date, fallback to the one marked is_active
    if not sprint:
        result = await db.execute(
            select(Sprint)
            .where(Sprint.is_active == True)
            .limit(1)
        )
        sprint = result.scalar_one_or_none()

    # 3. Fallback: find the most recent sprint that has already started
    if not sprint:
        result = await db.execute(
            select(Sprint)
            .where(Sprint.start_date <= today)
            .order_by(Sprint.start_date.desc())
            .limit(1)
        )
        sprint = result.scalar_one_or_none()

    # 4. Last fallback: find the first sprint (for before program start)
    if not sprint:
        result = await db.execute(select(Sprint).order_by(Sprint.sprint_number).limit(1))
        sprint = result.scalar_one_or_none()

    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No current, active, or past sprint found"
        )
    return sprint

@router.get("/current/leaderboard", response_model=List[SprintLeaderboardEntry])
async def get_current_sprint_leaderboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Reuse get_current_sprint logic to find the ID
    today = date.today()
    result = await db.execute(
        select(Sprint).where(
            and_(
                Sprint.start_date <= today,
                Sprint.end_date >= today
            )
        )
    )
    sprint = result.scalar_one_or_none()
    
    if not sprint:
        # Fallback to is_active
        result = await db.execute(select(Sprint).where(Sprint.is_active == True).limit(1))
        sprint = result.scalar_one_or_none()
        
    if not sprint:
        # Fallback to most recent
        result = await db.execute(
            select(Sprint)
            .where(Sprint.start_date <= today)
            .order_by(Sprint.start_date.desc())
            .limit(1)
        )
        sprint = result.scalar_one_or_none()

    if not sprint:
        # Fallback to first
        result = await db.execute(select(Sprint).order_by(Sprint.sprint_number).limit(1))
        sprint = result.scalar_one_or_none()

    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    return await get_sprint_leaderboard(db, sprint.id)

@router.get("/leaderboard/sprint/{sprint_id}", response_model=List[SprintLeaderboardEntry])
async def get_any_sprint_leaderboard(
    sprint_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Allows any logged-in user to see the leaderboard for a specific sprint."""
    return await get_sprint_leaderboard(db, sprint_id)
