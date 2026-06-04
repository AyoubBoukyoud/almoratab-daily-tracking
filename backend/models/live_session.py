import uuid
from datetime import datetime, date
from sqlalchemy import ForeignKey, Integer, String, Date, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class LiveSession(Base):
    __tablename__ = "live_sessions"
    __table_args__ = (
        CheckConstraint("session_number BETWEEN 1 AND 2", name="session_number_range"),
        UniqueConstraint("sprint_id", "session_number", name="unique_session"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    sprint_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sprints.id", ondelete="CASCADE"), nullable=False, index=True)
    session_number: Mapped[int] = mapped_column(Integer, nullable=False)
    session_date: Mapped[date] = mapped_column(Date, nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    sprint: Mapped["Sprint"] = relationship(back_populates="live_sessions")
    attendance: Mapped[list["LiveAttendance"]] = relationship(back_populates="live_session", cascade="all, delete-orphan")
