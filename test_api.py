"""Integration tests for the API endpoints using FastAPI's TestClient."""

from fastapi.testclient import TestClient

from supportgenie.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_signup_and_login_flow():
    # Use a unique username so the test is repeatable.
    import uuid
    username = f"testuser_{uuid.uuid4().hex[:8]}"

    # Sign up.
    signup = client.post("/auth/signup", json={"username": username, "password": "testpass123"})
    assert signup.status_code == 200

    # Log in with the same credentials.
    login = client.post("/auth/login", json={"username": username, "password": "testpass123"})
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_login_with_wrong_password_fails():
    import uuid
    username = f"testuser_{uuid.uuid4().hex[:8]}"

    client.post("/auth/signup", json={"username": username, "password": "correctpass"})
    login = client.post("/auth/login", json={"username": username, "password": "wrongpass"})
    assert login.status_code == 401


def test_chat_without_token_is_rejected():
    response = client.post("/chat", json={"question": "hello"})
    assert response.status_code in (401, 403)