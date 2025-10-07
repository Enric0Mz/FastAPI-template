from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.security.password import hash_password
from src.repositorys.user import UserRepository
from src.models.user import CreateUserModel

class CreateUserService:
    def __init__(self, session: AsyncSession, data: CreateUserModel) -> None:
        self._repository = UserRepository(session)
        self._data = data

    async def execute(self):
        self._data.password = hash_password(self._data.password)
        result = await self._repository.create(self._data)
        return result
