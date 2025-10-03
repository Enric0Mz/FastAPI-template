from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserModel(BaseModel):
    username: str
    email: EmailStr


class CreateUserModel(UserModel):
    password: str = Field(serialization_alias="hashed_password")

