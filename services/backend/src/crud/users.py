from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.settings import get_settings
from src.database.models import Users
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


async def get_user(user_id, current_user) -> UserOutSchema:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User \
                            {user_id} not found")
    if db_user.id == current_user.id:
        return db_user
    else:
        raise HTTPException(
            status_code=403, detail=f"Not authorized to get user")


async def create_user(user) -> UserOutSchema:
    settings = get_settings()
    user.password = settings.pwd_context.encrypt(user.password)

    try:
        user_obj = await Users.create(**user.dict())
    except IntegrityError:
        raise HTTPException(
            status_code=401, detail=f"Sorry, that username or email already exists")

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def reset_password(db_user, new_password):
    settings = get_settings()
    user_dict = db_user.dict(exclude_unset=True)
    user_dict["password"] = settings.pwd_context.encrypt(new_password)
    await Users.filter(email=db_user.email).update(**user_dict)


async def delete_user(db_user) -> Status:
    await Users.filter(id=db_user.id).delete()
    return Status(message=f"User {db_user.id} deleted")
