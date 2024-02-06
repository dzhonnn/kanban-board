from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Notes
from src.schemas.token import Status
from src.schemas.notes import NoteOutSchema


async def get_note(note_id, current_user) -> NoteOutSchema:
    try:
        db_note = await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note \
                            {note_id} not found")
    if db_note.section.author.id == current_user.id:
        return db_note
    return HTTPException(status_code=403, detail="Not authorized to get note")


async def create_note(note, current_user) -> NoteOutSchema:
    note_dict = note.dict(exclude_unset=True)
    note_obj = await Notes.create(**note_dict)
    return await NoteOutSchema.from_tortoise_orm(note_obj)


async def update_note(db_note, note) -> NoteOutSchema:
    try:
        note_dict = note.dict(exclude_unset=True)
        await Notes.filter(id=db_note.id).update(**note_dict)
        return await NoteOutSchema.from_queryset_single(Notes.get(id=db_note.id))
    except IntegrityError:
        raise HTTPException(status_code=404, detail=f"Section not found")


async def delete_note(db_note) -> Status:
    await Notes.filter(id=db_note.id).delete()
    return Status(message=f"Deleted note {db_note.id}")
