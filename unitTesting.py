import pytest
from app import app

@pytest.fixture()
def client():
    return app.test_client()

def test_login(client):
    email = "test@gmail.com"
    password = "test"

    response = client.post("/login", data={
        "email": email,
        "password": password
    })

    assert response.status_code == 200
    assert b"Be a better friend and stop forgetting they birthdays" in response.data

def test_wrong_login(client):
    email = "wrong@example.com"
    password = "wrongpassword"

    response = client.post("/login", data={
        "email": email,
        "password": password
    })
    assert b"Be a better friend and stop forgetting they birthdays" not in response.data

def test_register(client):
    email = "new@email.com"
    password = "password"

    response = client.post("/register", data={
        "email": email,
        "password": password
    })
    assert b">/login</a>" in response.data