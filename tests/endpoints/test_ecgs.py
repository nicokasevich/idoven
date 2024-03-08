import pytest
from fastapi.testclient import TestClient

from tests.factories.ecg import EcgFactory
from tests.factories.insight import InsightFactory


@pytest.mark.usefixtures("authenticate_user")
def test_get_ecgs(client: TestClient):
    EcgFactory.create_batch(10)

    response = client.get("/ecgs")

    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.usefixtures("authenticate_user")
def test_get_ecg(client: TestClient):
    ecg = EcgFactory.create()

    response = client.get(f"/ecgs/{ecg.id}")

    assert response.status_code == 200
    assert response.json()["id"] == ecg.id


@pytest.mark.usefixtures("authenticate_user")
def test_get_ecg_insights(client: TestClient):
    ecg = EcgFactory.create(insights=[])
    InsightFactory.create_batch(5, ecg=ecg)

    response = client.get(f"/ecgs/{ecg.id}/insights")

    assert response.status_code == 200
    assert len(response.json()) == 5


@pytest.mark.usefixtures("authenticate_user")
def test_create_ecg(client: TestClient):
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

    assert response.status_code == 200
