import pytest
import asyncio
from httpx import AsyncClient

from tests.conftest import clear_tables

asyncio.run(clear_tables())


@pytest.mark.asyncio
async def test_create_user_with_correct_payload():
    payload = {
        "username": "UserName",
        "email": "user@name.com",
        "password": "SecurePassword123!",
    }

    async with AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/users/", json=payload
        )

    assert response.status_code == 201

    response_body = response.json()
    assert response_body["username"] == payload["username"]
    assert response_body["email"] == payload["email"]


@pytest.mark.asyncio
async def test_create_user_with_duplicate_email():

    payload = {
        "username": "DifferentName",
        "email": "user@name.com",  # Email used in the firts test
        "password": "SecurePassword123!",
    }

    async with AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/users/", json=payload
        )

    assert response.status_code == 409

    response_body = response.json()
    detail = response_body["detail"]
    assert detail["error"] == "ConflictError"
    assert (
        detail["message"]
        == f"A 'email' with the identifier '{payload['email']}' already exists"
    )


@pytest.mark.asyncio
async def test_create_user_with_duplicate_username():
    payload = {
        "username": "UserName",  # Username used in the first test
        "email": "different@email.com",
        "password": "SecurePassword123!",
    }

    async with AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/users/", json=payload
        )

    assert response.status_code == 409
    response_body = response.json()
    detail = response_body["detail"]

    assert detail["error"] == "ConflictError"
    assert (
        detail["message"]
        == f"A 'username' with the identifier '{payload['username']}' already exists"
    )


@pytest.mark.parametrize(
    "invalid_password, expected_msg_part",
    [
        ("short", "String should have at least 8 characters"),
        ("nouppercase1!", "Password must contain at least one uppercase letter"),
        ("NOLOWERCASE1!", "Password must contain at least one lowercase letter"),
        ("NoNumber!", "Password must contain at least one number"),
        ("NoSymbol1", "Password must contain at least one special symbol"),
    ],
)
@pytest.mark.asyncio
async def test_create_user_with_invalid_password(invalid_password, expected_msg_part):

    payload = {
        "username": "NewValidUser",
        "email": "newvalid@email.com",
        "password": invalid_password,
    }

    async with AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/users/", json=payload
        )

    assert response.status_code == 422

    response_body = response.json()

    assert "detail" in response_body
    error_details = response_body["detail"]
    assert isinstance(error_details, list)
    assert len(error_details) == 1

    error_message = error_details[0]["msg"]
    assert expected_msg_part in error_message

    assert error_details[0]["loc"] == ["body", "password"]


asyncio.run(clear_tables())
