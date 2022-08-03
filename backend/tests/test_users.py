import pytest
from faker import Faker
from httpx import AsyncClient


from app.main import app


fake = Faker()


@pytest.fixture
async def async_app_client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.mark.users
async def test_create_a_new_user(async_app_client):
    user = fake.name().split()

    response = await async_app_client.post(
        "/users/",
        json={
            "first_name": user[0],
            "last_name": user[1],
            "email": fake.email(),
            "password": fake.password()
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert "_id" in data

    user_id = data["_id"]

    response = await async_app_client.get(f"/users/{user_id}")
    assert response.status_code == 200

    response = await async_app_client.delete(f"/users/{user_id}")
    assert response.status_code == 200
