from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class HealthRepository:
    def __init__(self, session: AsyncSession):
        self._database = session

    async def get_opened_conns(self, database: str) -> int:
        result = await self._database.execute(text(f"SELECT count(*) FROM pg_stat_activity WHERE datname = '{database}';"))
        return result.scalar_one()
    
    async def get_max_conns(self) -> int:
        result = await self._database.execute(text("SHOW max_connections;"))
        return int(result.scalar_one())
    
    async def get_server_version(self) -> str:
        result = await self._database.execute(text("SHOW server_version;"))
        return result.scalar_one()
