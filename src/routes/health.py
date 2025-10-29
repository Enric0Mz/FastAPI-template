import os
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.service.health import HealthService
from src.models.health import HealthCheckResponseModel
from src.repositorys.generic import GenericRepository

from src.infra.database import get_db

ENV = os.getenv("ENVIROMENT", "production")

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


@router.get("/", response_model=HealthCheckResponseModel)
async def health_check(session: Annotated[AsyncSession, Depends(get_db)]):
    return await HealthService(session).execute()


if ENV == "development":

    @router.delete("/", include_in_schema=False)
    async def clear_tables(
        session: Annotated[AsyncSession, Depends(get_db)],
    ):
        return await GenericRepository(session).clear_tables()
