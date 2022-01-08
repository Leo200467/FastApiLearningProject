import pytest
from app import schemas
from app.config import settings
from jose import jwt


@pytest.mark.parametrize("email, password, status_code", [
    ("wrong@email.com", "wrongpassword", 403),
    ("wrong@email.com", "password123", 403),
    ("test@test.com", "wrongpassword", 403),
    ("test@test.com", None, 422),
    (None, "password123", 422)])
def test_incorrect_login(client, email, password, status_code, test_user):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code


def test_correct_login(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": "password123"})

    auth_data_schema = schemas.Token(**res.json())

    payload = jwt.decode(
        auth_data_schema.access_token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm])
    id = payload.get("user_id")

    assert res.status_code == 200
    assert id == test_user["id"]
    assert auth_data_schema.token_type == "bearer"
