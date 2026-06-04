from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List
from uuid import UUID

class LeaderboardEntry(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    total_points: int

class UserSprintStats(BaseModel):
    sprint_number: int
    task_points: int
    live_points: int
    total: int
    max_task_points: int = 72
    max_live_points: int = 8
    max_total: int = 80

class UserProgressOut(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str
    total_points: int
    current_sprint_number: int = 1
    current_day: int = 1
    sprint_stats: List[UserSprintStats]

class ProgressChartEntry(BaseModel):
    date: date
    cumulative_points: int
