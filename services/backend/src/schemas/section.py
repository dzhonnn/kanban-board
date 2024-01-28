from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Sections

SectionInSchema = pydantic_model_creator(
    Sections, name="SectionIn", exclude=["author_id"], exclude_readonly=True
)

SectionOutSchema = pydantic_model_creator(
    Sections, name="Section", exclude=["author.password", "author.email"]
)


class UpdateSection(BaseModel):
    title: str | None
