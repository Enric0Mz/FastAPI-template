from fastapi.security import APIKeyHeader
from fastapi import Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database import get_db
from src.repositorys.sessions import SessionRepository
from src.repositorys.user import UserRepository
from src.models.session import SessionWithUserModel
from src.models.session import SessionModel
from src.models.user import UserModel
from src.helpers.errors import UnauthenticatedExpection


oauth2_scheme = APIKeyHeader(name="token", auto_error=False)

async def validate_session_middleware(session: Annotated[AsyncSession, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)] ):
    if not token:
        raise UnauthenticatedExpection()
    
    repository = SessionRepository(session)

    session_item = await repository.get_by_token(token)
    if not session_item:
        raise UnauthenticatedExpection()

    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(session_item.user_id)
    
    if not user:
        raise UnauthenticatedExpection()

    user_result = UserModel(username=user.username, email=user.email)

    EXPIRES_DELTA = 10 # minutes
    refreshed_session = await repository.refresh(session_item.user_id, EXPIRES_DELTA)

    refreshed_session_result = SessionModel(
        token=token,
        expires_at=refreshed_session.expires_at,
        user_id=refreshed_session.user_id
    )

    return SessionWithUserModel(
        session=refreshed_session_result,
        user=user_result
    )


