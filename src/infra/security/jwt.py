import jwt
import os

from datetime import timedelta
from datetime import datetime
from datetime import timezone

from src.helpers.load_env import custom_loadenv
from src.helpers.errors import UnauthenticatedExpection


custom_loadenv()

SECRET_KEY = os.getenv("SECRET_JWT_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "FALLBACK_ALGORITHM")

def expires_at(expires_delta: int) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=expires_delta)


def create_access_token(data: dict, expires_at: datetime):
    to_encode = data.copy()
    to_encode.update({"exp": expires_at})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise UnauthenticatedExpection("Invalid authorization token")
        return email
    except jwt.ExpiredSignatureError:
        raise UnauthenticatedExpection("Expired authorization token")
    except jwt.InvalidTokenError:
        raise UnauthenticatedExpection("Invalid authorization token")