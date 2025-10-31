import pytest
from httpx import AsyncClient
from typing import Optional, AsyncGenerator

from src.models.user import CreateUserModel
from src.models.token import TokenModel

BASE_URL = "http://localhost:8000"


@pytest.fixture(autouse=True, scope="module")
async def clear_tables() -> AsyncGenerator[None, None]:
    async with AsyncClient() as client:
        await client.delete(f"{BASE_URL}/api/v1/health/")
        yield None
        await client.delete(f"{BASE_URL}/api/v1/health/")


async def create_mock_user(optional_payload: Optional[dict] = None) -> CreateUserModel:
    payload = optional_payload or {
        "username": "MockUser",
        "email": "mock@user.com",
        "password": "MockPassword123!"
    }

    async with AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/users/", json=payload)
    body = response.json()
    if response.status_code != 201:
        raise ConnectionRefusedError("An error ocurred when creating mock user")
    return CreateUserModel(**payload)


async def create_session(optional_user: Optional[dict] = None) -> TokenModel:
    if optional_user:
        user = await create_mock_user(optional_user)
    else:
        user = await create_mock_user()

    async with AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/sessions/",
            data={"username": user.email, "password": user.password},
        )
        if response.status_code != 201:
            raise ConnectionRefusedError("An error ocurred when creating session")
        return TokenModel(**response.json())
