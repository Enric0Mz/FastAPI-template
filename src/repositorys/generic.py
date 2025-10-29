from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.entitys.base import Base


class GenericRepository:
    def __init__(self, session: AsyncSession):
        self._database = session

    async def clear_tables(self) -> int:
        tables = ", ".join(table.name for table in Base.metadata.tables.values())
        return await self._database.execute(
            text(f"TRUNCATE TABLE {tables} RESTART IDENTITY CASCADE;")
        )
