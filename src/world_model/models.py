from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for the PostgreSQL world model."""


class TimestampMixin:
    """Standard audit timestamps using TIMESTAMPTZ."""

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Zone(TimestampMixin, Base):
    """Persisted disaster zone state derived from perception and planning."""

    __tablename__ = "zones"

    zone_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    critical_count: Mapped[int] = mapped_column(default=0, nullable=False)
    high_count: Mapped[int] = mapped_column(default=0, nullable=False)
    medium_count: Mapped[int] = mapped_column(default=0, nullable=False)
    total_count: Mapped[int] = mapped_column(default=0, nullable=False)
    hazard_multiplier: Mapped[float] = mapped_column(default=1.0, nullable=False)
    urgency_score: Mapped[float] = mapped_column(default=0.0, nullable=False, index=True)
    survivor_metrics: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )
    pose_distribution: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )
    scene_summary: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    tasks: Mapped[list[Task]] = relationship(
        back_populates="zone",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_zones_status_severity", "status", "severity"),
    )


class Agent(TimestampMixin, Base):
    """Track responder or software agent assignment state."""

    __tablename__ = "agents"

    agent_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), default="idle", nullable=False, index=True)
    capabilities: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    current_load: Mapped[int] = mapped_column(default=0, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    last_heartbeat: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    tasks: Mapped[list[Task]] = relationship(back_populates="assigned_agent")


class Task(TimestampMixin, Base):
    """Operational work item produced from zone triage and planning."""

    __tablename__ = "tasks"

    task_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    zone_id: Mapped[int] = mapped_column(
        ForeignKey("zones.zone_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assigned_agent_id: Mapped[int | None] = mapped_column(
        ForeignKey("agents.agent_id", ondelete="SET NULL"),
        index=True,
    )
    type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False, index=True)
    priority: Mapped[float] = mapped_column(default=0.0, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    task_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    zone: Mapped[Zone] = relationship(back_populates="tasks")
    assigned_agent: Mapped[Agent | None] = relationship(back_populates="tasks")

    __table_args__ = (
        Index("ix_tasks_zone_status", "zone_id", "status"),
    )


class InferenceCache(Base):
    """Cache deterministic inference artifacts keyed by image hash."""

    __tablename__ = "inference_cache"

    image_hash: Mapped[str] = mapped_column(String(32), primary_key=True)
    zone_report_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    pose_distribution: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )
    model_versions: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    last_accessed_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


def create_schema(engine: Engine) -> None:
    """Create the world model schema idempotently."""

    Base.metadata.create_all(bind=engine, checkfirst=True)
