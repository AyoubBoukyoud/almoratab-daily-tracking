import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class LiveAttendance(Base):
    __tablename__ = "live_attendance"
    __table_args__ = (
        UniqueConstraint("user_id", "live_session_id", name="unique_attendance"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    live_session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("live_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    validated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    validated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    points_awarded: Mapped[int] = mapped_column(Integer, default=4, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="attendance", foreign_keys=[user_id])
    live_session: Mapped["LiveSession"] = relationship(back_populates="attendance")
    admin_validator: Mapped["User"] = relationship(foreign_keys=[validated_by])
