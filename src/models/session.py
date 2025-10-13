from pydantic import BaseModel
from datetime import datetime


class SessionModel(BaseModel):
    token: str
    expires_at: datetime
    user_id: int

