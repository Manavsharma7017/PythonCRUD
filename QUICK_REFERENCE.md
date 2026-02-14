# QUICK REFERENCE GUIDE

A developer's quick reference for the Task Management System.

## 🚀 Start Project (5 Minutes)

### With Docker (Easiest)
```bash
docker-compose up --build
# API:      http://localhost:8000
# Frontend: http://localhost:3000
# Docs:     http://localhost:8000/api/v1/docs
```

### Local Development
```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm start
```

---

## 📁 File Locations Cheat Sheet

### Backend Core
| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app entry point |
| `backend/app/core/config.py` | Settings & env vars |
| `backend/app/core/security.py` | JWT & password functions |
| `backend/app/core/dependencies.py` | Auth dependencies |

### Backend Database
| File | Purpose |
|------|---------|
| `backend/app/models/user.py` | User model |
| `backend/app/models/task.py` | Task model |
| `backend/app/db/session.py` | DB connection |

### Backend CRUD & API
| File | Purpose |
|------|---------|
| `backend/app/crud/user.py` | User operations |
| `backend/app/crud/task.py` | Task operations |
| `backend/app/schemas/user.py` | User validation |
| `backend/app/schemas/task.py` | Task validation |
| `backend/app/api/v1/auth.py` | Auth endpoints |
| `backend/app/api/v1/tasks.py` | Task endpoints |

### Frontend
| File | Purpose |
|------|---------|
| `frontend/src/App.js` | Main app component |
| `frontend/src/api/api.js` | API client |
| `frontend/src/pages/Login.js` | Login page |
| `frontend/src/pages/Register.js` | Register page |
| `frontend/src/pages/Dashboard.js` | Main page |

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/v1/auth/register     → Create account
POST   /api/v1/auth/login        → Get tokens
GET    /api/v1/auth/me           → Get current user
```

### Tasks
```
POST   /api/v1/tasks             → Create task
GET    /api/v1/tasks             → List tasks
GET    /api/v1/tasks/{id}        → Get task
PUT    /api/v1/tasks/{id}        → Update task
DELETE /api/v1/tasks/{id}        → Delete task
```

### Health
```
GET    /health                   → Server status
GET    /                         → API info
```

---

## 🔑 Authentication Flow

```
1. User registers at /register
   ↓
2. Email + Password sent to POST /auth/register
   ↓
3. User logs in at /login
   ↓
4. Email + Password sent to POST /auth/login
   ↓
5. Receive access_token + refresh_token
   ↓
6. Store tokens in localStorage
   ↓
7. Send: Authorization: Bearer <access_token> with requests
   ↓
8. If 401: Auto logout and redirect to /login
```

---

## 📝 Common Code Patterns

### Backend - Create Endpoint
```python
from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.core.dependencies import get_current_active_user

router = APIRouter(prefix="/api/v1/items", tags=["Items"])

