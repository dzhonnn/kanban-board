from tortoise.contrib.pydantic import pydantic_model_creator
from src.database.models import Users

UserInSchema = pydantic_model_creator(
    Users, name="UserIn", exclude_readonly=True
)
UserOutSchema = pydantic_model_creator(
    Users, name="UserOut", exclude=["password"]
)
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User"
)
