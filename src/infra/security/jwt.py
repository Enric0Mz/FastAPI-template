import jwt
import os
from typing import Optional

from jwt.exceptions import InvalidTokenError
from datetime import timedelta
from datetime import datetime
from datetime import timezone

from src.helpers.load_env import custom_loadenv


custom_loadenv()

SECRET_KEY = os.getenv("SECRET_JWT_KEY")
ALGORITH = os.getenv("JWT_ALGORITH")

def expires_at(expires_delta: timedelta) -> timedelta:
    return datetime.now(timezone.utc) + timedelta(minutes=expires_delta)


def create_acess_token(data: dict, expires_at: datetime):
    to_encode = data.copy()
    to_encode.update({"exp": expires_at})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITH)
