import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_login_success():
    response = client.post("/api/v1/auth/login", json={
        "username_or_email": "admin@soc.defense",
        "password": "Admin@123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" == "access_token" in data
    assert data["user"]["email"] == "admin@soc.defense"
    assert data["user"]["role"] == "admin"

def test_login_invalid_password():
    response = client.post("/api/v1/auth/login", json={
        "username_or_email": "admin@soc.defense",
        "password": "WrongPassword999!"
    })
    assert response.status_code == 401

def test_register_and_me():
    new_user = {
        "email": "test_analyst@soc.defense",
        "username": "testanalyst",
        "full_name": "Test Analyst",
        "password": "Password@123",
        "role": "analyst"
    }
    # Register
    reg_resp = client.post("/api/v1/auth/register", json=new_user)
    assert reg_resp.status_code == 201
    token = reg_resp.json()["access_token"]
    
    # Get Profile with token
    me_resp = client.get("/api/v1/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "test_analyst@soc.defense"
