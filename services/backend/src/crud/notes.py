from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Notes
from src.database.models import Sections
from src.schemas.token import Status
from src.schemas.notes import NoteOutSchema


async def get_note(note_id) -> NoteOutSchema:
    return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))


async def create_note(note, current_user) -> NoteOutSchema:
    if current_user.section:
        note_dict = note.dict(exclude_unset=True)
        # note_dict["status_id"] = current_user.section[0].id
        note_obj = await Notes.create(**note_dict)
        return await NoteOutSchema.from_tortoise_orm(note_obj)
    else:
        return Status(message="First need to create section")


async def update_note(note_id, note, current_user) -> NoteOutSchema:
    try:
        db_note = await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note \
                            {note_id} not found")

    if db_note.status.author.id == current_user.id:
        try:
            note_dict = note.dict(exclude_unset=True)
            await Notes.filter(id=note_id).update(**note_dict)
            return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
        except IntegrityError:
            raise HTTPException(status_code=404, detail=f"Section not found")

    return HTTPException(status_code=403, detail="Not authorized to update")


async def delete_note(note_id, current_user) -> Status:
    try:
        db_note = await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note \
                            {note_id} not found")

    if db_note.status.author.id == current_user.id:
        deleted_count = await Notes.filter(id=note_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Note \
                                {note_id} not found")
        return Status(message=f"Deleted note {note_id}")

    raise HTTPException(status_code=403, detail="Not authorized to delete")
