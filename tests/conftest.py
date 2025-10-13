from httpx import AsyncClient
from src.models.user import CreateUserModel

BASE_URL = "http://localhost:8000"


async def clear_tables():
    async with AsyncClient() as client:
        return await client.delete(f"{BASE_URL}/api/v1/health/")


async def create_mock_user():
    payload = {
        "username": "MockUser",
        "email": "mock@user.com",
        "password": "MockPassword123!"
    }

    async with AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/users/", json=payload)

    if response.status_code != 201:
        raise ConnectionRefusedError("An error ocurred when creating mock user")
    
    return CreateUserModel(**payload)
