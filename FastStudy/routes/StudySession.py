from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId

from models.StudySession import StudySession, Task
from models.User import User, StudyStat
from auth.dependencies import get_current_user

router = APIRouter(prefix="/study-sessions", tags=["Study Sessions"])


class CreateSessionRequest(BaseModel):
    tasks: List[Task]
    planned_duration: int


class CompleteSessionRequest(BaseModel):
    actual_duration: int
    distractions_blocked: int = 0
    notes: Optional[str] = None


# Get user's study sessions
@router.get("/", response_model=List[StudySession])
async def get_study_sessions(current_user: User = Depends(get_current_user)):
    return await StudySession.find(
        StudySession.user.id == current_user.id
    ).sort(-StudySession.start_time).to_list()


@router.get("/{session_id}", response_model=StudySession)
async def get_study_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    session = await StudySession.get(PydanticObjectId(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Verify ownership
    if str(session.user.id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")

    return session


# Create study session
@router.post("/", response_model=StudySession, status_code=201)
async def create_study_session(
    req: CreateSessionRequest,
    current_user: User = Depends(get_current_user)
):
    session = StudySession(
        user=current_user,  # stored as a Link[User]
        tasks=req.tasks,
        planned_duration=req.planned_duration,
        start_time=datetime.utcnow()
    )
    await session.insert()
    return session


# Complete study session
@router.post("/{session_id}/complete")
async def complete_study_session(
    session_id: str,
    req: CompleteSessionRequest,
    current_user: User = Depends(get_current_user)
):
    session = await StudySession.get(PydanticObjectId(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # verify ownership
    if str(session.user.id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")

    # apply completion data
    session.end_time = datetime.utcnow()
    session.actual_duration = req.actual_duration
    session.distractions_blocked = req.distractions_blocked
    session.notes = req.notes

    # mark tasks done up to actual_duration
    remaining = req.actual_duration
    for t in session.tasks:
        if t.duration <= remaining:
            t.completed = True
            remaining -= t.duration
        else:
            break

    await session.save()

    # bump user aggregate stats
    await current_user.update({"$inc": {
        "total_focus_time": session.actual_duration,
        "weekly_focus_time": session.actual_duration,
        "monthly_focus_time": session.actual_duration
    }})

    # append a daily StudyStat entry
    stat = StudyStat(
        date=datetime.utcnow(),
        focus_time=session.actual_duration,
        sessions=1,
        distractions_blocked=req.distractions_blocked
    )
    current_user.study_stats.append(stat)
    await current_user.save()

    return {"message": "Study session completed successfully"}
