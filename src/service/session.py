from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.infra.security.jwt import create_access_token
from src.infra.security.jwt import expires_at
from src.models.token import TokenModel
from src.models.session import SessionModel
from src.repositorys.sessions import SessionRepository
from src.repositorys.user import UserRepository
from src.infra.security.password import verify_password
from src.helpers.errors import BadRequestException
from src.entitys.user import User


class LoginService:
    def __init__(
        self, session: AsyncSession, data: OAuth2PasswordRequestForm | User
    ) -> None:
        self._database = SessionRepository(session)
        self._user_database = UserRepository(session)
        self._data = data
        self._EXPIRES_DELTA = 60  # 1h

    async def execute(self):
        if isinstance(self._data, User):
            return await self.__google_handler()
        return await self.__local_handler()

    async def __local_handler(self):
        user = await self._user_database.get(self._data.username)
        if not user:
            raise BadRequestException("Incorrect username or password")

        password = verify_password(self._data.password, user.hashed_password)
        if not password:
            raise BadRequestException("Incorrect username or password")

        expires = expires_at(self._EXPIRES_DELTA)
        access_token = create_access_token({"sub": user.email}, expires)
        await self._database.create(
            SessionModel(token=access_token, user_id=user.id, expires_at=expires)
        )

        return TokenModel(
            access_token=access_token, expires_at=expires, token_type="Bearer"
        )

    async def __google_handler(self):
        expires = expires_at(self._EXPIRES_DELTA)
        access_token = create_access_token({"sub": self._data.email}, expires)
        await self._database.create(
            SessionModel(token=access_token, user_id=self._data.id, expires_at=expires)
        )
        return TokenModel(
            access_token=access_token, expires_at=expires, token_type="Bearer"
        )
