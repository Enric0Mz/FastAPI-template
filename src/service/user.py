from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.security.password import hash_password
from src.repositorys.user import UserRepository
from src.models.user import CreateUserModel
from src.models.user import GoogleUserModel
from src.service.session import LoginService


class CreateUserService:
    def __init__(self, session: AsyncSession, data: CreateUserModel) -> None:
        self._repository = UserRepository(session)
        self._data = data

    async def execute(self):
        self._data.password = hash_password(self._data.password)
        result = await self._repository.create(self._data)
        return result


class CreateOrGetGoogleUser:
    def __init__(self, session: AsyncSession, data: GoogleUserModel):
        self._repository = UserRepository(session)
        self._data = data
        self._session = session

    async def execute(self):
        user_in_db = await self._repository.get_with_google_id(self._data.google_id)
        if user_in_db:
            return await LoginService(self._session, user_in_db).execute()

        new_user = await self._repository.create(self._data)
        return await LoginService(self._session, new_user).execute()
