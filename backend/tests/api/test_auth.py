"""
tests/api/test_auth.py
───────────────────────
Integration tests for the /auth endpoints.

Run with:
    cd backend
    pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.core.dependencies import get_db
from main import app

# ── In-memory SQLite for tests ─────────────────────────────────────────────────
SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(autouse=True, scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Tests ──────────────────────────────────────────────────────────────────────

class TestRegister:
    def test_register_new_doctor(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={"name": "Dr. Test", "email": "test@hospital.com", "password": "Test@12345"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@hospital.com"
        assert "hashed_password" not in data

    def test_duplicate_email_rejected(self, client):
        client.post(
            "/api/v1/auth/register",
            json={"name": "Dr. A", "email": "dup@hospital.com", "password": "Pass@12345"},
        )
        response = client.post(
            "/api/v1/auth/register",
            json={"name": "Dr. B", "email": "dup@hospital.com", "password": "Pass@12345"},
        )
        assert response.status_code == 409


class TestLogin:
    def setup_method(self):
        self.email = "login@hospital.com"
        self.password = "Login@12345"

    def test_login_returns_token(self, client):
        client.post(
            "/api/v1/auth/register",
            json={"name": "Dr. Login", "email": self.email, "password": self.password},
        )
        response = client.post(
            "/api/v1/auth/login",
            data={"username": self.email, "password": self.password},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_wrong_password_rejected(self, client):
        response = client.post(
            "/api/v1/auth/login",
            data={"username": self.email, "password": "WrongPass"},
        )
        assert response.status_code == 401


class TestMe:
    def test_get_me_with_valid_token(self, client):
        client.post(
            "/api/v1/auth/register",
            json={"name": "Dr. Me", "email": "me@hospital.com", "password": "Me@123456"},
        )
        login_resp = client.post(
            "/api/v1/auth/login",
            data={"username": "me@hospital.com", "password": "Me@123456"},
        )
        token = login_resp.json()["access_token"]
        me_resp = client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
        )
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == "me@hospital.com"

    def test_get_me_without_token_fails(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
