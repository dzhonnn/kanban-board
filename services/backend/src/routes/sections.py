from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.sections as crud
from src.auth.jwthandler import get_current_user
from src.schemas.section import SectionOutSchema, SectionInSchema, UpdateSection
from src.schemas.token import Status
from src.schemas.users import UserOutSchema

router = APIRouter()


@router.get(
    "/sections{section_id}",
    response_model=SectionOutSchema,
    dependencies=[Depends(get_current_user)],
    tags=["Sections"]
)
async def get_section(section_id, user: UserOutSchema = Depends(get_current_user)):
    return await crud.get_section(section_id, user)


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
    return await crud.create_section(section, current_user)


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
    return await crud.update_section(section_id, section, user)


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
    return await crud.delete_section(section_id, current_user)
