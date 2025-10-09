from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.models.user import UserModel
from src.models.user import CreateUserModel
from src.service.user import CreateUserService

from src.infra.database import get_db


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.post("/", response_model=UserModel, status_code=201)
async def create_user(session: Annotated[AsyncSession, Depends(get_db)], body: CreateUserModel):
    return await CreateUserService(session, body).execute()
