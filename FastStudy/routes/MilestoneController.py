from fastapi import APIRouter, HTTPException, Depends
from models.Milestone import Milestone, TierName
from typing import List
from beanie import PydanticObjectId
from auth.dependencies import get_current_user
from models.User import User

router = APIRouter(prefix="/milestones", tags=["Milestones"])


# Get all milestones - public
@router.get("/", response_model=List[Milestone])
async def get_milestones():
    return await Milestone.find_all().to_list()


# Get single milestone - public
@router.get("/{milestone_id}", response_model=Milestone)
async def get_milestone(milestone_id: str):
    milestone = await Milestone.get(PydanticObjectId(milestone_id))
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return milestone


# Create milestone - admin only
@router.post("/", response_model=Milestone, status_code=201)
async def create_milestone(
        milestone: Milestone,
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    await milestone.insert()
    return milestone


# Seed default milestones - admin only
@router.post("/seed-default")
async def seed_default_milestones(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    default_milestones = [
        Milestone(
            title="Study Time Master",
            description="Accumulate study hours",
            tiers={
                TierName.BRONZE: {"value": 50, "coins": 100},
                TierName.SILVER: {"value": 100, "coins": 200},
                TierName.GOLD: {"value": 200, "coins": 300},
                TierName.PLATINUM: {"value": 500, "coins": 500},
            },
            progress_unit="hours"
        ),
    ]
    await Milestone.insert_many(default_milestones)
    return {"message": "Default milestones seeded"}