import pytest
from fastapi.testclient import TestClient

from tests.factories.user import UserFactory


@pytest.mark.usefixtures("authenticate_as_admin")
def test_user_can_register(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "name",
            "email": "email@test.com",
            "full_name": "lastname",
            "password": "password",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "username": "name",
        "email": "email@test.com",
        "full_name": "lastname",
    }


@pytest.mark.usefixtures("authenticate_as_user")
def test_user_can_not_register(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "name",
            "email": "email@example.com",
            "full_name": "lastname",
            "password": "password",
        },
    )

    assert response.status_code == 403


@pytest.mark.usefixtures("authenticate_as_admin")
def test_user_can_not_register_with_existing_email(client: TestClient):
    user = UserFactory()

    response = client.post(
        "/auth/register",
        json={
            "email": user.email,
            "password": "password",
            "username": "name",
            "full_name": "full name",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists"}


@pytest.mark.usefixtures("authenticate_as_admin")
def test_user_can_not_register_with_existing_username(client: TestClient):
    user = UserFactory(email="email2@test.com")

    response = client.post(
        "/auth/register",
        json={
            "email": "email1@test.com",
            "password": "password",
            "username": user.username,
            "full_name": "full name",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}


def test_user_can_login(client: TestClient):
    user = UserFactory()

    response = client.post(
        "/auth/token",
        data={"username": str(user.username), "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200


def test_user_cant_login_with_username(client: TestClient):
    UserFactory(username="john_doe")

    response = client.post(
        "/auth/token",
        data={"username": "wrong_username", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_user_cant_login_with_wrong_password(client: TestClient):
    UserFactory(username="john_doe")

    response = client.post(
        "/auth/token",
        data={"username": "john_doe", "password": "wrong_password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
