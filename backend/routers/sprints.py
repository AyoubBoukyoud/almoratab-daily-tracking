from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from dependencies.auth import get_current_user
from models.sprint import Sprint
from schemas.sprint import SprintOut
from sqlalchemy import select
from datetime import date
from typing import List

router = APIRouter(prefix="/sprints", tags=["sprints"])

@router.get("/", response_model=List[SprintOut])
async def list_sprints(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = await db.execute(select(Sprint).order_by(Sprint.sprint_number))
    return result.scalars().all()

@router.get("/current", response_model=SprintOut)
async def get_current_sprint(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    today = date.today()
    result = await db.execute(
        select(Sprint).where(
            Sprint.is_active == True
        )
    )
    sprint = result.scalar_one_or_none()
    if not sprint:
        # Fallback: find sprint covering today
        result = await db.execute(
            select(Sprint).where(
                Sprint.start_date <= today,
                Sprint.end_date >= today
            )
        )
        sprint = result.scalar_one_or_none()

    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active sprint found"
        )
    return sprint
