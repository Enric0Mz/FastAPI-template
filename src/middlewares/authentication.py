from fastapi.security import APIKeyHeader
from fastapi.exceptions import HTTPException
from fastapi import Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database import get_db
from src.repositorys.sessions import SessionRepository
from src.repositorys.user import UserRepository
from src.models.user import UserModel


oauth2_scheme = APIKeyHeader(name="token")

async def validate_session_middleware(session: Annotated[AsyncSession, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)] ):
    if not token:
        raise HTTPException(401, "Provide a valid authentication token")
    
    repository = SessionRepository(session)

    session_item = await repository.get_by_token(token)
    if not session_item:
        raise HTTPException(401, "Invalid or expired session")

    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(session_item.user_id)
    
    if not user:
        raise HTTPException(401, "Provide a valid authentication token") 

    EXPIRES_DELTA = 10 # minutes
    await repository.refresh(session_item.user_id, EXPIRES_DELTA)

    return UserModel(
        username=user.username,
        email=user.email
    )


