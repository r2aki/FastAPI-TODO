import pytest


@pytest.mark.parametrize(
    "username, password, email",
    [
        ("testuser", "Test1234", "test@example.com"),
        ("testuser67", "Test12345", "test@example.ru"),
        ("testuser2", "Teguiyhit1234", "test2@example.ru"),
    ],
)
def test_login_flow(client, username, password, email):
    reg_payload = {
        "username": username,
        "email": email,
        "password": password,
    }
    r = client.post("/users/", json=reg_payload)
    assert r.status_code in (200, 201)

    login_payload = {
        "username": username,
        "password": password,
    }
    r = client.post("/auth/login", json=login_payload)
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
