from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.helpers.errors import ConflictException
from src.entitys.user import User
from src.models.user import CreateUserModel

class UserRepository:
    def __init__(self, session: AsyncSession):
        self._database = session

    async def get_by_email(self, email: str) -> User:
        q = select(User).where(User.email == email)
        result = await self._database.execute(q)
        return result.scalars().first()

    async def create(self, data: CreateUserModel) -> User:
        existing_user = await self.get_by_email(data.email)
        if existing_user:
            print("ENTROU AQUI")
            raise ConflictException("email", data.email)

        user = User(**data.model_dump(by_alias=True))

        self._database.add(user)
        await self._database.flush()
        await self._database.refresh(user)

        return user