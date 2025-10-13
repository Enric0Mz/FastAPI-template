import pytest
import asyncio
from httpx import AsyncClient
from datetime import datetime
from datetime import timezone

from tests.conftest import clear_tables, create_mock_user, BASE_URL

asyncio.run(clear_tables())


@pytest.mark.asyncio
async def test_create_session_with_correct_user_and_password():
    user = await create_mock_user()
    payload = {
        "username": user.email,
        "password": user.password
    }

    async with AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/sessions/", data=payload)

    assert response.status_code == 201

    response_body = response.json()
    print(f"{response_body['expires_at']} MAIOR QUE {str(datetime.now(timezone.utc))}")

    assert "access_token" in response_body
    assert response_body["token_type"] == "Bearer"
    assert response_body["expires_at"] > str(datetime.now(timezone.utc))



asyncio.run(clear_tables())