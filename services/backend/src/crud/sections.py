from typing import List
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Sections
from src.schemas.token import Status
from src.schemas.section import SectionOutSchema


async def get_section(section_id, current_user) -> SectionOutSchema:
    try:
        db_section = await SectionOutSchema.from_queryset_single(Sections.get(id=section_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note \
                            {section_id} not found")
    if db_section.author_id == current_user.id:
        return db_section
    return HTTPException(status_code=403, detail="Not authorized to get note")


async def get_sections(current_user) -> List[SectionOutSchema]:
    return await SectionOutSchema.from_queryset(Sections.filter(author_id=current_user.id))


async def create_section(section, current_user) -> SectionOutSchema:
    section_dict = section.dict(exclude_unset=True)
    section_dict["author_id"] = current_user.id
    section_obj = await Sections.create(**section_dict)
    return await SectionOutSchema.from_tortoise_orm(section_obj)


async def update_section(db_section, section) -> SectionOutSchema:
    await Sections.filter(id=db_section.id).update(**section.dict(exclude_unset=True))
    return await SectionOutSchema.from_queryset_single(Sections.get(id=db_section.id))


async def delete_section(db_section) -> Status:
    await Sections.filter(id=db_section.id).delete()
    return Status(message=f"Deleted section {db_section.id}")
