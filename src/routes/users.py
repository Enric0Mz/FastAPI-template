from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.models.session import SessionWithUserModel
from src.models.user import UserModel
from src.models.user import CreateUserModel
from src.service.user import CreateUserService

from src.infra.database import get_db
from src.middlewares.authentication import validate_session_middleware


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.get("/me", response_model=SessionWithUserModel, status_code=200)
async def get_self_user(user: Annotated[SessionWithUserModel, Depends(validate_session_middleware)]):
    return user

@router.post("/", response_model=UserModel, status_code=201)
async def create_user(session: Annotated[AsyncSession, Depends(get_db)], body: CreateUserModel):
    return await CreateUserService(session, body).execute()
