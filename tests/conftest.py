import pytest
from app.config import settings
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import schemas

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_user}:{settings.database_pwd}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):

    user_data = {
        "email": "test@test.com",
        "username": "testUser",
        "password": "password123"
    }

    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]

    assert new_user["email"] == user_data["email"]
    assert res.status_code == 201
    return new_user


@pytest.fixture
def test_auth_user(test_user, client):

    res = client.post(
        "/login", data={
            "username": test_user["email"],
            "password": "password123"
        }
    )
    auth_data = res.json()
    payload = jwt.decode(
        auth_data["access_token"],
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm])

    id = payload.get("user_id")

    assert res.status_code == 200
    assert id == test_user["id"]
    assert auth_data["token_type"] == "bearer"
    return auth_data


@pytest.fixture
def test_item(client, test_user, test_auth_user):

    item_data = {
        "name": "Test item",
        "description": "Test description",
        "price": 7,
        "tax": 1
    }
    token = test_auth_user["access_token"]
    res = client.post(
        "/items/",
        json=item_data,
        headers={"Authorization": f"Bearer {token}"})

    new_item = schemas.ItemResponse(**res.json())

    assert new_item.name == item_data["name"]
    assert new_item.description == item_data["description"]
    assert new_item.price == item_data["price"]
    assert new_item.tax == item_data["tax"]

    return new_item
