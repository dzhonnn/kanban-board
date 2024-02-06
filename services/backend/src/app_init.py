from src.settings import create_mq
from src.database.register import init_orm, close_orm
from src.rabbitServer.mq import make_queue, recieve_message
import asyncio
from tortoise import Tortoise
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.config import TortoiseConfig

Tortoise.init_models(["src.database.models"], "models")

from src.routes import notes, sections, users


def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(users.router)
    app.include_router(notes.router)
    app.include_router(sections.router)

    @app.on_event("startup")
    async def start_message_consuming():
        channel = await create_mq()
        asyncio.ensure_future(make_queue(channel, recieve_message))

    @app.on_event("startup")
    async def init_tortoise():
        await init_orm(config=TortoiseConfig.get(), generate_schemas=False)

    @app.on_event("shutdown")
    async def close_tortoise():
        await close_orm()

    return app
