from typing import List

from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

import src.services.sections as section_service
from src.auth.jwthandler import get_current_user
from src.schemas.section import SectionOutSchema, SectionInSchema, UpdateSection
from src.schemas.token import Status
from src.schemas.users import UserOutSchema

router = APIRouter()


@router.get(
    "/sections",
    response_model=List[SectionOutSchema],
    dependencies=[Depends(get_current_user)],
    tags=["Sections"]
)
async def get_sections(user: UserOutSchema = Depends(get_current_user)):
    return await section_service.get_sections_service(user)


@router.post(
    "/section",
    response_model=SectionOutSchema,
    dependencies=[Depends(get_current_user)],
    tags=["Sections"]
)
async def create_section(
    section: SectionInSchema,
    current_user: UserOutSchema = Depends(get_current_user)
) -> SectionOutSchema:
    return await section_service.create_section_service(section, current_user)


@router.patch(
    "/sections/{section_id}",
    dependencies=[Depends(get_current_user)],
    response_model=SectionOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
    tags=["Sections"]
)
async def update_section(
    section_id: int,
    section: UpdateSection,
    user: UserOutSchema = Depends(get_current_user)
) -> SectionOutSchema:
    return await section_service.update_section_service(section_id, section, user)


@router.delete(
    "/sections/{section_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    tags=["Sections"]
)
async def delete_section(
    section_id: int,
    current_user: UserOutSchema = Depends(get_current_user)
):
    try:
        return await section_service.delete_section_service(section_id, current_user)
    except Exception as e:
        return Status(message=f"{e}")
