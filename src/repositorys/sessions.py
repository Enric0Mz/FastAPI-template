from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy import update
from datetime import datetime
from datetime import timezone

from src.infra.security.jwt import expires_at as expires_at_
from src.entitys.session import Session
from src.entitys.user import User
from src.models.session import SessionModel


class SessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._database = session

    async def get_by_token(self, token: str):
        q = (
            select(Session)
            .join(User, Session.user_id == User.id)
            .where(
                and_(
                    Session.token == token,
                    Session.expires_at > datetime.now(timezone.utc),
                    User.inactive.is_(None)
                )
            )
        )

        result = await self._database.execute(q)

        return result.scalars().first()

    async def create(self, data: SessionModel) -> Session | None:

        session = Session(**data.model_dump(by_alias=True))

        self._database.add(session)
        await self._database.flush()
        await self._database.refresh(session)

        return session

    async def refresh(self, user_id: int, expires_delta: int) -> Session | None:
        q = (
            update(Session)
            .where(Session.user_id == user_id)
            .values(expires_at=expires_at_(expires_delta))
            .returning(Session)
        )
        result = await self._database.execute(q)
        return result.scalars().first()
