from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID

class SprintOut(BaseModel):
    id: UUID
    sprint_number: int
    start_date: date
    end_date: date
    is_active: bool

    class Config:
        from_attributes = True
