from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_session
from .models import ArcStatus, Character, Goal, GoalStatus, NarrativeArc, NarrativeBeat
from .schemas import ArcCreate, ArcRead, BeatRead, CharacterCreate, CharacterRead, DailyChapterRequest, GoalCreate, GoalRead, NarrativeState, ProgressCreate
from .services import add_progress, generate_daily_chapter, transition_arc, transition_goal

Base.metadata.create_all(engine)
app = FastAPI(title="Influence V2", version="0.1.0")

def character_or_404(db, character_id):
    character = db.get(Character, character_id)
    if not character: raise HTTPException(404, "Character not found")
    return character

def goal_or_404(db, goal_id):
    goal = db.get(Goal, goal_id)
    if not goal: raise HTTPException(404, "Goal not found")
    return goal

def arc_or_404(db, arc_id):
    arc = db.get(NarrativeArc, arc_id)
    if not arc: raise HTTPException(404, "Narrative arc not found")
    return arc

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/characters", response_model=CharacterRead, status_code=201)
def create_character(data: CharacterCreate, db: Session = Depends(get_session)):
    character = Character(**data.model_dump())
    db.add(character); db.commit(); db.refresh(character); return character

@app.get("/characters", response_model=list[CharacterRead])
def list_characters(db: Session = Depends(get_session)): return list(db.scalars(select(Character).order_by(Character.name)))

@app.post("/characters/{character_id}/goals", response_model=GoalRead, status_code=201)
def create_goal(character_id: int, data: GoalCreate, db: Session = Depends(get_session)):
    character_or_404(db, character_id)
    if data.parent_goal_id:
        parent = goal_or_404(db, data.parent_goal_id)
        if parent.character_id != character_id: raise HTTPException(422, "Parent goal belongs to another character")
    goal = Goal(character_id=character_id, **data.model_dump()); db.add(goal); db.commit(); db.refresh(goal); return goal

@app.get("/characters/{character_id}/goals", response_model=list[GoalRead])
def list_goals(character_id: int, db: Session = Depends(get_session)):
    character_or_404(db, character_id); return list(db.scalars(select(Goal).where(Goal.character_id == character_id).order_by(Goal.priority.desc())))

@app.post("/goals/{goal_id}/status/{status}", response_model=GoalRead)
def set_goal_status(goal_id: int, status: GoalStatus, db: Session = Depends(get_session)): return transition_goal(db, goal_or_404(db, goal_id), status)

@app.post("/goals/{goal_id}/progress", status_code=201)
def record_progress(goal_id: int, data: ProgressCreate, db: Session = Depends(get_session)):
    return add_progress(db, goal_or_404(db, goal_id), data.new_value, data.explanation, data.source)

@app.post("/characters/{character_id}/arcs", response_model=ArcRead, status_code=201)
def create_arc(character_id: int, data: ArcCreate, db: Session = Depends(get_session)):
    character_or_404(db, character_id)
    if data.primary_goal_id and goal_or_404(db, data.primary_goal_id).character_id != character_id: raise HTTPException(422, "Goal belongs to another character")
    active = list(db.scalars(select(NarrativeArc).where(NarrativeArc.character_id == character_id, NarrativeArc.status == ArcStatus.active)))
    if len(active) >= 3: raise HTTPException(409, "A character may have at most three active arcs")
    arc = NarrativeArc(character_id=character_id, **data.model_dump()); db.add(arc); db.commit(); db.refresh(arc); return arc

@app.get("/characters/{character_id}/arcs", response_model=list[ArcRead])
def list_arcs(character_id: int, db: Session = Depends(get_session)):
    character_or_404(db, character_id); return list(db.scalars(select(NarrativeArc).where(NarrativeArc.character_id == character_id)))

@app.post("/arcs/{arc_id}/status/{status}", response_model=ArcRead)
def set_arc_status(arc_id: int, status: ArcStatus, db: Session = Depends(get_session)): return transition_arc(db, arc_or_404(db, arc_id), status)

@app.get("/arcs/{arc_id}/beats", response_model=list[BeatRead])
def list_beats(arc_id: int, db: Session = Depends(get_session)):
    arc_or_404(db, arc_id); return list(db.scalars(select(NarrativeBeat).where(NarrativeBeat.arc_id == arc_id).order_by(NarrativeBeat.sequence_number)))

@app.post("/arcs/{arc_id}/daily-chapter", response_model=list[BeatRead])
def daily_chapter(arc_id: int, data: DailyChapterRequest, db: Session = Depends(get_session)):
    return generate_daily_chapter(db, arc_or_404(db, arc_id), data.date)

@app.get("/characters/{character_id}/narrative-state", response_model=NarrativeState)
def narrative_state(character_id: int, db: Session = Depends(get_session)):
    character = character_or_404(db, character_id)
    goals = list(db.scalars(select(Goal).where(Goal.character_id == character_id, Goal.status == GoalStatus.active)))
    arcs = list(db.scalars(select(NarrativeArc).where(NarrativeArc.character_id == character_id, NarrativeArc.status == ArcStatus.active)))
    beats = list(db.scalars(select(NarrativeBeat).where(NarrativeBeat.character_id == character_id, NarrativeBeat.status.in_(["planned", "scheduled"])).order_by(NarrativeBeat.planned_for)))
    return {"character": character, "active_goals": goals, "active_arcs": arcs, "next_beats": beats}
