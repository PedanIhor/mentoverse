from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_all_users():
    response = client.get("/user")
    assert response.status_code == 200


def test_auth_error():
    response = client.post("/token", data={"username": "", "password": ""})
    access_token = response.json().get("access_token")
    assert access_token is None
    message = response.json().get("detail")[0].get("msg")
    assert message == "Field required"


def test_auth_success():
    pass