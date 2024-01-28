import json
from datetime import timedelta
from typing import List
from dict2xml import dict2xml

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

from pathlib import Path

import src.crud.users as crud
from src.auth.users import validate_user
from src.email_notifications.email_notify import send_reset_password_mail
from src.database.models import Users
from src.schemas.token import Status
from src.schemas.users import UserInSchema, UserOutSchema
from src.rabbitServer.mq import mq

from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    decode_data,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

parent_directory = Path(__file__).parent
templates_path = parent_directory.parent / "email_templates"
templates = Jinja2Templates(directory=templates_path)

router = APIRouter()


@router.post("/register", tags=["Auth"], response_model=UserOutSchema)
async def create_user(user: UserInSchema) -> UserOutSchema:
    return await crud.create_user(user)


@router.post("/login", tags=["Auth"])
async def login(email: str, password: str):
    user_obj = await UserOutSchema.from_queryset_single(
        Users.get(email=email))
    user_dict = user_obj.dict()
    username = user_dict["username"]
    user = OAuth2PasswordRequestForm(username=username, password=password)
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
async def forgot_password(request: Request, email: str):
    try:
        db_user = Users.get(email=email)
        if db_user:
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": email}, expires_delta=access_token_expires)
            url = f"http://localhost:8080/resetpassword?access_token={access_token}"
            await send_reset_password_mail(email, url, access_token_expires)
    except DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"User with email: {email} not found")


@router.get("/reset_password_template", tags=["Reset password"])
async def reset_password_template(request: Request):
    try:
        token = request.query_params.get("access_token")
        return templates.TemplateResponse(
            "reset_password.html",
            {
                "request": request,
                "access_token": token
            }
        )
    except Exception as e:
        Status(message=f"Need access token to reset password.\{e}")


@router.post("/reset_password", tags=["Reset password"])
async def reset_password(request: Request, new_password: str = Form(...)):
    try:
        token = request.query_params.get("access_token")
        if token is None:
            return Status("Need token to reset password.")
        payload = await decode_data(token)
        email = payload.get("sub")
        await crud.reset_password(email, new_password)
        return Status(message="Password changed")
    except Exception as e:
        return Status(message=f"Something went wrong.\{e}")


@router.post(
    "/user/export_send",
    dependencies=[Depends(get_current_user)],
    tags=["Export"]
)
async def send_exported_board(current_user: UserOutSchema = Depends(get_current_user)):
    try:
        await mq.send(current_user.json())
        return Status(message="File sended.")
    except Exception as e:
        return Status(message=e)


@router.get(
    "/user/export_get",
    response_class=FileResponse,
    dependencies=[Depends(get_current_user)],
    tags=["Export"]
)
async def get_exported_board(current_user: UserOutSchema = Depends(get_current_user)):
    return FileResponse(path=f"board.xml", filename=f"board.xml")


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
    return await crud.delete_user(user_id, current_user)
