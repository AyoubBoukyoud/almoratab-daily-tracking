from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.sprint import Sprint
from fastapi import HTTPException, status

async def get_sprint_for_date(db: AsyncSession, query_date: date) -> Sprint:
    """Finds the sprint that contains the given query_date."""
    result = await db.execute(
        select(Sprint).where(
            and_(
                Sprint.start_date <= query_date,
                Sprint.end_date >= query_date
            )
        )
    )
    sprint = result.scalar_one_or_none()
    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No active sprint found for the date: {query_date}"
        )
    return sprint

def is_submission_allowed(submission_date: date) -> bool:
    """Saturday is rest day for testing. Python date.weekday() returns 5 for Saturday."""
    if submission_date.weekday() == 5:
        return False
    return True
