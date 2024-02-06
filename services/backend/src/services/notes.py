from src.crud.notes import get_note, create_note, update_note, delete_note
from src.schemas.token import Status
from src.schemas.notes import NoteOutSchema


async def get_note_service(note_id, current_user) -> NoteOutSchema:
    return await get_note(note_id, current_user)


async def create_note_service(note, current_user) -> NoteOutSchema:
    if current_user.section:
        for section in current_user.section:
            if section.id == note.section_id:
                return await create_note(note, current_user)
        return Status(message="Not authorized to create note")
    else:
        return Status(message="First need to create section")


async def update_note_service(note_id, note, current_user) -> NoteOutSchema:
    try:
        db_note = await get_note(note_id, current_user)
    except Exception as e:
        return Status(message=f"{e}")
    return await update_note(db_note, note)


async def delete_note_serivce(note_id, current_user):
    try:
        db_note = await get_note(note_id, current_user)
    except Exception as e:
        return Status(message=f"{e}")
    return await delete_note(db_note)
