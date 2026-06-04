from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from core.database import get_db
from dependencies.auth import get_current_user
from models.user import User
from models.task_submission import TaskSubmission
from schemas.task import TaskSubmitRequest, TaskSubmissionOut
from services.sprint_service import get_sprint_for_date, is_submission_allowed
from sqlalchemy import select, and_
from typing import List, Optional
from uuid import UUID

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/submit", response_model=TaskSubmissionOut)
async def submit_tasks(
    payload: TaskSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    today = date.today()

    # 1. Enforce Sunday lock
    if not is_submission_allowed(today):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rest day — submissions are not allowed on Sundays."
        )

    # 2. Must be within active sprint
    sprint = await get_sprint_for_date(db, today)

    # 3. Check for duplicate daily submission
    result = await db.execute(
        select(TaskSubmission).where(
            and_(
                TaskSubmission.user_id == current_user.id,
                TaskSubmission.submission_date == today
            )
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already submitted tasks for today."
        )

    # 4. Calculate points
    tasks_done_count = sum([payload.task1_done, payload.task2_done, payload.task3_done])
    points_earned = tasks_done_count * 2

    # 5. Create submission record
    submission = TaskSubmission(
        user_id=current_user.id,
        sprint_id=sprint.id,
        submission_date=today,
        task1_done=payload.task1_done,
        task2_done=payload.task2_done,
        task3_done=payload.task3_done,
        points_earned=points_earned
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return submission

@router.get("/today")
async def get_today_submission_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    today = date.today()
    result = await db.execute(
        select(TaskSubmission).where(
            and_(
                TaskSubmission.user_id == current_user.id,
                TaskSubmission.submission_date == today
            )
        )
    )
    submission = result.scalar_one_or_none()
    if submission:
        return {"submitted": True, "submission": submission}
    return {"submitted": False, "submission": None}

@router.get("/history", response_model=List[TaskSubmissionOut])
async def get_history(
    sprint_id: Optional[UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TaskSubmission).where(TaskSubmission.user_id == current_user.id)
    if sprint_id:
        query = query.where(TaskSubmission.sprint_id == sprint_id)
    query = query.order_by(TaskSubmission.submission_date.desc())

    result = await db.execute(query)
    return result.scalars().all()
