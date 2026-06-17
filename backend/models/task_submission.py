import uuid
from datetime import datetime, date
from sqlalchemy import ForeignKey, Date, Boolean, Integer, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class TaskSubmission(Base):
    __tablename__ = "task_submissions"
    __table_args__ = (
        UniqueConstraint("user_id", "submission_date", name="unique_submission"),
        CheckConstraint(
            "points_earned = "
            "(CASE WHEN task1_done THEN 2 ELSE 0 END) + "
            "(CASE WHEN task2_done THEN 2 ELSE 0 END) + "
            "(CASE WHEN task3_done THEN 3 ELSE 0 END)",
            name="valid_points"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    sprint_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sprints.id", ondelete="CASCADE"), nullable=False, index=True)
    submission_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    task1_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    task2_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    task3_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    points_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="submissions")
    sprint: Mapped["Sprint"] = relationship(back_populates="submissions")
