from sqlalchemy.ext.asyncio import AsyncSession

from src.repositorys.health import HealthRepository
from src.models.health import HealthCheckResponseModel, HealthChekModel
from src.infra.database import POSTGRES_DB

class HealthService:
    def __init__(self, session: AsyncSession):
        self._repository = HealthRepository(session)

    async def execute(self):
        opened_conns = await self._repository.get_opened_conns(POSTGRES_DB)
        max_conns = await self._repository.get_max_conns()
        server_version = await self._repository.get_server_version()
        
        health_details = HealthChekModel(
            opened_conns=opened_conns,
            max_conns=max_conns,
            server_version=server_version
        )
        return HealthCheckResponseModel(
            api_status="healthy",
            details=health_details
        )
