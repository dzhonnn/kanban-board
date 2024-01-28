import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from src.database.config import TORTOISE_ORM
from src.database.register import register_tortoise
from src.rabbitServer.mq import mq, make_connection

Tortoise.init_models(["src.database.models"], "models")

from src.routes import notes, sections, users

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

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.on_event("startup")
async def start_message_consuming():
    print("start")
    loop = asyncio.get_event_loop()
    channel = await make_connection(loop)
    mq.channel = channel
    asyncio.ensure_future(mq.make_queue(users.recieve_message))


@app.get("/")
async def home():
    return "Hello, World!"
