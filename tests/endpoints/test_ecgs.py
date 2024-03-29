from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.factories.ecg import EcgFactory
from tests.factories.user import UserFactory


def test_get_ecgs(client: TestClient, authenticate_as_user):
    EcgFactory.create_batch(10, user=authenticate_as_user)
    EcgFactory.create_batch(10)

    response = client.get("/ecgs")

    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.usefixtures("authenticate_as_admin")
def test_admin_can_not_get_ecgs(client: TestClient):
    response = client.get("/ecgs")

    assert response.status_code == 403


def test_get_ecg(client: TestClient, authenticate_as_user):
    ecg = EcgFactory.create(user=authenticate_as_user)

    response = client.get(f"/ecgs/{ecg.id}")

    assert response.status_code == 200
    assert response.json()["id"] == ecg.id


@pytest.mark.usefixtures("authenticate_as_admin")
def test_admin_can_not_get_ecg(client: TestClient):
    ecg = EcgFactory.create()

    response = client.get(f"/ecgs/{ecg.id}")

    assert response.status_code == 403


@pytest.mark.usefixtures("authenticate_as_user")
def test_can_not_get_ecg_from_another_user(client: TestClient):
    user = UserFactory.create()
    ecg = EcgFactory.create(user=user)

    response = client.get(f"/ecgs/{ecg.id}")

    assert response.status_code == 403


def test_get_ecg_insights(client: TestClient, authenticate_as_user):
    ecg = EcgFactory.create(user=authenticate_as_user)

    response = client.get(f"/ecgs/{ecg.id}/insights")

    assert response.status_code == 200
    assert response.json()["id"] == ecg.insight.id


@pytest.mark.usefixtures("authenticate_as_admin")
def test_admin_can_not_get_ecg_insights(client: TestClient):
    ecg = EcgFactory.create()

    response = client.get(f"/ecgs/{ecg.id}/insights")

    assert response.status_code == 403


@pytest.mark.usefixtures("authenticate_as_user")
def test_can_not_get_ecg_insights_from_another_user(client: TestClient):
    user = UserFactory.create()
    ecg = EcgFactory.create(user=user)

    response = client.get(f"/ecgs/{ecg.id}/insights")

    assert response.status_code == 403


@pytest.mark.usefixtures("authenticate_as_user")
@patch("app.endpoints.ecg.on_ecg_create.delay")
def test_create_ecg(mock_on_ecg_create, client: TestClient):
    data = {
        "leads": [
            {
                "name": "I",
                "number_of_samples": 2,
                "signal": [1, 2],
            }
        ],
    }

    response = client.post("/ecgs", json=data)

    mock_on_ecg_create.assert_called_with(response.json()["id"])
    assert response.status_code == 200


@pytest.mark.usefixtures("authenticate_as_admin")
def test_admin_can_not_create_ecg(client: TestClient):
    data = {
        "leads": [
            {
                "name": "I",
                "number_of_samples": 2,
                "signal": [1, 2],
            }
        ],
    }

    response = client.post("/ecgs", json=data)

    assert response.status_code == 403
