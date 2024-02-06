from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError

import src.services.notes as notes_service
from src.auth.jwthandler import get_current_user
from src.schemas.notes import NoteOutSchema, NoteInSchema, UpdateNote
from src.schemas.token import Status
from src.schemas.users import UserOutSchema

router = APIRouter()


@router.get(
    "/note/{note_id}",
    response_model=NoteOutSchema,
    dependencies=[Depends(get_current_user)],
    tags=["Notes"]
)
async def get_note(note_id: int, user: UserOutSchema = Depends(get_current_user)) -> NoteOutSchema:
    return await notes_service.get_note_service(note_id, user)


@router.post(
    "/note",
    response_model=NoteOutSchema | Status,
    dependencies=[Depends(get_current_user)],
    tags=["Notes"]
)
async def create_note(
    note: NoteInSchema,
    current_user: UserOutSchema = Depends(get_current_user)
) -> NoteOutSchema | Status:
    try:
        return await notes_service.create_note_service(note, current_user)
    except Exception as e:
        return Status(message=f"{e}")


@router.patch(
    "/note/{note_id}",
    dependencies=[Depends(get_current_user)],
    response_model=NoteOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
    tags=["Notes"]
)
async def update_note(
    note_id: int,
    note: UpdateNote,
    current_user: UserOutSchema = Depends(get_current_user)
) -> NoteOutSchema:
    return await notes_service.update_note_service(note_id, note, current_user)


@router.delete(
    "/note/{note_id}",
    dependencies=[Depends(get_current_user)],
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    tags=["Notes"]
)
async def delete_note(
    note_id: int,
    current_user: UserOutSchema = Depends(get_current_user)
):
    return await notes_service.delete_note_serivce(note_id, current_user)
