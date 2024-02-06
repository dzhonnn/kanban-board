from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from tortoise.exceptions import DoesNotExist

from src.settings import get_settings
from src.schemas.token import TokenData
from src.database.models import Users
from src.schemas.users import UserOutSchema


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization: str = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            else:
                return None
        return param


def create_access_token(data: dict, expires_delta: timedelta | None):
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def get_current_user(token: str = Depends(OAuth2PasswordBearerCookie(token_url="/login"))):
    settings = get_settings()
    credentials_exceptions = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exceptions
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exceptions

    try:
        user = await UserOutSchema.from_queryset_single(
            Users.get(username=token_data.username)
        )
    except DoesNotExist:
        raise credentials_exceptions

    return user


async def decode_data(data):
    settings = get_settings()
    decoded_data = jwt.decode(data, settings.SECRET_KEY,
                              algorithms=[settings.ALGORITHM])
    return decoded_data
