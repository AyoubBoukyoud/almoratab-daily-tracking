from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID

class TaskSubmitRequest(BaseModel):
    task1_done: bool = False
    task2_done: bool = False
    task3_done: bool = False

class TaskSubmissionOut(BaseModel):
    id: UUID
    submission_date: date
    task1_done: bool
    task2_done: bool
    task3_done: bool
    points_earned: int
    submitted_at: datetime

    class Config:
        from_attributes = True
