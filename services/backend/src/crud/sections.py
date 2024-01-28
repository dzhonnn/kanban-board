from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Sections
from src.schemas.token import Status
from src.schemas.section import SectionOutSchema


async def get_sections(current_user):
    return await SectionOutSchema.from_queryset(Sections.filter(author_id=current_user.id))

async def create_section(section, current_user) -> SectionOutSchema:
    section_dict = section.dict(exclude_unset=True)
    section_dict["author_id"] = current_user.id
    section_obj = await Sections.create(**section_dict)
    return await SectionOutSchema.from_tortoise_orm(section_obj)


async def update_section(section_id, section, current_user) -> SectionOutSchema:
    try:
        db_section = await SectionOutSchema.from_queryset_single(Sections.get(id=section_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Section \
            {section_id} not found")

    if db_section.author.id == current_user.id:
        await Sections.filter(id=section_id).update(**section.dict(exclude_unset=True))
        return await SectionOutSchema.from_queryset_single(Sections.get(id=section_id))

    return HTTPException(status_code=403, detail="Not authorized to update")


async def delete_section(section_id, current_user) -> Status:
    try:
        db_section = await SectionOutSchema.from_queryset_single(Sections.get(id=section_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Section \
            {section_id} not found")

    if db_section.author.id == current_user.id and len(db_section.dict(exclude_unset=True)["note"]) == 0:
        deleted_count = await Sections.filter(id=section_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Section \
                {section_id} not found")
        return Status(message=f"Deleted section {section_id}")
    else:
        return Status(message="Section must not have notes")
