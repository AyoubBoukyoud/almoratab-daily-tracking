import uuid
from datetime import datetime, date
from sqlalchemy import Integer, Date, Boolean, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Sprint(Base):
    __tablename__ = "sprints"
    __table_args__ = (
        CheckConstraint("sprint_number BETWEEN 1 AND 5", name="sprint_number_range"),
        CheckConstraint("end_date > start_date", name="valid_dates"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    sprint_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    submissions: Mapped[list["TaskSubmission"]] = relationship(back_populates="sprint", cascade="all, delete-orphan")
    live_sessions: Mapped[list["LiveSession"]] = relationship(back_populates="sprint", cascade="all, delete-orphan")
