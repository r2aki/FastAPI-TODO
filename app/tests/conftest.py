import asyncio

import pytest
from starlette.testclient import TestClient

from app.main import app
from app.db import get_db
from app.tests.db_test import init_test_db, override_get_db


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    asyncio.run(init_test_db())
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def register_and_login(client):
    def _register_and_login(username: str, password: str, email: str) -> str:
        # 1. регистрация
        reg_payload = {
            "username": username,
            "email": email,
            "password": password,
        }
        r = client.post("/users/", json=reg_payload)
        assert r.status_code in (200, 201)

        # 2. логин
        login_payload = {
            "username": username,
            "password": password,
        }
        r = client.post("/auth/login", json=login_payload)
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        return data["access_token"]

    return _register_and_login
