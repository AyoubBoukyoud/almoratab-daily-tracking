from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from core.database import get_db
from dependencies.auth import require_admin, require_elevated_privilege
from models.user import User
from models.live_session import LiveSession
from models.live_attendance import LiveAttendance
from models.task_submission import TaskSubmission
from schemas.user import UserOut
from schemas.task import TaskSubmissionOut
from schemas.live import LiveSessionOut, LiveAttendanceOut
from schemas.admin import LeaderboardEntry, UserProgressOut, ProgressChartEntry, SprintLeaderboardEntry
from services.points_service import (
    get_leaderboard,
    get_user_progress_detail,
    get_user_cumulative_chart,
    get_sprint_leaderboard,
)
from typing import List
from uuid import UUID

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_elevated_privilege)
):
    result = await db.execute(select(User).where(User.role.in_(["user", "superUser"])).order_by(User.full_name))
    return result.scalars().all()

@router.get("/users/{user_id}", response_model=UserProgressOut)
async def get_user_detail(
    user_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_elevated_privilege)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return await get_user_progress_detail(db, user)

@router.get("/users/{user_id}/history", response_model=List[TaskSubmissionOut])
async def get_user_history(
    user_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_elevated_privilege)
):
    result = await db.execute(
        select(TaskSubmission)
        .where(TaskSubmission.user_id == user_id)
        .order_by(TaskSubmission.submission_date.desc())
    )
    return result.scalars().all()

@router.get("/users/{user_id}/chart", response_model=List[ProgressChartEntry])
async def get_user_chart(
    user_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_elevated_privilege)
):
    # Check if user exists
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return await get_user_cumulative_chart(db, user_id)

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def leaderboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_elevated_privilege)
):
    return await get_leaderboard(db)

@router.get("/leaderboard/sprint/{sprint_id}", response_model=List[SprintLeaderboardEntry])
async def sprint_leaderboard(
    sprint_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_elevated_privilege)
):
    return await get_sprint_leaderboard(db, sprint_id)

from sqlalchemy.orm import selectinload
...
@router.get("/live-sessions", response_model=List[LiveSessionOut])
async def list_live_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_elevated_privilege)
):
    result = await db.execute(
        select(LiveSession)
        .options(selectinload(LiveSession.attendance))
        .order_by(LiveSession.session_date)
    )
    sessions = result.scalars().all()
    # Map attendance to attendees for the schema
    for s in sessions:
        s.attendees = s.attendance
    return sessions

@router.get("/live-attendance/{session_id}", response_model=List[LiveAttendanceOut])
async def list_live_attendance_for_session(
    session_id: UUID, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_elevated_privilege)
):
    result = await db.execute(select(LiveAttendance).where(LiveAttendance.live_session_id == session_id))
    return result.scalars().all()

@router.post("/live-sessions/{session_id}/validate/{user_id}", response_model=LiveAttendanceOut)
async def validate_live_attendance(
    session_id: UUID,
    user_id: UUID,
    current_admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    # Verify session exists
    result = await db.execute(select(LiveSession).where(LiveSession.id == session_id))
    session_exists = result.scalar_one_or_none()
    if not session_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Live session not found"
        )

    # Verify user exists
    user_result = await db.execute(select(User).where(User.id == user_id))
    user_exists = user_result.scalar_one_or_none()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check for existing validation
    att_result = await db.execute(
        select(LiveAttendance).where(
            LiveAttendance.live_session_id == session_id,
            LiveAttendance.user_id == user_id
        )
    )
    existing_attendance = att_result.scalar_one_or_none()
    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Live attendance has already been validated for this user."
        )

    # Create new validation
    attendance = LiveAttendance(
        user_id=user_id,
        live_session_id=session_id,
        validated_by=current_admin.id,
        points_awarded=8
    )
    db.add(attendance)
    try:
        await db.commit()
        await db.refresh(attendance)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Integrity constraint violated: validation already exists"
        )
    return attendance
