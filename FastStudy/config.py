import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_DB_NAME = "StudyShield"
    MONGO_URI = os.getenv("MONGO_URI")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    SEED_DATA = os.getenv("SEED_DATA", "False").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")