from beanie import Document
from typing import Dict
from models.Challenge import TierName, TierRequirement
from models.Challenge import ProgressUnit


class Milestone(Document):
    title: str
    description: str
    tiers: Dict[TierName, TierRequirement]
    progress_unit: ProgressUnit

    class Settings:
        name = "milestones"