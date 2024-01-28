from datetime import datetime
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Notes

NoteInSchema = pydantic_model_creator(
    Notes, name="NoteIn", exclude_readonly=True
)
NoteOutSchema = pydantic_model_creator(
    Notes, name="Note", exclude=["status.author.password", "status.author.email"]
)


class UpdateNote(BaseModel):
    title: str | None
    description: str | None
    comments: str | None
    deadline: datetime | str
    status_id: int | None
