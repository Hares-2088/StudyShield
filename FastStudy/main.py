import asyncio
import datetime
from _pydatetime import timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from auth.utils import get_password_hash
from config import Config
from database import init_db
from models.User import User, StudyStat
from models.Challenge import Challenge, ChallengeType, TierName
from models.ShopItem import ShopItem
from models.Milestone import Milestone
from models.StudySession import StudySession, Task

# ─── configure root logger ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("studyshield")

app = FastAPI(
    title="Study Shield API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

@app.get("/___debug")
async def __debug():
    print("🐞  __debug HIT")
    return {"debug": True}


# ─── CORS ───────────────────────────────────────────────────────────
origins = [
"http://localhost:5173",
"http://127.0.0.1:5173",
"https://focusbuddy.study",
"https://focusbuddy.study/"
]

app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_methods=["*"],
allow_headers=["*"],
allow_credentials=True,
)


# ─── 1) REQUEST/RESPONSE LOGGING ──────────────────────────────────
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"→ {request.method} {request.url}")      # <-- simple print so you definitely see it
    response = await call_next(request)
    print(f"← {response.status_code} {request.url}")  # <-- and print response code
    return response

# ─── 2) GLOBAL EXCEPTION HANDLER ─────────────────────────────────
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"💥 Exception on {request.method} {request.url}: {exc!r}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


# ─── now include your routers ───────────────────────────────────────
from routes.UserController import router as user_router
from routes.ChallengeController import router as challenge_router
from routes.ItemController import router as item_router
from routes.MilestoneController import router as milestone_router
from routes.StudySessionController import router as study_session_router, monitor_sessions
from auth.routes import router as auth_router

app.include_router(user_router)
app.include_router(challenge_router)
app.include_router(item_router)
app.include_router(milestone_router)
app.include_router(study_session_router)
app.include_router(auth_router)


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
                    image_url="https://images.unsplash.com/photo-1506784983877-45594efa4cbe"
                ),
                ShopItem(
                    title="Study Achievement Badges",
                    description="Unlock exclusive profile badges",
                    price=25,
                    image_url="https://images.unsplash.com/photo-1533928298208-27ff66555d8d"
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
                        date= datetime.utcnow() - timedelta(days=i),
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

        if Config.DEBUG:
            logger.info("Starting data seeding...")
            await seed_initial_data()
        else:
            logger.info("Skipping data seeding")

        logger.info("Starting session monitor...")
        asyncio.create_task(monitor_sessions())

    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
