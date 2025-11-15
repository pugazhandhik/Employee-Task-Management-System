import os
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from functools import lru_cache


class Settings:
    MONGODB_URI: str = os.getenv(
        "MONGODB_URI",
        "mongodb+srv://pugazhandhik26_db_user:uBK178tMc2B9tHYc@cluster0.viwykuy.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=false"
    )
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "employee_task_db")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def get_database():
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        tlsCAFile=certifi.where()
    )
    return client[settings.DATABASE_NAME]
