from typing import List
from src.crud.sections import get_section, get_sections, create_section, update_section, delete_section
from src.schemas.section import SectionOutSchema


async def get_section_service(section_id, current_user) -> SectionOutSchema:
    return await get_section(section_id, current_user)


async def get_sections_service(current_user) -> List[SectionOutSchema]:
    return await get_sections(current_user)


async def create_section_service(section, current_user) -> SectionOutSchema:
    return await create_section(section, current_user)


async def update_section_service(section_id, section, current_user) -> SectionOutSchema:
    db_section = await get_section(section_id, current_user)
    return await update_section(db_section, section)


async def delete_section_service(section_id, current_user):
    db_section = await get_section(section_id, current_user)
    if len(db_section.dict(exclude_unset=True)["note"]) != 0:
        raise Exception("Section must not have notes")
    return await delete_section(db_section)
