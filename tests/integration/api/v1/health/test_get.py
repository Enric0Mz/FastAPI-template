from httpx import AsyncClient

from tests.conftest import BASE_URL

async def test_health_check_returns_200_with_correct_payload():
    async with AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/health/")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["api_status"] == "healthy"
    assert "details" in response_body

    response_body_details = response_body["details"]

    assert response_body_details["opened_conns"] == 1
    assert response_body_details["max_conns"] == 100
    assert response_body_details["server_version"] == "15.14"
