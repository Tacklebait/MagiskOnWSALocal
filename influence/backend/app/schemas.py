from datetime import date
from pydantic import BaseModel, Field

from .models import ArcStatus, BeatStatus, GoalStatus


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    bio: str = ""
    stable_identity: dict = Field(default_factory=dict)


class CharacterRead(CharacterCreate):
    id: int
    evolving_identity: dict
    volatile_state: dict
    class Config: from_attributes = True


class GoalCreate(BaseModel):
    title: str
    description: str = ""
    category: str = "other"
    time_horizon: str = "long_term"
    priority: int = Field(default=50, ge=0, le=100)
    motivation: str = ""
    success_definition: str = ""
    parent_goal_id: int | None = None
    target_date: date | None = None


class GoalRead(GoalCreate):
    id: int; character_id: int; status: GoalStatus; progress_summary: str; progress_value: float; version: int
    class Config: from_attributes = True


class ProgressCreate(BaseModel):
    new_value: float = Field(ge=0, le=100)
    explanation: str
    source: str = "operator"


class ArcCreate(BaseModel):
    title: str; premise: str; primary_goal_id: int | None = None
    category: str = "personal"; tone: str = "grounded"; stakes: str = ""; desired_outcome: str = ""; priority: int = Field(default=50, ge=0, le=100)


class ArcRead(ArcCreate):
    id: int; character_id: int; status: ArcStatus; current_summary: str; operator_locked: bool
    class Config: from_attributes = True


class BeatRead(BaseModel):
    id: int; arc_id: int; character_id: int; sequence_number: int; beat_type: str; title: str; description: str; purpose: str; planned_for: date | None; status: BeatStatus
    class Config: from_attributes = True


class DailyChapterRequest(BaseModel):
    date: date


class NarrativeState(BaseModel):
    character: CharacterRead
    active_goals: list[GoalRead]
    active_arcs: list[ArcRead]
    next_beats: list[BeatRead]
