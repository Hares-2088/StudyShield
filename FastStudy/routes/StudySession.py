from fastapi import APIRouter, HTTPException, Depends
from models.StudySession import StudySession
from models.User import User
from models.StudySession import Task
from typing import List
from datetime import datetime
from bson import ObjectId
from typing import Optional
from auth.dependencies import get_current_user

router = APIRouter(prefix="/study-sessions", tags=["Study Sessions"])


# Get user's study sessions - authenticated user only
@router.get("/", response_model=List[StudySession])
async def get_study_sessions(current_user: User = Depends(get_current_user)):
    return await StudySession.find(
        StudySession.user.id == current_user.id
    ).sort(-StudySession.start_time).to_list()


# Create study session - authenticated user only
@router.post("/", response_model=StudySession, status_code=201)
async def create_study_session(
        tasks: List[Task],
        planned_duration: int,
        current_user: User = Depends(get_current_user)
):
    session = StudySession(
        user=current_user.id,
        tasks=tasks,
        planned_duration=planned_duration,
        start_time=datetime.utcnow()
    )
    await session.insert()
    return session


# Complete study session - authenticated user only
@router.post("/{session_id}/complete")
async def complete_study_session(
        session_id: str,
        actual_duration: int,
        distractions_blocked: int = 0,
        notes: Optional[str] = None,
        current_user: User = Depends(get_current_user)
):
    session = await StudySession.get(ObjectId(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Verify session belongs to current user
    if str(session.user.id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to complete this session")

    session.end_time = datetime.utcnow()
    session.actual_duration = actual_duration
    session.distractions_blocked = distractions_blocked
    session.notes = notes

    # Mark completed tasks
    for task in session.tasks:
        if task.duration <= actual_duration:
            task.completed = True
            actual_duration -= task.duration
        else:
            break

    await session.save()

    # Update user stats
    await current_user.update({"$inc": {
        "total_focus_time": session.actual_duration,
        "weekly_focus_time": session.actual_duration,
        "monthly_focus_time": session.actual_duration
    }})

    return {"message": "Study session completed successfully"}