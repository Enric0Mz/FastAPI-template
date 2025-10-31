from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from src.service.session import LoginService
from src.service.session import LogoutService
from src.models.token import TokenModel
from src.models.session import SessionWithUserModel
from src.middlewares.authentication import validate_session_middleware

from src.infra.database import get_db


router = APIRouter(prefix="/api/v1/sessions", tags=["Sessions"])


@router.post("/", response_model=TokenModel, status_code=201)
async def login(
    session: Annotated[AsyncSession, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await LoginService(session, form_data).execute()

@router.delete("/", status_code=204)
async def logout(session: Annotated[AsyncSession, Depends(get_db)], user: Annotated[SessionWithUserModel, Depends(validate_session_middleware)]):
    return await LogoutService(session, user.session.user_id).execute()
