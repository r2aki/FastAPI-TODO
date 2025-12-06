from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Task(Base):
    __tablename__ = "tasks"
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[int] = mapped_column(Integer)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    assigned_to_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project: Mapped["Project"] | None = relationship(back_populates="tasks")
    assigned_to: Mapped["User"] | None = relationship(back_populates="tasks")
