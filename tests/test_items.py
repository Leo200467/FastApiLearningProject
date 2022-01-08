import random

import pytest
from app import schemas


@pytest.mark.parametrize("name, description, price, tax", [
    ("Banana", "Reponse Test", 11, 0),
    ("Apple", "Not the company", 6, 0.5),
    ("Grapes", "We love wine", 3, 0.2)
])
def test_create_item(name, description, price, tax, test_auth_user, client):

    token = test_auth_user["access_token"]

    res = client.post(
        "/items/",
        json={
            "name": name,
            "description": description,
            "price": price,
            "tax": tax},
        headers={"Authorization": f"Bearer {token}"})

    new_item = schemas.ItemResponse(**res.json())

    assert new_item.name == name
    assert new_item.description == description
    assert new_item.price == price
    assert new_item.tax == tax


def test_create_item_unauthorized(client):

    dummy_item = {
        'name': 'Test item',
        'description': 'Test description',
        'price': 7.0,
        'tax': 1.0,
        'id': 1
        }

    res = client.post("/items/", json=dummy_item)

    assert res.status_code == 401


def test_get_item(test_auth_user, client, test_item):

    token = test_auth_user["access_token"]

    res = client.get(
        f"/items/{test_item.id}",
        headers={"Authorization": f"Bearer {token}"})

    returned_item = res.json()

    assert res.status_code == 200
    assert returned_item["name"] == "Test item"
    assert returned_item["description"] == "Test description"
    assert returned_item["price"] == 7.0
    assert returned_item["tax"] == 1.0


def test_get_item_unauthorized(client):

    rand_item_id = random.randint(0, 100)

    res = client.get(f"/items/{rand_item_id}")

    assert res.status_code == 401


def test_get_item_outrange(test_auth_user, client):

    token = test_auth_user["access_token"]

    res = client.get(
        f"/items/{101}",
        headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 404


def test_delete_item(test_auth_user, client, test_item):

    token = test_auth_user["access_token"]

    res = client.delete(
        f"/items/{test_item.id}",
        headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 204


def test_delete_item_outrange(test_auth_user, client):

    token = test_auth_user["access_token"]

    res = client.delete(
        f"/items/{101}",
        headers={"Authorization": f"Bearer {token}"})

    assert res.status_code == 404


def test_update_item(test_auth_user, client, test_item):

    update_item_data = {
        'name': 'Updated item',
        'description': 'Updated description',
        'price': 8.0,
        'tax': 0.5
        }

    token = test_auth_user["access_token"]

    res = client.put(
        f"/items/{test_item.id}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_item_data)

    assert res.status_code == 204


def test_update_item_outrange(test_auth_user, client):

    update_item_data = {
        'name': 'Updated item',
        'description': 'Updated description',
        'price': 8.0,
        'tax': 0.5
        }

    token = test_auth_user["access_token"]

    res = client.put(
        f"/items/{101}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_item_data)

    assert res.status_code == 404
