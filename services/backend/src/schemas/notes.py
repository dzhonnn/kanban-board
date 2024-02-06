from datetime import datetime
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Notes

NoteInSchema = pydantic_model_creator(
    Notes, name="NoteIn", exclude=["section", "id"]
)
NoteOutSchema = pydantic_model_creator(
    Notes, name="Note", exclude=["section.author.password", "section.author.email"]
)


class UpdateNote(BaseModel):
    title: str | None
    description: str | None
    comments: str | None
    deadline: datetime | str
    section_id: int | None
