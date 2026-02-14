"""Unit tests for tasks"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

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
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def get_auth_token():
    """Helper function to get authentication token"""
    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "testpassword123"
        }
    )
    
    # Login and get token
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
    )
    return response.json()["access_token"]


def test_create_task():
    """Test task creation"""
    token = get_auth_token()
    
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"


def test_get_user_tasks():
    """Test retrieving user's tasks"""
    token = get_auth_token()
    
    # Create tasks
    client.post(
        "/api/v1/tasks",
        json={"title": "Task 1", "description": "First task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    client.post(
        "/api/v1/tasks",
        json={"title": "Task 2", "description": "Second task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get tasks
    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 2
    assert data["total"] == 2


def test_get_task_by_id():
    """Test retrieving specific task"""
    token = get_auth_token()
    
    # Create task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "Test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    # Get task
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"


def test_update_task():
    """Test task update"""
    token = get_auth_token()
    
    # Create task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original Title", "description": "Original"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    # Update task
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_delete_task():
    """Test task deletion"""
    token = get_auth_token()
    
    # Create task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Task to Delete", "description": "Will be deleted"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    # Delete task
    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    
    # Verify task is deleted
    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404
