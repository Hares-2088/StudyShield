from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from auth.dependencies import get_current_user
from models.User import User, ChallengeProgress, MilestoneProgress, StudyStat
from models.Challenge import Challenge, ChallengeType
from models.Milestone import Milestone
from models.ShopItem import ShopItem
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from bson import ObjectId
import math

router = APIRouter(prefix="/users", tags=["Users"])


# Helper functions
async def get_user_or_404(user_id: str) -> User:
    user = await User.get(ObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Request models
class AddCoinsRequest(BaseModel):
    amount: int


class BlockWebsiteRequest(BaseModel):
    website: str


class UpdateFocusTimeRequest(BaseModel):
    minutes: int


# User profile endpoints
@router.get("/me", response_model=User)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[User])
async def get_users(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return await User.find_all().to_list()


@router.get("/{user_id}", response_model=User)
async def get_user(
        user_id: str,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Can only view your own profile")
    return await get_user_or_404(user_id)


@router.post("/", response_model=User, status_code=201)
async def create_user(
        user: User,
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    await user.insert()
    return user


# User management endpoints
@router.post("/{user_id}/add-coins", response_model=User)
async def add_coins(
        user_id: str,
        request: AddCoinsRequest,
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    user = await get_user_or_404(user_id)
    user.coins += request.amount
    await user.save()
    return user


# Challenge progress endpoints
@router.get("/{user_id}/challenges", response_model=List[ChallengeProgress])
async def get_user_challenges(
        user_id: str,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Can only view your own challenges")

    user = await get_user_or_404(user_id)
    return user.challenges


@router.post("/{user_id}/challenges/{challenge_id}/progress")
async def update_challenge_progress(
        user_id: str,
        challenge_id: str,
        progress: int,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only update your own challenges")

    user = await get_user_or_404(user_id)
    challenge = await Challenge.get(ObjectId(challenge_id))

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    challenge_progress = next(
        (cp for cp in user.challenges if str(cp.challenge_id.id) == challenge_id),
        None
    )

    if not challenge_progress:
        challenge_progress = ChallengeProgress(
            challenge_id=ObjectId(challenge_id),
            progress=progress,
            is_completed=progress >= challenge.goal
        )
        user.challenges.append(challenge_progress)
    else:
        challenge_progress.progress += progress
        challenge_progress.is_completed = challenge_progress.progress >= challenge.goal
        challenge_progress.last_updated = datetime.utcnow()

    if challenge_progress.is_completed and challenge_progress.progress == progress:
        coins_to_add = challenge.coins
        if challenge.challenge_type == ChallengeType.DAILY:
            streak_bonus = 1 + min(math.floor(user.day_streak / 7), 2)
            coins_to_add = math.floor(challenge.coins * streak_bonus)
        user.coins += coins_to_add

    await user.save()
    return challenge_progress


# Milestone endpoints
@router.get("/{user_id}/milestones", response_model=List[MilestoneProgress])
async def get_user_milestones(
        user_id: str,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Can only view your own milestones")

    user = await get_user_or_404(user_id)
    return user.milestones


@router.post("/{user_id}/milestones/{milestone_id}/claim-tier")
async def claim_milestone_tier(
        user_id: str,
        milestone_id: str,
        tier_name: str,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only claim your own milestones")

    user = await get_user_or_404(user_id)
    milestone = await Milestone.get(ObjectId(milestone_id))

    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    milestone_progress = next(
        (mp for mp in user.milestones if str(mp.milestone_id.id) == milestone_id),
        None
    )

    if not milestone_progress:
        raise HTTPException(status_code=400, detail="Milestone not started by user")

    tier = milestone.tiers.get(tier_name)
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")

    if milestone_progress.progress < tier.value:
        raise HTTPException(status_code=400, detail="Tier requirements not met")

    if tier.claimed:
        raise HTTPException(status_code=400, detail="Tier already claimed")

    user.coins += tier.coins
    tier.claimed = True
    milestone_progress.current_tier = tier_name

    next_tier = None
    if tier_name == "bronze":
        next_tier = "silver"
    elif tier_name == "silver":
        next_tier = "gold"
    elif tier_name == "gold":
        next_tier = "platinum"

    if next_tier and next_tier in milestone.tiers:
        milestone_progress.next_goal = milestone.tiers[next_tier].value
    else:
        milestone_progress.next_goal = None

    await user.save()
    return {"message": "Tier reward claimed successfully"}


# Shop endpoints
@router.post("/{user_id}/shop/items/{item_id}/purchase")
async def purchase_item(
        user_id: str,
        item_id: str,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only purchase for yourself")

    user = await get_user_or_404(user_id)
    item = await ShopItem.get(ObjectId(item_id))

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if user.coins < item.price:
        raise HTTPException(status_code=400, detail="Not enough coins")

    user.coins -= item.price
    user.purchased_items.append(item)
    await user.save()
    return {"message": "Item purchased successfully"}


# Study stats endpoints
@router.get("/{user_id}/stats", response_model=List[StudyStat])
async def get_user_stats(
        user_id: str,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Can only view your own stats")

    user = await get_user_or_404(user_id)
    return user.study_stats


@router.post("/{user_id}/stats/update-focus")
async def update_focus_time(
        user_id: str,
        request: UpdateFocusTimeRequest,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only update your own stats")

    user = await get_user_or_404(user_id)
    user.total_focus_time += request.minutes
    user.weekly_focus_time += request.minutes
    user.monthly_focus_time += request.minutes

    today = datetime.utcnow().date()
    last_active = user.last_active_date.date() if user.last_active_date else None

    if last_active == today:
        pass
    elif last_active == today - timedelta(days=1):
        user.day_streak += 1
        user.longest_streak = max(user.longest_streak, user.day_streak)
    else:
        user.day_streak = 1

    user.last_active_date = datetime.utcnow()

    today_stat = next(
        (stat for stat in user.study_stats if stat.date.date() == today),
        None
    )

    if today_stat:
        today_stat.focus_time += request.minutes
        today_stat.sessions += 1
    else:
        user.study_stats.append(StudyStat(
            date=datetime.utcnow(),
            focus_time=request.minutes,
            sessions=1
        ))

    await user.save()
    return {"message": "Focus time updated successfully"}


# Blocked websites endpoints
@router.get("/{user_id}/blocked-websites", response_model=List[str])
async def get_blocked_websites(
        user_id: str,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Can only view your own blocked sites")

    user = await get_user_or_404(user_id)
    return user.blocked_websites


@router.post("/{user_id}/blocked-websites/add")
async def add_blocked_website(
        user_id: str,
        request: BlockWebsiteRequest,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only modify your own blocked sites")

    user = await get_user_or_404(user_id)
    if request.website in user.blocked_websites:
        raise HTTPException(status_code=400, detail="Website already blocked")

    user.blocked_websites.append(request.website)
    await user.save()
    return {"message": "Website blocked successfully"}


@router.delete("/{user_id}/blocked-websites/remove")
async def remove_blocked_website(
        user_id: str,
        website: str,
        current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only modify your own blocked sites")

    user = await get_user_or_404(user_id)
    if website not in user.blocked_websites:
        raise HTTPException(status_code=404, detail="Website not in blocked list")

    user.blocked_websites.remove(website)
    await user.save()
    return {"message": "Website unblocked successfully"}