from pydantic import BaseModel


class TokenData(BaseModel):
    username: str | None


class Status(BaseModel):
    message: str
