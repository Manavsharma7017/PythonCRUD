# Task Management System - Full Stack Application

A production-ready full-stack application with FastAPI backend and React frontend for managing tasks with JWT authentication and role-based access control.

## 📋 Project Overview

This is a complete task management system featuring:

**Backend (FastAPI)**
- JWT authentication with access & refresh tokens
- Bcrypt password hashing
- Role-based access control (User, Admin)
- PostgreSQL database with SQLAlchemy
- RESTful API with versioning (/api/v1)
- Comprehensive error handling
- Pydantic validation
- Swagger & ReDoc documentation
- Docker containerization
- Pytest unit tests
- Production-ready architecture

**Frontend (React)**
- Modern responsive UI
- User registration and login
- Task CRUD operations
- JWT token management
- Protected routes
- Error handling and user feedback
- Clean component architecture

## 🏗️ Project Structure

```
.
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── core/              # Configuration, security, dependencies
│   │   ├── db/                # Database configuration
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── crud/              # Database operations
│   │   └── api/               # API endpoints (v1)
│   ├── tests/                 # Unit tests
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── Dockerfile            # Docker build
│   └── README.md             # Backend documentation
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── api/              # API client
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable components
│   │   ├── styles/           # CSS stylesheets
│   │   ├── App.js            # Main app
│   │   └── index.js          # Entry point
│   ├── public/               # Static files
│   ├── package.json          # NPM dependencies
│   ├── .env                  # Environment variables
│   └── README.md             # Frontend documentation
│
├── docker-compose.yml         # Docker Compose orchestration
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 14+
- PostgreSQL 12+
- Docker & Docker Compose (optional but recommended)

### Option 1: Using Docker Compose (Recommended)

**Easiest and fastest way to run everything:**

```bash
# From project root directory
docker-compose up --build

# Services will be available at:
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:3000
# - API Docs: http://localhost:8000/api/v1/docs
# - PostgreSQL: localhost:5432
```

### Option 2: Local Development Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
# Create PostgreSQL database:
createdb taskmanager_db

# Update .env with your database credentials

# Run migrations and start server
uvicorn app.main:app --reload

# Backend will be available at http://localhost:8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Frontend will open at http://localhost:3000
```

## 📡 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Interactive Documentation

Access interactive API documentation:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Authentication Endpoints

#### Register
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}

Response: 201 Created
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-02-14T10:00:00",
  "updated_at": "2024-02-14T10:00:00"
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": { ... }
}
```

#### Get Current User
```
GET /auth/me
Authorization: Bearer <access_token>

Response: 200 OK
{ user object }
```

### Task Endpoints

#### Create Task
```
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "My Task",
  "description": "Task description"
}

Response: 201 Created
```

#### List Tasks
```
GET /tasks?skip=0&limit=100
Authorization: Bearer <access_token>

Response: 200 OK
{
  "tasks": [ ... ],
  "total": 5
}
```

#### Get Task
```
GET /tasks/{task_id}
Authorization: Bearer <access_token>

Response: 200 OK
{ task object }
```

#### Update Task
```
PUT /tasks/{task_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description"
}

Response: 200 OK
```

#### Delete Task
```
DELETE /tasks/{task_id}
Authorization: Bearer <access_token>

Response: 204 No Content
```

## 🔐 Authentication & Security

### JWT Flow

1. **Register** → User creates account with email and password
2. **Login** → User receives access + refresh tokens
3. **Request** → Include `Authorization: Bearer <token>` header
4. **Automatic Logout** → App logs out on 401 (token expired)

### Security Features

- **Password Hashing**: Bcrypt with 12 salt rounds
- **JWT Tokens**: HS256 algorithm with configurable expiry
- **CORS**: Configured for specific origins
- **Input Validation**: Pydantic schemas
- **SQL Injection Protection**: SQLAlchemy ORM
- **HTTP Only**: Optional secure cookie support

### Environment Variables

**Backend (.env)**
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-long-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=False
CORS_ORIGINS=["http://localhost:3000"]
```

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:8000
```

## 👥 Role-Based Access Control

### User Role
- ✅ Create own tasks
- ✅ View own tasks
- ✅ Update own tasks
- ✅ Delete own tasks
- ❌ Cannot access other user's tasks

### Admin Role
- ✅ Create own tasks
- ✅ View all tasks
- ✅ Update any task
- ✅ Delete any task
- ✅ Manage users

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Test Coverage

- User registration
- User login
- Token validation
- Task CRUD operations
- Permission checks
- Error handling

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 📊 Database Schema

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
    description TEXT,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

### Environment-Specific Configuration

**Development**
```
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskmanager_db
```

**Production**
```
DEBUG=False
DATABASE_URL=postgresql://user:secure_password@prod_host:5432/dbname
SECRET_KEY=generate-new-secure-key
```

### Database Connection Pool

SQLAlchemy automatically manages connection pooling:
- Pool size: 5 connected connections
- Max overflow: 10 additional connections
- Pool recycle: 3600 seconds

## 📈 Scalability & Best Practices

### Horizontal Scaling

1. **Multiple Workers**: Use Gunicorn with multiple workers
   ```bash
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

2. **Load Balancer**: Use Nginx/HAProxy to distribute requests

3. **Database Pooling**: SQLAlchemy connection pooling

### Performance Optimization

- **Database Indexes**: Indexed on email, task owner_id
- **Query Optimization**: Efficient SQLAlchemy queries
- **Caching**: Can add Redis for session/query caching
- **Compression**: Gzip enabled for responsive payloads

### Future Enhancements

**Caching Layer**
```python
# Redis for caching frequently accessed data
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

**Background Tasks**
```python
# Celery for async operations
from celery import Celery
celery_app = Celery('tasks', broker='redis://localhost')
```

**Microservices Architecture**
- Auth Service
- Task Service
- User Service
- Notification Service

## 🐳 Docker Deployment

### Docker Images

**Backend**
```dockerfile
# Builds on python:3.11-slim
# Installs dependencies
# Exposes port 8000
# Runs uvicorn server
```

**PostgreSQL**
```dockerfile
# Uses postgres:15-alpine
# Auto-initializes database
# Persists data in volume
```

### Docker Compose Services

1. **postgres** - PostgreSQL 15 database
2. **backend** - FastAPI application
3. **frontend** (optional) - React app

### Production Deployment

**Kubernetes Ready**
- Dockerfile optimized for K8s
- Health check endpoints
- Liveness/readiness probes

**Cloud Deployment Options**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Heroku
- DigitalOcean App Platform

## 🚨 Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful request |
| 201 | Created | Task created |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Validation Error | Invalid data format |
| 500 | Server Error | Internal error |

### Error Response Format

```json
{
  "detail": "Error message",
  "errors": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email",
      "type": "value_error"
    }
  ]
}
```

## 📝 Logging

Structured logging for debugging and monitoring:

```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"User created: {user.email}")
logger.error(f"Database error: {error}")
```

Log levels:
- **DEBUG**: Detailed information
- **INFO**: General information
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

Configure in `app/core/config.py`

## 🔍 Monitoring & Debugging

### Health Check Endpoint

```
GET /health

Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "app_name": "Task Management API"
}
```

### API Documentation

You can explore all endpoints at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Debug Mode

Enable debug logging:
```bash
DEBUG=True
```

## 🆘 Troubleshooting

### Database Connection Error
```bash
# Verify PostgreSQL is running
psql -U postgres -h localhost

# Check DATABASE_URL format
# postgresql://user:password@host:port/dbname
```

### Port Already in Use
```bash
# Change port in environment or find process using port
# Linux/Mac:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000
```

### CORS Error
```
# Verify CORS_ORIGINS in backend .env
# Frontend URL must be in allowed origins
```

### Token Validation Error
```
# Check SECRET_KEY matches between backend instances
# Verify token includes "Bearer" prefix in header
```

## 📚 Documentation Links

- [Backend README](./backend/README.md) - Detailed backend documentation
- [Frontend README](./frontend/README.md) - Detailed frontend documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [JWT Documentation](https://jwt.io/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Created as a production-ready example for building scalable full-stack applications.

## 🙏 Support

For issues and questions:
1. Check existing documentation
2. Review error messages and logs
3. Check troubleshooting section
4. Open an issue with detailed information

---

## Quick Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] PostgreSQL database created
- [ ] Environment variables configured
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Can create/read/update/delete tasks
- [ ] API documentation accessible at /api/v1/docs
- [ ] All tests passing
- [ ] Docker images building successfully

## Next Steps

1. **Customize**: Modify colors, branding, and features
2. **Deploy**: Push to production using Docker
3. **Monitor**: Setup logging and error tracking
4. **Scale**: Add caching and background tasks
5. **Extend**: Add more models and endpoints

Happy coding! 🚀
