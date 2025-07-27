from enum import Enum
from typing import List, Optional
from datetime import datetime

from beanie import Document, Link
from pydantic import BaseModel, Field, EmailStr

from models.Challenge import Challenge, TierName
from models.ShopItem import ShopItem
from models.Milestone import Milestone

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class ChallengeProgress(BaseModel):
    challenge_id: Link[Challenge]
    progress: int = 0
    is_completed: bool = False
    redeemed: bool = False
    redeemed_at: Optional[datetime] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class MilestoneProgress(BaseModel):
    milestone_id: Link[Milestone]
    progress: int = 0
    current_tier: Optional[TierName] = None
    next_goal: Optional[int] = None
    claimed_tiers: List[TierName] = []

class StudyStat(BaseModel):
    date: datetime
    focus_time: int
    sessions: int
    distractions_blocked: int = 0

class User(Document):
    name: str
    email: EmailStr
    password: str
    coins: int = 0
    day_streak: int = 0
    longest_streak: int = 0
    streak_multiplier: float = 1
    last_active_date: Optional[datetime] = None

    challenges: List[ChallengeProgress] = []
    milestones: List[MilestoneProgress] = []
    purchased_items: List[Link[ShopItem]] = []
    blocked_websites: List[str] = []

    total_focus_time: int = 0
    weekly_focus_time: int = 0
    today_focus_time: int = 0
    monthly_focus_time: int = 0

    study_stats: List[StudyStat] = []

    #We are going to use this to track the current study session and make it optional
    # forward‐ref string, no import here
    current_session: Optional[Link["StudySession"]] = None

    is_active: bool = True
    role: UserRole = UserRole.USER
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"
        use_state_management = True

    @classmethod
    async def create_user(cls, user_data: dict):
        from auth.utils import get_password_hash
        user_data["password"] = get_password_hash(user_data["password"])
        return await cls(**user_data).create()

# at bottom, teach Pydantic about StudySession
from models.StudySession import StudySession
User.model_rebuild()
