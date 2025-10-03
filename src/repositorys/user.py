from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.entitys.user import User
from src.models.user import CreateUserModel

class UserRepository:
    def __init__(self, session: AsyncSession):
        self._database = session

    async def create(self, data: CreateUserModel) -> User:
        user = User(**data.model_dump(by_alias=True))

        self._database.add(user)
        await self._database.flush()
        await self._database.refresh(user)

        return user