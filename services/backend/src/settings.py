import asyncio
from os import environ
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pathlib import Path
from src.rabbitServer.mq import RMQ, make_connection


class Settings():
    SECRET_KEY = environ.get("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    parent_directory = Path(__file__).parent
    templates_path = parent_directory.parent / "email_templates"
    templates = Jinja2Templates(directory=templates_path)


async def create_mq():
    mq = RMQ()
    loop = asyncio.get_event_loop()
    channel = await make_connection(loop)
    mq.channel = channel
    return mq.channel


def get_settings() -> Settings:
    return Settings()


