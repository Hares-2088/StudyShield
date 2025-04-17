from beanie import Document
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from models import User


class Task(BaseModel):
    name: str
    duration: int  # minutes
    completed: bool = False

class StudySession(Document):
    user: "User"
    tasks: List[Task]
    planned_duration: int  # minutes
    actual_duration: Optional[int] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    distractions_blocked: int = 0
    notes: Optional[str] = None

    class Settings:
        name = "study_sessions"