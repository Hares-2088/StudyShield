import logging
from fastapi import APIRouter, HTTPException, Depends
from models.Challenge import Challenge, ChallengeType
from typing import List, Optional
from beanie import PydanticObjectId
from auth.dependencies import get_current_user
from models.User import User

router = APIRouter(prefix="/challenges", tags=["Challenges"])
logger = logging.getLogger("ChallengeController")


# Public endpoints (no auth required)
@router.get("/", response_model=List[Challenge])
async def get_challenges(
        challenge_type: Optional[ChallengeType] = None,
        is_limited: Optional[bool] = None
):
    logger.info("Fetching challenges with filters: challenge_type=%s, is_limited=%s", challenge_type, is_limited)
    query = {}
    if challenge_type:
        query["challenge_type"] = challenge_type
    if is_limited is not None:
        query["is_limited"] = is_limited
    challenges = await Challenge.find(query).to_list()
    logger.info("Fetched %d challenges", len(challenges))
    return challenges


@router.get("/daily", response_model=List[Challenge])
async def get_daily_challenges():
    logger.info("Fetching daily challenges")
    challenges = await Challenge.find(
        Challenge.challenge_type == ChallengeType.DAILY
    ).to_list()
    logger.info("Fetched %d daily challenges", len(challenges))
    return challenges


@router.get("/milestones", response_model=List[Challenge])
async def get_milestone_challenges():
    logger.info("Fetching milestone challenges")
    challenges = await Challenge.find(
        Challenge.challenge_type == ChallengeType.MILESTONE
    ).to_list()
    logger.info("Fetched %d milestone challenges", len(challenges))
    return challenges


@router.get("/{challenge_id}", response_model=Challenge)
async def get_challenge(challenge_id: str):
    logger.info("Fetching challenge with ID: %s", challenge_id)
    challenge = await Challenge.get(PydanticObjectId(challenge_id))
    if not challenge:
        logger.warning("Challenge with ID %s not found", challenge_id)
        raise HTTPException(status_code=404, detail="Challenge not found")
    logger.info("Fetched challenge: %s", challenge.title)
    return challenge


# Protected endpoints (admin only)
@router.post("/", response_model=Challenge, status_code=201)
async def create_challenge(
        challenge: Challenge,
        current_user: User = Depends(get_current_user)
):
    logger.info("Attempting to create a new challenge: %s", challenge.title)
    if not current_user.is_admin:
        logger.warning("Unauthorized access attempt by user: %s", current_user.email)
        raise HTTPException(status_code=403, detail="Admin access required")
    await challenge.insert()
    logger.info("Challenge created successfully: %s", challenge.title)
    return challenge


@router.post("/daily/seed-default")
async def seed_default_daily_challenges(
        current_user: User = Depends(get_current_user)
):
    logger.info("Seeding default daily challenges")
    if not current_user.is_admin:
        logger.warning("Unauthorized access attempt by user: %s", current_user.email)
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
    logger.info("Default daily challenges seeded successfully")
    return {"message": "Default daily challenges seeded"}