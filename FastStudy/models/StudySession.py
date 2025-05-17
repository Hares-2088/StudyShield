from typing import List, Optional
from datetime import datetime

from beanie import Document, Link
from pydantic import BaseModel, Field

class Task(BaseModel):
    name: str
    duration: int
    completed: bool = False

class StudySession(Document):
    # forward‐ref string, no import here
    user: Link["User"]

    tasks: List[Task]
    planned_duration: int
    actual_duration: Optional[int] = None

    start_time: datetime
    end_time: Optional[datetime] = None

    is_paused: bool = False
    paused_at: Optional[datetime] = None
    total_paused: int = Field(0, description="accumulated pause time, in seconds")
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow)

    distractions_blocked: int = 0
    notes: Optional[str] = None

    class Settings:
        name = "study_sessions"

# at bottom, teach Pydantic about User
from models.User import User
StudySession.model_rebuild()
# to avoid circular import issues