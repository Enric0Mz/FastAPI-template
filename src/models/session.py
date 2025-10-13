from pydantic import BaseModel
from datetime import datetime

from src.models.user import UserModel

class SessionModel(BaseModel):
    token: str
    expires_at: datetime
    user_id: int


class SessionWithUserModel(BaseModel):
    session: SessionModel
    user: UserModel
