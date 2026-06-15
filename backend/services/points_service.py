from uuid import UUID
from datetime import date
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from models.sprint import Sprint
from models.task_submission import TaskSubmission
from models.live_session import LiveSession
from models.live_attendance import LiveAttendance
from schemas.admin import (
    LeaderboardEntry, 
    UserSprintStats, 
    UserProgressOut, 
    ProgressChartEntry, 
    SprintLeaderboardEntry
)
from typing import List
from .sprint_service import get_sprint_for_date

async def get_user_total_points(db: AsyncSession, user_id: UUID) -> int:
    # 1. Sum task submission points
    task_result = await db.execute(
        select(func.sum(TaskSubmission.points_earned)).where(TaskSubmission.user_id == user_id)
    )
    task_pts = task_result.scalar() or 0

    # 2. Sum live attendance points
    live_result = await db.execute(
        select(func.sum(LiveAttendance.points_awarded)).where(LiveAttendance.user_id == user_id)
    )
    live_pts = live_result.scalar() or 0

    return task_pts + live_pts

async def get_user_sprint_stats(db: AsyncSession, user_id: UUID, sprint: Sprint) -> UserSprintStats:
    # Task points in sprint
    task_result = await db.execute(
        select(func.sum(TaskSubmission.points_earned))
        .where(
            TaskSubmission.user_id == user_id,
            TaskSubmission.sprint_id == sprint.id
        )
    )
    task_pts = task_result.scalar() or 0

    # Live points in sprint (join with LiveSession)
    live_result = await db.execute(
        select(func.sum(LiveAttendance.points_awarded))
        .join(LiveSession, LiveAttendance.live_session_id == LiveSession.id)
        .where(
            LiveAttendance.user_id == user_id,
            LiveSession.sprint_id == sprint.id
        )
    )
    live_pts = live_result.scalar() or 0

    return UserSprintStats(
        sprint_number=sprint.sprint_number,
        task_points=task_pts,
        live_points=live_pts,
        total=task_pts + live_pts
    )

async def get_leaderboard(db: AsyncSession) -> List[LeaderboardEntry]:
    # Query all users with role 'user' or 'superUser'
    result = await db.execute(select(User).where(User.role.in_(["user", "superUser"])))
    users = result.scalars().all()

    leaderboard = []
    for user in users:
        total_pts = await get_user_total_points(db, user.id)
        leaderboard.append(
            LeaderboardEntry(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                total_points=total_pts
            )
        )

    # Sort descending by total_points, ties broken alphabetically by full_name
    leaderboard.sort(key=lambda x: (-x.total_points, x.full_name))
    return leaderboard

async def get_sprint_leaderboard(db: AsyncSession, sprint_id: UUID) -> List[SprintLeaderboardEntry]:
    # 1. Get the sprint
    res = await db.execute(select(Sprint).where(Sprint.id == sprint_id))
    sprint = res.scalar_one_or_none()
    if not sprint:
        return []

    # 2. Query all users (user + superUser)
    res = await db.execute(select(User).where(User.role.in_(["user", "superUser"])))
    users = res.scalars().all()

    leaderboard = []
    for user in users:
        stats = await get_user_sprint_stats(db, user.id, sprint)
        leaderboard.append(
            SprintLeaderboardEntry(
                id=user.id,
                full_name=user.full_name,
                sprint_points=stats.total
            )
        )

    # 3. Sort descending by points
    leaderboard.sort(key=lambda x: (-x.sprint_points, x.full_name))
    return leaderboard

async def get_user_progress_detail(db: AsyncSession, user: User) -> UserProgressOut:
    # Query all 5 sprints sorted by sprint_number
    sprints_result = await db.execute(select(Sprint).order_by(Sprint.sprint_number))
    sprints = sprints_result.scalars().all()

    sprint_stats = []
    for sprint in sprints:
        stats = await get_user_sprint_stats(db, user.id, sprint)
        sprint_stats.append(stats)

    total_points = await get_user_total_points(db, user.id)

    # Determine current sprint and day
    today = date.today()
    try:
        # 1. Try date-based lookup
        res = await db.execute(
            select(Sprint).where(
                and_(
                    Sprint.start_date <= today,
                    Sprint.end_date >= today
                )
            )
        )
        current_sprint = res.scalar_one_or_none()
        
        # 2. If not found by date, fallback to the one marked is_active
        if not current_sprint:
            res = await db.execute(select(Sprint).where(Sprint.is_active == True).limit(1))
            current_sprint = res.scalar_one_or_none()
            
        # 3. Last fallback: first sprint
        if not current_sprint:
            res = await db.execute(select(Sprint).order_by(Sprint.sprint_number).limit(1))
            current_sprint = res.scalar_one_or_none()

        if current_sprint:
            current_sprint_number = current_sprint.sprint_number
            # If we are before the start_date, day is 0
            if today < current_sprint.start_date:
                current_day = 0
            else:
                current_day = (today - current_sprint.start_date).days + 1
        else:
            current_sprint_number = 1
            current_day = 0
            
    except Exception:
        current_sprint_number = 1
        current_day = 0

    return UserProgressOut(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        total_points=total_points,
        current_sprint_number=current_sprint_number,
        current_day=current_day,
        sprint_stats=sprint_stats
    )

async def get_user_cumulative_chart(db: AsyncSession, user_id: UUID) -> List[ProgressChartEntry]:
    # Get all task submissions chronologically
    sub_result = await db.execute(
        select(TaskSubmission.submission_date, TaskSubmission.points_earned)
        .where(TaskSubmission.user_id == user_id)
        .order_by(TaskSubmission.submission_date)
    )
    submissions = sub_result.all()

    # Get all live sessions validations. 
    # We fetch session_date and validation date separately to handle logic in Python.
    live_result = await db.execute(
        select(LiveSession.session_date, LiveAttendance.validated_at, LiveAttendance.points_awarded)
        .join(LiveSession, LiveAttendance.live_session_id == LiveSession.id)
        .where(LiveAttendance.user_id == user_id)
    )
    live_validations = live_result.all()

    # Combine both lists and sort chronologically in Python to avoid complex SQL issues
    events = []
    for s_date, points in submissions:
        events.append((s_date, points))
        
    for session_date, validated_at, points in live_validations:
        # Use session date if available, otherwise fallback to date of validation
        event_date = session_date if session_date else validated_at.date()
        events.append((event_date, points))

    # Sort all events by date
    events.sort(key=lambda x: x[0])

    # Aggregate cumulative points
    chart_data = []
    cumulative = 0
    for event_date, points in events:
        cumulative += points
        # Update existing date or append new date
        if chart_data and chart_data[-1].date == event_date:
            # Create a new ProgressChartEntry to replace the old one
            chart_data[-1] = ProgressChartEntry(date=event_date, cumulative_points=cumulative)
        else:
            chart_data.append(ProgressChartEntry(date=event_date, cumulative_points=cumulative))

    return chart_data
