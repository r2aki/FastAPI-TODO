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
