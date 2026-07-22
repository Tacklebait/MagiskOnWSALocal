import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class GoalStatus(str, enum.Enum):
    proposed = "proposed"; active = "active"; blocked = "blocked"; achieved = "achieved"; failed = "failed"; abandoned = "abandoned"; paused = "paused"


class ArcStatus(str, enum.Enum):
    planned = "planned"; active = "active"; paused = "paused"; blocked = "blocked"; resolving = "resolving"; completed = "completed"; abandoned = "abandoned"


class BeatStatus(str, enum.Enum):
    proposed = "proposed"; planned = "planned"; scheduled = "scheduled"; in_progress = "in_progress"; completed = "completed"; skipped = "skipped"; failed = "failed"; cancelled = "cancelled"


class Character(Base):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    bio: Mapped[str] = mapped_column(Text, default="")
    stable_identity: Mapped[dict] = mapped_column(JSON, default=dict)
    evolving_identity: Mapped[dict] = mapped_column(JSON, default=dict)
    volatile_state: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    goals: Mapped[list["Goal"]] = relationship(back_populates="character")
    arcs: Mapped[list["NarrativeArc"]] = relationship(back_populates="character")


class Goal(Base):
    __tablename__ = "goals"
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), index=True)
    parent_goal_id: Mapped[int | None] = mapped_column(ForeignKey("goals.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(40), default="other")
    time_horizon: Mapped[str] = mapped_column(String(30), default="long_term")
    status: Mapped[GoalStatus] = mapped_column(Enum(GoalStatus), default=GoalStatus.proposed, index=True)
    priority: Mapped[int] = mapped_column(Integer, default=50)
    motivation: Mapped[str] = mapped_column(Text, default="")
    success_definition: Mapped[str] = mapped_column(Text, default="")
    progress_summary: Mapped[str] = mapped_column(Text, default="")
    progress_value: Mapped[float] = mapped_column(Float, default=0)
    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    origin_type: Mapped[str] = mapped_column(String(40), default="operator")
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    character: Mapped[Character] = relationship(back_populates="goals")
    progress_entries: Mapped[list["GoalProgressEntry"]] = relationship(back_populates="goal")


class GoalProgressEntry(Base):
    __tablename__ = "goal_progress_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"), index=True)
    change_type: Mapped[str] = mapped_column(String(50))
    previous_value: Mapped[float] = mapped_column(Float)
    new_value: Mapped[float] = mapped_column(Float)
    explanation: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(40), default="operator")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    goal: Mapped[Goal] = relationship(back_populates="progress_entries")


class NarrativeArc(Base):
    __tablename__ = "narrative_arcs"
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), index=True)
    primary_goal_id: Mapped[int | None] = mapped_column(ForeignKey("goals.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(200))
    premise: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(40), default="personal")
    status: Mapped[ArcStatus] = mapped_column(Enum(ArcStatus), default=ArcStatus.planned, index=True)
    tone: Mapped[str] = mapped_column(String(80), default="grounded")
    stakes: Mapped[str] = mapped_column(Text, default="")
    desired_outcome: Mapped[str] = mapped_column(Text, default="")
    current_summary: Mapped[str] = mapped_column(Text, default="")
    current_state: Mapped[dict] = mapped_column(JSON, default=dict)
    start_date: Mapped[date] = mapped_column(Date, default=date.today)
    target_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=50)
    operator_locked: Mapped[bool] = mapped_column(default=False)
    character: Mapped[Character] = relationship(back_populates="arcs")
    beats: Mapped[list["NarrativeBeat"]] = relationship(back_populates="arc")


class NarrativeBeat(Base):
    __tablename__ = "narrative_beats"
    __table_args__ = (UniqueConstraint("arc_id", "sequence_number", name="uq_arc_beat_sequence"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    arc_id: Mapped[int] = mapped_column(ForeignKey("narrative_arcs.id"), index=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), index=True)
    sequence_number: Mapped[int] = mapped_column(Integer)
    beat_type: Mapped[str] = mapped_column(String(40))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    purpose: Mapped[str] = mapped_column(Text)
    planned_for: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    status: Mapped[BeatStatus] = mapped_column(Enum(BeatStatus), default=BeatStatus.planned, index=True)
    expected_consequences: Mapped[dict] = mapped_column(JSON, default=dict)
    arc: Mapped[NarrativeArc] = relationship(back_populates="beats")
