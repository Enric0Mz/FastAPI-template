from pydantic import BaseModel
from datetime import datetime

class TokenModel(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime
