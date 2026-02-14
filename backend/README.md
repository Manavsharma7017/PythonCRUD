# Task Management API - Backend

A production-ready, scalable FastAPI backend with JWT authentication, role-based access control, and PostgreSQL database.

## Features

✅ **JWT Authentication** - Access tokens with refresh token support  
✅ **Password Security** - bcrypt hashing with salting  
✅ **Role-Based Access Control** - User and Admin roles with granular permissions  
✅ **RESTful API** - Clean API design with versioning (/api/v1)  
✅ **Database** - PostgreSQL with SQLAlchemy ORM  
✅ **Validation** - Pydantic schemas with comprehensive validation  
✅ **Error Handling** - Proper HTTP status codes and error messages  
✅ **API Documentation** - Interactive Swagger and ReDoc documentation  
✅ **Logging** - Structured logging for debugging and monitoring  
✅ **Docker Support** - Containerized deployment with docker-compose  
✅ **Testing** - Comprehensive unit tests with pytest  

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── security.py        # JWT and password utilities
│   │   └── dependencies.py    # Dependency injection
│   ├── db/
│   │   ├── base.py           # SQLAlchemy base
│   │   └── session.py        # Database session management
│   ├── models/
│   │   ├── user.py           # User database model
│   │   └── task.py           # Task database model
│   ├── schemas/
│   │   ├── user.py           # User Pydantic schemas
│   │   └── task.py           # Task Pydantic schemas
│   ├── crud/
│   │   ├── user.py           # User CRUD operations
│   │   └── task.py           # Task CRUD operations
│   └── api/
│       └── v1/
│           ├── auth.py       # Authentication endpoints
│           └── tasks.py      # Task endpoints
├── tests/
│   ├── test_auth.py          # Authentication tests
│   └── test_tasks.py         # Task tests
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── Dockerfile               # Docker image definition
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Local Development

1. **Clone the repository**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
Created `.env` file with:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskmanager_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Create database**
```bash
# Create PostgreSQL database
createdb taskmanager_db
```

6. **Run server**
```bash
uvicorn app.main:app --reload
```

Server will be available at `http://localhost:8000`

### Using Docker

1. **Build and run with docker-compose**
```bash
cd ..
docker-compose up --build
```

2. **Verify services**
- API: http://localhost:8000
- PostgreSQL: localhost:5432
- API Docs: http://localhost:8000/api/v1/docs

## API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Authentication Endpoints

**POST /api/v1/auth/register**
- Register new user
- Body: `{ "email": "user@example.com", "password": "secure123", "full_name": "John Doe" }`
- Response: User profile with ID

**POST /api/v1/auth/login**
- Login user
- Body: `{ "email": "user@example.com", "password": "secure123" }`
- Response: Access token, refresh token, user profile

**GET /api/v1/auth/me**
- Get current user info
- Headers: `Authorization: Bearer <access_token>`
- Response: User profile

### Task Endpoints

**POST /api/v1/tasks**
- Create task
- Headers: `Authorization: Bearer <access_token>`
- Body: `{ "title": "Task Title", "description": "Description" }`
- Response: Created task

**GET /api/v1/tasks**
- List user's tasks (admins see all)
- Headers: `Authorization: Bearer <access_token>`
- Query: `?skip=0&limit=100`
- Response: List of tasks with total count

**GET /api/v1/tasks/{task_id}**
- Get specific task
- Headers: `Authorization: Bearer <access_token>`
- Response: Task details

**PUT /api/v1/tasks/{task_id}**
- Update task (owner or admin)
- Headers: `Authorization: Bearer <access_token>`
- Body: `{ "title": "Updated Title", "description": "Updated Description" }`
- Response: Updated task

**DELETE /api/v1/tasks/{task_id}**
- Delete task (owner or admin)
- Headers: `Authorization: Bearer <access_token>`
- Response: 204 No Content

## Authentication

### JWT Flow

1. **Registration** → User creates account
2. **Login** → User receives access + refresh tokens
3. **Protected Routes** → Include `Authorization: Bearer <token>` header
4. **Token Expiry** → Access tokens expire in 30 minutes
5. **Refresh** → Use refresh token to get new access token

### Password Security

- Passwords hashed with bcrypt (12 rounds)
- Never stored in plain text
- Verified using constant-time comparison

## Role-Based Access Control

### User Role
- Create, read, update, delete own tasks
- Cannot access other users' tasks
- Cannot delete other tasks

### Admin Role
- Create, read, update own tasks
- View all users' tasks
- Delete any task
- Manage user accounts

## Error Handling

All errors return proper HTTP status codes:

| Status | Description |
|--------|-------------|
| 200 | OK - Successful request |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid credentials |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error |

## Validation

Uses Pydantic for request validation:
- Email validation
- Password minimum length (8 characters)
- Task title required (1-255 chars)
- Description max length (5000 chars)
- Query parameter validation with ranges

## Logging

Structured logging for:
- User authentication events
- CRUD operations
- Errors and exceptions
- Performance metrics

Configure log level in `.env`: `DEBUG=True` for verbose output

## Scalability & Best Practices

### Horizontal Scaling

**Database Connection Pooling**
```bash
# Use connection pool for multiple worker processes
# SQLAlchemy handles pooling automatically
```

**Multiple Worker Processes**
```bash
# Run with Gunicorn for production
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

**Load Balancing**
```bash
# Use Nginx or HAProxy to distribute requests
# Each worker handles independent requests
```

### Performance Optimization

**Database Indexing**
- Indexed on: user email, task owner_id
- Improves query performance for lookups

**Connection Pooling**
- Pre-configured in SQLAlchemy
- Reuses connections, reduces overhead

**Caching (Future Enhancement)**
- Redis can cache frequently accessed data
- Session-based caching for user tokens
- Query result caching for read-heavy operations

### Background Tasks (Future Enhancement)

```python
# Example with Celery
from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost")

@celery_app.task
def send_email_confirmation(user_id):
    # Send async email notification
    pass
```

### Microservices Architecture (Future Enhancement)

**Service Separation**
- Auth Service (JWT, registration, login)
- Task Service (CRUD operations)
- User Service (user management)
- Notification Service (emails, alerts)

**Benefits**
- Independent scaling
- Technology flexibility
- Fault isolation
- Easier testing and deployment

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
```

### Run with Coverage
```bash
pytest --cov=app tests/
```

### Test Categories

**Authentication Tests**
- User registration
- User login
- Token validation
- Duplicate email handling

**Task Tests**
- Task creation
- Task retrieval
- Task update
- Task deletion
- Permission checks

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role ENUM('user', 'admin') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# JWT
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
APP_NAME=Task Management API
APP_VERSION=1.0.0
DEBUG=False

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## Production Checklist

- [ ] Change `SECRET_KEY` to secure random string
- [ ] Set `DEBUG=False` in production
- [ ] Use environment-specific `.env` files
- [ ] Enable HTTPS/SSL
- [ ] Setup proper logging and monitoring
- [ ] Configure database backups
- [ ] Use connection pooling
- [ ] Implement rate limiting
- [ ] Add request logging
- [ ] Setup error tracking (Sentry)
- [ ] Use environment secrets management
- [ ] Enable CORS only for allowed origins
- [ ] Implement API rate limiting
- [ ] Setup health checks
- [ ] Configure auto-scaling

## Troubleshooting

**Database Connection Error**
```bash
# Verify PostgreSQL is running
psql -U postgres -h localhost

# Check DATABASE_URL in .env
# Format: postgresql://user:password@host:port/dbname
```

**Token Validation Error**
```bash
# Verify SECRET_KEY matches
# Check token expiry
# Include 'Bearer' prefix in Authorization header
```

**CORS Issues**
```bash
# Check CORS_ORIGINS in .env
# Frontend URL must be in allowed origins
# Check browser console for CORS errors
```

## Support & Contributing

For issues, feature requests, or contributions, please refer to the main project repository.

## License

MIT License - See LICENSE file for details
