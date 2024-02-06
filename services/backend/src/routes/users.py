from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.services.users as user_service
from src.settings import get_settings, create_mq
from src.email_notifications.email_notify import send_reset_password_mail
from src.schemas.token import Status
from src.schemas.users import UserInSchema, UserOutSchema
from src.rabbitServer.mq import send

from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    decode_data,
)

router = APIRouter()


@router.post("/register", tags=["Auth"], response_model=UserOutSchema | Status)
async def create_user(user: UserInSchema) -> UserOutSchema:
    try:
        return await user_service.create_user_service(user)
    except Exception as e:
        return Status(message=f"{e}")


@router.post("/login", tags=["Auth"])
async def login(email: str, password: str):
    settings = get_settings()
    user_obj = await user_service.get_unauthorized_user_service(email=email)
    user_dict = user_obj.dict()
    username = user_dict["username"]
    user = OAuth2PasswordRequestForm(username=username, password=password)
    user = await user_service.validate_user_service(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False
    )

    return response


@router.post("/forgot_password", tags=["Reset password"])
async def forgot_password(email: str):
    settings = get_settings()
    try:
        db_user = await user_service.get_unauthorized_user_service(email=email)
        if db_user:
            access_token_expires = timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": email}, expires_delta=access_token_expires)
            url = f"http://localhost:8080/resetpassword?access_token={access_token}"
            await send_reset_password_mail(email, url, access_token_expires)
    except DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"User with email: {email} not found")


@router.get("/reset_password_template", include_in_schema=False)
async def reset_password_template(request: Request):
    settings = get_settings()
    try:
        token = request.query_params.get("access_token")
        return settings.templates.TemplateResponse(
            "reset_password.html",
            {
                "request": request,
                "access_token": token
            }
        )
    except Exception as e:
        Status(message=f"Need access token to reset password.\{e}")


@router.post("/reset_password", include_in_schema=False)
async def reset_password(request: Request, new_password: str = Form(...)):
    try:
        token = request.query_params.get("access_token")
        if token is None:
            return Status("Need token to reset password.")
        payload = await decode_data(token)
        email = payload.get("sub")
        await user_service.reset_password_service(email, new_password)
        return Status(message="Password changed")
    except Exception as e:
        return Status(message=f"Something went wrong.\{e}")


@router.post(
    "/user/export_send",
    dependencies=[Depends(get_current_user)],
    tags=["Export"]
)
async def send_exported_board(current_user: UserOutSchema = Depends(get_current_user)):
    channel = await create_mq()
    try:
        await send(channel, current_user.json())
        return Status(message="File sended.")
    except Exception as e:
        return Status(message=f"{e}")


@router.get(
    "/user/export_get",
    response_class=FileResponse,
    dependencies=[Depends(get_current_user)],
    tags=["Export"]
)
async def get_exported_board(current_user: UserOutSchema = Depends(get_current_user)):
    return FileResponse(path=f"board{current_user.id}.xml", filename=f"board{current_user.id}.xml")


@router.get(
    "/users/whoami",
    response_model=UserOutSchema,
    dependencies=[Depends(get_current_user)],
    tags=["Users"]
)
async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)):
    return current_user


@router.delete(
    "/users/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
    tags=["Users"]
)
async def delete_user(user_id: int, current_user: UserOutSchema = Depends(get_current_user)) -> Status:
    return await user_service.delete_user_service(user_id, current_user)
