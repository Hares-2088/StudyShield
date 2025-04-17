# Import models explicitly to avoid conflicts
from auth.utils import get_password_hash
from config import Config
from database import init_db
from models.User import User, StudyStat
from models.Challenge import Challenge, ChallengeType, TierName
from models.ShopItem import ShopItem
from models.Milestone import Milestone
from models.StudySession import StudySession, Task  # Make sure this exists

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import bcrypt

# Import routers with clearer names
from routes.UserController import router as user_router
from routes.ChallengeController import router as challenge_router
from routes.ItemController import router as item_router
from routes.MilestoneController import router as milestone_router
from routes.StudySession import router as study_session_router  # Renamed for clarity
from auth.routes import router as auth_router

import logging
import sys

# Update your logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Use stdout with proper encoding
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Study Shield API",
    description="API for Study Shield productivity application",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Cross-origin resource sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(user_router)
app.include_router(challenge_router)
app.include_router(item_router)
app.include_router(milestone_router)
app.include_router(study_session_router)
app.include_router(auth_router)

print(app.routes)  # Add this temporarily to see all registered routes

async def seed_initial_data():
    try:
        logger.info("Checking database for existing data...")

        # Seed challenges if the collection is empty
        if await Challenge.find_all().count() == 0:
            logger.info("Seeding challenges...")
            challenges = [
                Challenge(
                    title="Study Marathon",
                    description="Accumulate 2 hours of total study time today",
                    coins=30,
                    goal=120,  # minutes
                    challenge_type=ChallengeType.DAILY
                ),
                Challenge(
                    title="Subject Explorer",
                    description="Study 3 different subjects today",
                    coins=40,
                    goal=3,
                    challenge_type=ChallengeType.SPECIAL
                )
            ]
            await Challenge.insert_many(challenges)
            logger.info(f"Inserted {len(challenges)} challenges")

        # Seed milestones if the collection is empty
        if await Milestone.find_all().count() == 0:
            logger.info("Seeding milestones...")
            milestones = [
                Milestone(
                    title="Distraction Defender",
                    description="Block distracting websites",
                    tiers={
                        TierName.BRONZE: {"value": 25, "coins": 75, "claimed": False},
                        TierName.SILVER: {"value": 50, "coins": 150, "claimed": False},
                        TierName.GOLD: {"value": 100, "coins": 300, "claimed": False},
                        TierName.PLATINUM: {"value": 250, "coins": 500, "claimed": False}
                    },
                    progress_unit="blocks"
                )
            ]
            await Milestone.insert_many(milestones)
            logger.info(f"Inserted {len(milestones)} milestones")

        # Seed shop items if the collection is empty
        if await ShopItem.find_all().count() == 0:
            logger.info("Seeding shop items...")
            shop_items = [
                ShopItem(
                    title="Digital Productivity Planner",
                    description="Advanced digital planner for optimal productivity",
                    price=45,
                    image_url="https://images.unsplash.com/photo-1506784983877-45594efa4cbe",
                    category="tools"
                ),
                ShopItem(
                    title="Study Achievement Badges",
                    description="Unlock exclusive profile badges",
                    price=25,
                    image_url="https://images.unsplash.com/photo-1533928298208-27ff66555d8d",
                    category="cosmetic"
                )
            ]
            await ShopItem.insert_many(shop_items)
            logger.info(f"Inserted {len(shop_items)} shop items")

        # Seed test user if the User collection is empty
        if await User.find_all().count() == 0:
            logger.info("Seeding test user...")
            test_user = User(
                name="Test User",
                email="test@studyshield.com",
                password=get_password_hash("testpassword123"),
                coins=200,
                day_streak=5,
                longest_streak=10,
                blocked_websites=["twitter.com", "youtube.com"],
                total_focus_time=1250,  # minutes
                weekly_focus_time=360,
                monthly_focus_time=890,
                study_stats=[
                    StudyStat(
                        date=datetime.utcnow() - timedelta(days=i),
                        focus_time=60 + (i * 10),
                        sessions=2 + i,
                        distractions_blocked=3 + i
                    )
                    for i in range(7)  # Last 7 days
                ]
            )
            await test_user.create()
            logger.info("Created test user with realistic data")

            # Seed study sessions for the test user
            logger.info("Seeding study sessions...")
            study_sessions = [
                StudySession(
                    user=test_user,  # Directly use the User object
                    tasks=[
                        Task(name="Math", duration=45, completed=True),
                        Task(name="Reading", duration=30, completed=False)
                    ],
                    planned_duration=75,
                    actual_duration=60,
                    start_time=datetime.utcnow() - timedelta(hours=2),
                    end_time=datetime.utcnow() - timedelta(hours=1),
                    distractions_blocked=3,
                    notes="First session"
                )
            ]
            try:
                await StudySession.insert_many(study_sessions)
                logger.info(f"Successfully inserted {len(study_sessions)} StudySessions")
            except Exception as e:
                logger.error(f"StudySession insertion failed: {e}")
                logger.error(f"Error details: {e.__class__.__name__}: {str(e)}")
                raise

        logger.info("✅ Data seeding completed successfully!")

    except Exception as e:
        logger.error(f"❌ Error during data seeding: {str(e)}")
        raise
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Initializing database connection...")
        await init_db()

        # Use Config instead of settings
        if Config.DEBUG:  # Or add SEED_DATA to your Config
            logger.info("Starting data seeding...")
            await seed_initial_data()
        else:
            logger.info("Skipping data seeding")

    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise