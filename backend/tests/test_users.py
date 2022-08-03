import pytest
from faker import Faker

from fastapi.testclient import TestClient

from app.main import app
from app.database.client import connect_to_database


fake = Faker()

db = connect_to_database()

client = TestClient(app)


@pytest.mark.users
def test_create_a_new_user():
    user = fake.name().split()
    response = client.post(
        "/users/",
        json={
            "first_name": user[0],
            "last_name": user[1],
            "email": fake.email(),
            "password": fake.password()
        }
    )
    assert response.status_code == 201
