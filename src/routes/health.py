from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.service.health import HealthService
from src.models.health import HealthCheckResponseModel

from src.infra.database import get_db


router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health"]
)

@router.get("/", response_model=HealthCheckResponseModel)
async def health_check(session: Annotated[AsyncSession, Depends(get_db)]):
    return await HealthService(session).execute()
