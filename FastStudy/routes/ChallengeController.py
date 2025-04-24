from fastapi import APIRouter, HTTPException, Depends
from models.Challenge import Challenge, ChallengeType
from typing import List, Optional
from beanie import PydanticObjectId
from auth.dependencies import get_current_user
from models.User import User

router = APIRouter(prefix="/challenges", tags=["Challenges"])


# Public endpoints (no auth required)
@router.get("/", response_model=List[Challenge])
async def get_challenges(
        challenge_type: Optional[ChallengeType] = None,
        is_limited: Optional[bool] = None
):
    query = {}
    if challenge_type:
        query["challenge_type"] = challenge_type
    if is_limited is not None:
        query["is_limited"] = is_limited
    return await Challenge.find(query).to_list()


@router.get("/daily", response_model=List[Challenge])
async def get_daily_challenges():
    return await Challenge.find(
        Challenge.challenge_type == ChallengeType.DAILY
    ).to_list()


@router.get("/milestones", response_model=List[Challenge])
async def get_milestone_challenges():
    return await Challenge.find(
        Challenge.challenge_type == ChallengeType.MILESTONE
    ).to_list()


@router.get("/{challenge_id}", response_model=Challenge)
async def get_challenge(challenge_id: str):
    challenge = await Challenge.get(PydanticObjectId(challenge_id))
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge


# Protected endpoints (admin only)
@router.post("/", response_model=Challenge, status_code=201)
async def create_challenge(
        challenge: Challenge,
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    await challenge.insert()
    return challenge


@router.post("/daily/seed-default")
async def seed_default_daily_challenges(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    default_dailies = [
        Challenge(
            title="Study Session",
            description="Complete a 25-minute focused study session",
            coins=10,
            goal=1,
            challenge_type=ChallengeType.DAILY
        ),
        Challenge(
            title="No Distractions",
            description="Block 3 distracting websites during study time",
            coins=15,
            goal=3,
            challenge_type=ChallengeType.DAILY
        ),
    ]
    await Challenge.insert_many(default_dailies)
    return {"message": "Default daily challenges seeded"}