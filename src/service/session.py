from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.infra.security.jwt import create_acess_token
from src.infra.security.jwt import expires_at
from src.models.token import TokenModel
from src.models.session import SessionModel
from src.repositorys.sessions import SessionRepository
from src.repositorys.user import UserRepository
from src.infra.security.password import verify_password



class LoginService:
    def __init__(self, session: AsyncSession, data: OAuth2PasswordRequestForm) -> None:
        self._database = SessionRepository(session)
        self._user_database = UserRepository(session)
        self._data = data

    async def execute(self):
        EXPIRES_DELTA = 60 # 1h
        user = await self._user_database.get(self._data.username)
        if not user:
            raise HTTPException(400, "Incorrect username or passowrd") #TODO Implement CustomException
        
        password = verify_password(self._data.password, user.hashed_password)
        if not password:
            raise HTTPException(400, "Incorrect username or password") # TODO same thing kkkk
        
        expires = expires_at(EXPIRES_DELTA)
        access_token = create_acess_token({"sub": user.username}, expires)
        await self._database.create(SessionModel(token=access_token, user_id=user.id, expires_at=expires))

        return TokenModel(
            access_token=access_token,
            expires_at=expires,
            token_type="Bearer"
        )
