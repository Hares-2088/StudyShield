from typing import List, Type

import motor.motor_asyncio
from beanie import init_beanie, Document
from models.Challenge import Challenge
from models.ShopItem import ShopItem
from models.User import User
from models.Milestone import Milestone
from models.StudySession import StudySession
from config import Config
import logging
from pymongo.errors import ConnectionFailure, PyMongoError

# Configure logging
logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.client = None
        self.database = None

    async def connect(self):
        """Connect to MongoDB with retry logic"""
        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                self.client = motor.motor_asyncio.AsyncIOMotorClient(
                    Config.MONGO_URI,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000
                )
                self.database = self.client[Config.MONGO_DB_NAME]

                # Test the connection
                await self.client.admin.command('ping')
                logger.info("✅ Successfully connected to MongoDB")
                return True

            except ConnectionFailure as e:
                logger.warning(
                    f"⚠️ Connection attempt {attempt + 1}/{max_retries} failed: {str(e)}"
                )
                if attempt < max_retries - 1:
                    import asyncio
                    await asyncio.sleep(retry_delay)
                continue
            except PyMongoError as e:
                logger.error(f"❌ MongoDB error: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"❌ Unexpected error: {str(e)}")
                raise

        logger.error("❌ Failed to connect to MongoDB after multiple attempts")
        return False

    async def initialize_collections(self):
        """Initialize all Beanie document models"""
        try:
            # Import models here to avoid circular imports
            from models.User import User
            from models.Challenge import Challenge
            from models.ShopItem import ShopItem
            from models.Milestone import Milestone
            from models.StudySession import StudySession

            document_models = [
                User,
                Challenge,
                ShopItem,
                Milestone,
                StudySession
            ]

            # Initialize Beanie with the document models
            await init_beanie(
                database=self.database,
                document_models=document_models
            )

            # Verify collections exist
            collection_names = await self.database.list_collection_names()
            logger.info(f"Available collections: {collection_names}")

            logger.info("Database collections initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize collections: {str(e)}", exc_info=True)
            return False

    async def close(self):
        """Close the MongoDB connection"""
        try:
            if self.client:
                self.client.close()
                logger.info("🔌 MongoDB connection closed")
        except Exception as e:
            logger.error(f"❌ Error closing connection: {str(e)}")


# Global database instance
db = Database()


async def init_db():
    """Initialize the database connection and collections"""
    try:
        # First connect to MongoDB
        if not await db.connect():
            raise ConnectionError("Failed to establish database connection")

        # Then initialize Beanie with models
        if not await db.initialize_collections():
            raise RuntimeError("Failed to initialize database collections")

        logger.info("✅ Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}", exc_info=True)
        raise