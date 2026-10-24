"""Validation des entrées HTTP de la carte."""
import pytest
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_update_marker_sans_decalage(client):
    response = client.post("/update_marker", data={"lat": "43.3", "lon": "5.4"})
    assert response.status_code == 200
    assert response.get_json() == {"lat": 43.3, "lon": 5.4}


@pytest.mark.parametrize("data", [
    {"lat": "91", "lon": "3"},
    {"lat": "abc", "lon": "3"},
    {"lat": "45"},
])
def test_update_marker_refuse_coordonnees_invalides(client, data):
    assert client.post("/update_marker", data=data).status_code == 400
