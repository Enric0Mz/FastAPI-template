from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from src.models.user import UserLoginModel
from src.service.session import LoginService
from src.models.token import TokenModel

from src.infra.database import get_db


router = APIRouter(
    prefix="/api/v1/sessions",
    tags=["Sessions"]
)

@router.post("/", response_model=TokenModel, status_code=201)
async def login(session: Annotated[AsyncSession, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await LoginService(session, form_data).execute()
