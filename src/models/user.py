import re

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator


class UserModel(BaseModel):
    username:str = Field(min_length=1, max_length=50)
    email: EmailStr


class CreateUserModel(UserModel):
    password: str = Field(min_length=8, serialization_alias="hashed_password")

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        """
        Validates that the password meets complexity requirements:
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one digit
        - At least one special symbol
        The minimum length is handled by Field().
        """
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special symbol')

        return v

