from httpx import AsyncClient

BASE_URL = "http://localhost:8000"


async def clear_tables():
    async with AsyncClient() as client:
        return await client.delete(f"{BASE_URL}/api/v1/health/")
