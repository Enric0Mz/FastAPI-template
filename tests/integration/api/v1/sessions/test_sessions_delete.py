import pytest
from httpx import AsyncClient

from tests.conftest import create_session, BASE_URL



@pytest.mark.asyncio
async def test_delete_session_with_logged_user():
    session = await create_session()

    async with AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/api/v1/sessions/",  headers={"token": session.access_token})  # Added trailing slash
        test_if_logged_out_response = await client.get(f"{BASE_URL}/api/v1/users/me", headers={"token": session.access_token})

    assert response.status_code == 204
    assert test_if_logged_out_response.status_code == 401


    response_body = test_if_logged_out_response.json()

    assert response_body["detail"] == {
        "message":"Invalid or expired authorization token",
        "error" : "UnauthorizedError",
        "action" : "Provide a valid authorization token"
    }
