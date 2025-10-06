import pytest
import asyncio
from httpx import AsyncClient

from tests.conftest import clear_tables


asyncio.run(clear_tables()) 

@pytest.mark.asyncio
async def test_create_user_with_correct_payload():
    payload = {
        "username": "User Name",
        "email": "user@name.com",
        "password": "secretPassword"
    }

    async with AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/v1/users/", json=payload)
    
    assert response.status_code == 201

    response_body = response.json()
    print("CORPODAREQUEST", response_body)

    assert response_body["username"] == payload["username"]
    assert response_body["email"] == payload["email"]

asyncio.run(clear_tables())
