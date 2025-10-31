from fastapi import APIRouter, Request, Depends
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.infra.database import get_db
from src.infra.security.google_oauth import oauth
from src.service.user import CreateOrGetGoogleUser
from src.models.user import GoogleUserModel
from src.models.user import AuthServiceEnum


router = APIRouter(tags=["Google"])


@router.get("/login", include_in_schema=False)
async def google_login(request: Request):
    redirect_url = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_url)


@router.get("/auth/callback", include_in_schema=False)
async def auth_callback(
    request: Request, session: Annotated[AsyncSession, Depends(get_db)]
):
    google_info = await oauth.google.authorize_access_token(request)
    user_info = google_info["userinfo"]

    google_payload = GoogleUserModel(
        email=user_info["email"],
        username=user_info.get("name", ""),
        google_id=user_info["sub"],
    )

    return await CreateOrGetGoogleUser(session, google_payload).execute()
