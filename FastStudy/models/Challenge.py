from beanie import Document
from typing import Optional, Dict
from enum import Enum
from pydantic import BaseModel


class ChallengeType(str, Enum):
    DAILY = "daily"
    SPECIAL = "special"
    MILESTONE = "milestone"


class TierName(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


class Challenge(Document):
    title: str
    description: str
    coins: int
    goal: int
    challenge_type: ChallengeType
    is_limited: bool = False
    expires_in: Optional[int] = None  # in seconds

    class Settings:
        name = "challenges"

class ProgressUnit(str, Enum):
    HOURS = "hours"
    DAYS = "days"
    BLOCKS = "blocks"

class TierRequirement(BaseModel):
    value: int
    coins: int
