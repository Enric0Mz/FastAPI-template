from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import select, and_
from datetime import datetime
from datetime import timezone

from src.entitys.session import Session
from src.models.session import SessionModel

class SessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._database = session


    async def get_by_token(self, token: str):
        q = select(Session).where(and_(Session.token == token, Session.expires_at > datetime.now(timezone.utc())))

        result = await self._database.execute(q)

        return result.scalars().first()

    async def create(self, data: SessionModel) -> None:
        
        session = Session(**data.model_dump(by_alias=True))

        self._database.add(session)
        await self._database.flush()
        await self._database.refresh(session)

        return session
