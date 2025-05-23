from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId

from main import logger
from models.StudySession import StudySession, Task
from models.User import User, StudyStat
from auth.dependencies import get_current_user
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/study-sessions", tags=["Study Sessions"])


class CreateSessionRequest(BaseModel):
    tasks: List[Task]
    planned_duration: int


class CompleteSessionRequest(BaseModel):
    actual_duration: int
    distractions_blocked: int = 0
    notes: Optional[str] = None

def _parse_oid(session_id: str) -> PydanticObjectId:
    try:
        return PydanticObjectId(session_id)
    except:
        raise HTTPException(400, "Invalid session ID")


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
    try:
        oid = PydanticObjectId(session_id)
    except:
        raise HTTPException(400, "Invalid session ID")

    session = await StudySession.find_one(
        StudySession.id == oid,
        StudySession.user.id == current_user.id
    )
    if not session:
        raise HTTPException(404, "Session not found")
    return session

# Create study session

@router.post("/", status_code=201)
async def create_study_session(
    req: CreateSessionRequest,
    current_user: User = Depends(get_current_user)
):
    # 1) insert your session
    session = StudySession(
        user=current_user,
        tasks=req.tasks,
        planned_duration=req.planned_duration,
        start_time=datetime.utcnow()
    )
    await session.insert()

    # 2) pin it on the user
    current_user.current_session = session
    await current_user.save()

    # 3) build a *pure* dict to return
    payload = {
      "_id": str(session.id),
      "user": str(session.user.id),
      "tasks": [t.dict() for t in session.tasks],
      "planned_duration": session.planned_duration,
      "actual_duration": session.actual_duration,
      "start_time": session.start_time.isoformat(),
      "end_time": session.end_time and session.end_time.isoformat(),
      "is_paused": session.is_paused,
      "paused_at": session.paused_at and session.paused_at.isoformat(),
      "total_paused": session.total_paused,
      "distractions_blocked": session.distractions_blocked,
      "notes": session.notes,
    }

    return JSONResponse(status_code=201, content=payload)

# Complete study session
@router.post("/{session_id}/complete")
async def complete_study_session(
    session_id: str,
    req: CompleteSessionRequest,
    current_user: User = Depends(get_current_user)
):
    oid = _parse_oid(session_id)
    session = await StudySession.find_one(
        StudySession.id == oid,
        StudySession.user.id == current_user.id
    )
    if not session:
        raise HTTPException(404, "Session not found or not yours")

    session.end_time = datetime.utcnow()
    session.actual_duration = req.actual_duration
    session.distractions_blocked = req.distractions_blocked
    session.notes = req.notes

    remaining = req.actual_duration
    for t in session.tasks:
        if t.duration <= remaining:
            t.completed = True
            remaining -= t.duration
        else:
            break

    await session.save()

    # bump user stats
    await current_user.update({"$inc": {
        "total_focus_time": session.actual_duration,
        "weekly_focus_time": session.actual_duration,
        "monthly_focus_time": session.actual_duration
    }})
    current_user.study_stats.append(StudyStat(
        date=datetime.utcnow(),
        focus_time=session.actual_duration,
        sessions=1,
        distractions_blocked=req.distractions_blocked
    ))
    current_user.current_session = None
    await current_user.save()

    return {"message": "Study session completed successfully"}


@router.post("/{session_id}/resume")
async def resume_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    oid = _parse_oid(session_id)
    session = await StudySession.find_one(
        StudySession.id == oid,
        StudySession.user.id == current_user.id
    )
    if not session:
        raise HTTPException(404, "Session not found or not yours")

    if not session.is_paused:
        raise HTTPException(400, "Not paused")

    paused_time = datetime.utcnow() - session.paused_at
    session.total_paused += int(paused_time.total_seconds())  # int += int
    session.is_paused = False
    session.paused_at = None
    await session.save()
    return {"message": "Resumed"}


@router.post("/{session_id}/pause")
async def pause_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    oid = _parse_oid(session_id)
    session = await StudySession.find_one(
        StudySession.id == oid,
        StudySession.user.id == current_user.id
    )
    if not session:
        raise HTTPException(404, "Session not found or not yours")

    if session.is_paused:
        raise HTTPException(400, "Already paused")

    session.is_paused = True
    session.paused_at = datetime.utcnow()
    await session.save()
    return {"message": "Paused"}


@router.post("/{session_id}/heartbeat")
async def heartbeat(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    oid = _parse_oid(session_id)
    session = await StudySession.find_one(
        StudySession.id == oid,
        StudySession.user.id == current_user.id
    )
    if not session:
        raise HTTPException(404, "Session not found or not yours")

    session.last_heartbeat = datetime.utcnow()
    await session.save()
    return {"message": "Heartbeat received"}