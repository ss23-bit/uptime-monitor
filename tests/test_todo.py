from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_todos_invalid_token():
    login_response = client.post(
        "/login",
        json={
            "username": "usertest1",
            "password": "passwordtest2"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/todos",
        headers={
            "Authorization": f"Bearer invalidtoken" 
        }
    )

    assert response.status_code == 401



