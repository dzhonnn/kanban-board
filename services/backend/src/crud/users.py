from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Users
from src.schemas.token import Status
from src.schemas.users import UserOutSchema, UserInSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)

    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(
            status_code=401, detail=f"Sorry, that username or email already exists")

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def reset_password(email, new_password):
    try:
        user_obj = await UserInSchema.from_queryset_single(Users.get(email=email))
        user_dict = user_obj.dict(exclude_unset=True)
        user_dict["password"] = pwd_context.encrypt(new_password)
        await Users.filter(email=email).update(**user_dict)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Email \
                            {email} not found")


async def delete_user(user_id, current_user) -> Status:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User \
                            {user_id} not found")

    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User \
                                {user_id} not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
