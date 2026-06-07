from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

class LiveAttendanceOut(BaseModel):
    id: UUID
    user_id: UUID
    live_session_id: UUID
    validated_by: UUID
    points_awarded: int
    validated_at: datetime

    class Config:
        from_attributes = True

class LiveSessionOut(BaseModel):
    id: UUID
    sprint_id: UUID
    session_number: int
    session_date: Optional[date] = None
    title: Optional[str] = None
    attendees: List[LiveAttendanceOut] = []

    class Config:
        from_attributes = True
