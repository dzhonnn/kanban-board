import re
from src.auth.users import validate_user
from src.auth.users import get_user as get_unauthorized_user
from src.crud.users import get_user, create_user, reset_password, delete_user


async def get_unauthorized_user_service(username=None, email=None, user_id=None):
    return await get_unauthorized_user(username, email, user_id)


async def get_user_service(user_id, current_user):
    return await get_user(user_id, current_user)


async def validate_user_service(user):
    return await validate_user(user)


async def create_user_service(user):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise Exception("Incorrect email format")
    return await create_user(user)


async def reset_password_service(email, new_password):
    db_user = await get_unauthorized_user(email=email)
    await reset_password(db_user, new_password)


async def delete_user_service(user_id, current_user):
    db_user = await get_user(user_id, current_user)
    return await delete_user(db_user)
