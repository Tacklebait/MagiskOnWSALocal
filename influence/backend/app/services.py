from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ArcStatus, BeatStatus, Goal, GoalProgressEntry, GoalStatus, NarrativeArc, NarrativeBeat

GOAL_TRANSITIONS = {
    GoalStatus.proposed: {GoalStatus.active, GoalStatus.abandoned},
    GoalStatus.active: {GoalStatus.blocked, GoalStatus.achieved, GoalStatus.failed, GoalStatus.abandoned, GoalStatus.paused},
    GoalStatus.blocked: {GoalStatus.active, GoalStatus.failed, GoalStatus.abandoned},
    GoalStatus.paused: {GoalStatus.active, GoalStatus.abandoned},
}
ARC_TRANSITIONS = {
    ArcStatus.planned: {ArcStatus.active, ArcStatus.abandoned},
    ArcStatus.active: {ArcStatus.paused, ArcStatus.blocked, ArcStatus.resolving, ArcStatus.abandoned},
    ArcStatus.paused: {ArcStatus.active, ArcStatus.abandoned},
    ArcStatus.blocked: {ArcStatus.active, ArcStatus.abandoned},
    ArcStatus.resolving: {ArcStatus.completed, ArcStatus.active, ArcStatus.abandoned},
}


def transition_goal(db: Session, goal: Goal, status: GoalStatus) -> Goal:
    if status == goal.status:
        return goal
    if status not in GOAL_TRANSITIONS.get(goal.status, set()):
        raise HTTPException(422, f"Cannot transition goal from {goal.status} to {status}")
    goal.status = status
    goal.version += 1
    if status == GoalStatus.active and not goal.started_at: goal.started_at = datetime.now().astimezone()
    if status in {GoalStatus.achieved, GoalStatus.failed, GoalStatus.abandoned}: goal.completed_at = datetime.now().astimezone()
    db.add(goal); db.commit(); db.refresh(goal)
    return goal


def add_progress(db: Session, goal: Goal, new_value: float, explanation: str, source: str) -> GoalProgressEntry:
    entry = GoalProgressEntry(goal_id=goal.id, change_type="progress", previous_value=goal.progress_value, new_value=new_value, explanation=explanation, source=source)
    goal.progress_value = new_value; goal.progress_summary = explanation; goal.version += 1
    db.add_all([goal, entry]); db.commit(); db.refresh(entry)
    return entry


def transition_arc(db: Session, arc: NarrativeArc, status: ArcStatus) -> NarrativeArc:
    if status == arc.status: return arc
    if arc.operator_locked: raise HTTPException(409, "Operator-locked arcs cannot be changed automatically")
    if status not in ARC_TRANSITIONS.get(arc.status, set()): raise HTTPException(422, f"Cannot transition arc from {arc.status} to {status}")
    arc.status = status; db.add(arc); db.commit(); db.refresh(arc)
    return arc


def generate_daily_chapter(db: Session, arc: NarrativeArc, planned_for) -> list[NarrativeBeat]:
    """Deterministic fallback planner: one meaningful, schema-valid beat per day."""
    existing = db.scalar(select(NarrativeBeat).where(NarrativeBeat.arc_id == arc.id, NarrativeBeat.planned_for == planned_for))
    if existing: return [existing]
    sequence = (db.scalar(select(NarrativeBeat.sequence_number).where(NarrativeBeat.arc_id == arc.id).order_by(NarrativeBeat.sequence_number.desc())) or 0) + 1
    goal_phrase = arc.desired_outcome or arc.premise
    beat = NarrativeBeat(arc_id=arc.id, character_id=arc.character_id, sequence_number=sequence, beat_type="progress", title=f"Make room for {arc.title}", description=f"A focused, feasible step toward: {goal_phrase}", purpose="Advance the active narrative without inventing an event.", planned_for=planned_for, status=BeatStatus.scheduled)
    db.add(beat); db.commit(); db.refresh(beat)
    return [beat]
