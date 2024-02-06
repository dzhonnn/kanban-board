from fastapi import HTTPException, status, Depends
from tortoise.exceptions import DoesNotExist

from src.settings import get_settings
from src.database.models import Users
from src.schemas.users import UserInSchema


def verify_password(plain_password, hashed_password):
    settings = get_settings()
    return settings.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    settings = get_settings()
    return settings.pwd_context.hash(password)


async def get_user(username=None, email=None, user_id=None):
    try:
        if username:
            db_user = await UserInSchema.from_queryset_single(Users.get(username=username))
        elif email:
            db_user = await UserInSchema.from_queryset_single(Users.get(email=email))
        elif user_id:
            db_user = await UserInSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return db_user


async def validate_user(user):
    db_user = await get_user(user.username)

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    return db_user
