from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional

from src.helpers.errors import ConflictException
from src.entitys.user import User
from src.models.user import CreateUserModel
from src.models.user import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._database = session

    async def get(
        self, email: Optional[str] = None, username: Optional[str] = None
    ) -> User | None:
        q = select(User).where(or_(User.email == email, User.username == username))
        result = await self._database.execute(q)
        return result.scalars().first()

    async def create(self, data: CreateUserModel) -> User:
        existing_user = await self.get(data.email, data.username)
        if existing_user:
            if existing_user.email == data.email:
                raise ConflictException("email", data.email)
            elif existing_user.username == data.username:
                raise ConflictException("username", data.username)

        user = User(**data.model_dump(by_alias=True))

        self._database.add(user)
        await self._database.flush()
        await self._database.refresh(user)

        return user

    async def get_with_google_id(self, google_id: str) -> User | None:
        q = select(User).where(User.google_id == google_id)

        result = await self._database.execute(q)

        return result.scalars().first()
