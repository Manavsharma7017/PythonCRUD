"""Unit tests for authentication"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin
from app.crud.user import crud_user

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup():
    """Setup and teardown for each test"""
    # Clear database before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_register_duplicate_email():
    """Test registration with duplicate email"""
    # Register first user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "testpassword123"
        }
    )
    
    # Try to register with same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "full_name": "Another User",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.text


def test_login_user():
    """Test user login"""
    # Register user first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "testpassword123"
        }
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "testuser@example.com"


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_get_current_user():
    """Test getting current user information"""
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "testpassword123"
        }
    )
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
    )
    
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