@router.post("")
def create_item(
    item: ItemCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud_item.create(db, item, current_user.id)
```

### Backend - Protected Endpoint
```python
@router.get("")
def get_user_resources(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return crud_resource.get_all(db)
```

### Frontend - API Call
```javascript
import { tasksAPI } from '../api/api';

// Create
const response = await tasksAPI.createTask(title, description);

// List
const { data } = await tasksAPI.getTasks(0, 100);

// Update
await tasksAPI.updateTask(id, newTitle, newDesc);

// Delete
await tasksAPI.deleteTask(id);
```

### Frontend - Protected Route
```javascript
<Routes>
  <Route path="/login" element={<Login />} />
  <Route 
    path="/dashboard" 
    element={
      <ProtectedRoute>
        <Dashboard />
      </ProtectedRoute>
    } 
  />
</Routes>
```

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest                          # Run all
pytest tests/test_auth.py       # Specific file
pytest -v                       # Verbose
pytest --cov=app tests/         # With coverage
```

### Run Frontend Tests
```bash
cd frontend
npm test                        # Run all
npm test -- test_name           # Specific test
npm test -- --coverage          # With coverage
```

---

## 🔒 Key Security Functions

### Password Hashing
```python
from app.core.security import get_password_hash, verify_password

# Hash password
hashed = get_password_hash("user_password")

# Verify password
is_correct = verify_password("user_input", hashed_password)
```

### JWT Token Creation
```python
from app.core.security import create_access_token
from datetime import timedelta

token = create_access_token(
    data={"sub": user.id, "email": user.email},
    expires_delta=timedelta(minutes=30)
)
```

### Token Verification
```python
from app.core.dependencies import get_current_user

# Use as dependency in endpoints
async def protected_endpoint(
    current_user = Depends(get_current_user)
):
    return current_user
```

---

## 🐛 Common Issues & Solutions

### Backend Won't Start
```bash
# Check Python version
python --version  # Need 3.11+

# Check dependencies
pip install -r requirements.txt

# Check database
psql -U postgres  # Connection test

# Run with debug
DEBUG=True uvicorn app.main:app --reload
```

### Frontend Can't Connect to Backend
```javascript
// Check .env
REACT_APP_API_URL=http://localhost:8000

// Check CORS in backend
CORS_ORIGINS=["http://localhost:3000"]

// Check browser console for errors
```

### Port Already in Use
```bash
# Find process
lsof -i :8000           # macOS/Linux
netstat -ano | grep 8000  # Windows

# Kill process or use different port
uvicorn app.main:app --port 8001
```

---

## 📊 Database Queries

### User Operations
```python
from app.crud.user import crud_user

# Create
user = crud_user.create(db, user_create)

# Get by ID
user = crud_user.get_by_id(db, user_id)

# Get by email
user = crud_user.get_by_email(db, email)

# Authenticate
user = crud_user.authenticate(db, email, password)

# Update
user = crud_user.update(db, user, user_update)

# Delete
crud_user.delete(db, user_id)
```

### Task Operations
```python
from app.crud.task import crud_task

# Create
task = crud_task.create(db, task_create, owner_id)

# Get user tasks
tasks = crud_task.get_user_tasks(db, owner_id)

# Get all tasks (admin)
tasks = crud_task.get_all(db)

# Update
task = crud_task.update(db, task, task_update)

# Delete
crud_task.delete(db, task_id)
```

---

## 📋 Configuration Reference

### Backend .env
```env
# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# JWT
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
DEBUG=False
APP_NAME=Task Management API
CORS_ORIGINS=["http://localhost:3000"]

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### Frontend .env
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🛠️ Development Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run production (Gunicorn)
gunicorn app.main:app --workers 4

# Run tests
pytest

# Generate requirements
pip freeze > requirements.txt
```

### Frontend
```bash
# Install dependencies
npm install

# Development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Update dependencies
npm update
```

### Docker
```bash
# Build images
docker-compose build

# Start services
docker-compose up

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild everything
docker-compose up --build
```

---

## 📱 Response Format Examples

### Success Response (200 OK)
```json
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

### Error Response (400 Bad Request)
```json
{
  "detail": "Email already registered"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## 🎯 Role-Based Permissions

| Action | User | Admin |
|--------|------|-------|
| Create own task | ✅ | ✅ |
| View own tasks | ✅ | ✅ |
| Update own task | ✅ | ✅ |
| Delete own task | ✅ | ✅ |
| View all tasks | ❌ | ✅ |
| Update any task | ❌ | ✅ |
| Delete any task | ❌ | ✅ |

---

## 📊 Database Schema

### Users
```
id: Integer (PK)
email: String (Unique)
hashed_password: String
full_name: String
role: Enum('user', 'admin')
is_active: Boolean
created_at: DateTime
updated_at: DateTime
```

### Tasks
```
id: Integer (PK)
title: String
description: Text
owner_id: Integer (FK → users.id)
created_at: DateTime
updated_at: DateTime
```

---

## 🔍 Debugging Tips

### Backend Debug
```python
# Add print statements
print(f"User: {user}")

# Use logger
import logging
logger = logging.getLogger(__name__)
logger.info(f"Task created: {task.id}")

# Check database directly
python -c "from app.db.session import SessionLocal; \
  db = SessionLocal(); \
  users = db.query(User).all(); \
  print(users)"
```

### Frontend Debug
```javascript
// Console logging
console.log('User:', user);
console.error('Error:', error);

// Network inspection
// Open DevTools → Network tab
// See requests and responses

// State logging
const [state, setState] = useState(null);
useEffect(() => console.log('State:', state), [state]);
```

### Network Requests
```bash
# Test API with curl
curl -X GET http://localhost:8000/health

# With token
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/v1/auth/me
```

---

## 📚 Documentation Quick Links

- **API Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **Backend README**: `backend/README.md`
- **Frontend README**: `frontend/README.md`
- **Setup Guide**: `SETUP_GUIDE.md`
- **This Guide**: `QUICK_REFERENCE.md`

---

## ⚡ Performance Tips

### Backend
- Use async functions for I/O
- Index frequently queried columns
- Enable query logging to find bottlenecks
- Use connection pooling

### Frontend
- Lazy load components
- Memoize expensive calculations
- Minimize API calls
- Use production builds

### Database
- Index foreign keys
- Normalize schema
- Use prepared statements
- Monitor query performance

---

## 🚀 Deployment Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Update CORS_ORIGINS
- [ ] Setup HTTPS/SSL
- [ ] Configure database backups
- [ ] Setup monitoring/logging
- [ ] Enable rate limiting
- [ ] Run security audit
- [ ] Test all endpoints
- [ ] Verify error handling

---

## 💾 Backup & Recovery

### Backup Database
```bash
pg_dump taskmanager_db > backup.sql
```

### Restore Database
```bash
psql taskmanager_db < backup.sql
```

### Backup Application Files
```bash
tar -czf app_backup.tar.gz app/
```

---

## 🔗 Useful Links

- [FastAPI Docs](https://fastapi.tiangolo.com/docs/)
- [React Docs](https://react.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [JWT.io](https://jwt.io/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Axios Docs](https://axios-http.com/docs)

---

**Last Updated**: February 14, 2026
**Version**: 1.0.0
