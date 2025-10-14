import pytest
import asyncio
from httpx import AsyncClient

from tests.conftest import clear_tables, create_session, BASE_URL

asyncio.run(clear_tables())

@pytest.mark.asyncio
async def test_check_self_information_with_loged_session():
    payload = {"username":"GenericUsername", "email": "generic@username.com", "password": "GenericPassword@123"}
    session = await create_session(payload)

    async with AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/users/me", headers={"token": session.access_token})
    assert response.status_code == 200

    response_body = response.json()
    user_response = response_body.get("user")
    session_response = response_body.get("session")
    
    assert user_response.get("username") == payload.get("username")
    assert user_response.get("email") == payload.get("email")
    assert session_response.get("token") == session.access_token
    assert session_response.get("expires_at") > str(session.expires_at)


@pytest.mark.asyncio
async def test_check_self_information_without_token():
    async with AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/users/me")
    
    assert response.status_code == 401
    response_body = response.json()
    assert "detail" in response_body
    details = response_body.get("detail")

    assert details.get("message") == "Invalid or expired authorization token"
    assert details.get("error") == "UnauthorizedError"
    assert details.get("action") == "Provide a valid authorization token"

@pytest.mark.asyncio
async def test_check_self_information_with_invalid_token():

    async with AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/users/me", headers={"token": "invalid-token-string"})
    
    assert response.status_code == 401
    response_body = response.json()
    assert "detail" in response_body
    details = response_body.get("detail")

    assert details.get("message") == "Invalid or expired authorization token"
    assert details.get("error") == "UnauthorizedError"
    assert details.get("action") == "Provide a valid authorization token"


asyncio.run(clear_tables())
