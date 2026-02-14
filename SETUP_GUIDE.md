# SETUP & DEPLOYMENT GUIDE

Complete guide for setting up and deploying the Task Management System.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start with Docker](#quick-start-with-docker)
3. [Local Development Setup](#local-development-setup)
4. [Database Setup](#database-setup)
5. [Running Backend](#running-backend)
6. [Running Frontend](#running-frontend)
7. [Testing](#testing)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.11+** - Download from https://www.python.org/
- **Node.js 14+** - Download from https://nodejs.org/
- **PostgreSQL 12+** - Download from https://www.postgresql.org/
- **Git** - Download from https://git-scm.com/
- **Docker & Docker Compose** (optional, for containerized setup)

### System Requirements

- **RAM**: Minimum 2GB, recommended 4GB+
- **Disk Space**: 2GB for dependencies
- **Ports**: 8000 (backend), 3000 (frontend), 5432 (PostgreSQL)

### Verify Installation

```bash
# Check Python
python --version
# Expected: Python 3.11+

# Check Node.js
node --version
npm --version
# Expected: Node 14+ and npm 6+

# Check PostgreSQL
psql --version
# Expected: PostgreSQL 12+

# Check Git
git --version
# Expected: git 2+
```

---

## Quick Start with Docker

**Best option if you have Docker installed!**

### Step 1: Install Docker

[Download Docker Desktop](https://www.docker.com/products/docker-desktop)

### Step 2: Navigate to Project

```bash
cd path/to/intership  # Project root directory
```

### Step 3: Start Services

```bash
docker-compose up --build
```

This will:
- Build FastAPI backend image
- Start PostgreSQL database
- Start React development server
- Create necessary volumes

### Step 4: Access Applications

Once all services are running:

```
Backend API:       http://localhost:8000
Frontend:          http://localhost:3000
API Documentation: http://localhost:8000/api/v1/docs
API ReDoc:         http://localhost:8000/api/v1/redoc
PostgreSQL:        localhost:5432
```

### Step 5: Test the Setup

1. **Register User**
   - Go to http://localhost:3000/register
   - Fill in email, password, name
   - Click Register

2. **Login**
   - Go to http://localhost:3000/login
   - Enter registered credentials
   - Click Login

3. **Create Task**
   - Click "+ Create New Task"
   - Enter title and description
   - Click Create Task

4. **Verify API**
   - Go to http://localhost:8000/api/v1/docs
   - Try executing endpoints

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

---

## Local Development Setup

**If you prefer running without Docker**

### Step 1: Clone/Navigate Repository

```bash
# If cloning:
git clone <repository-url>
cd intership
```

### Step 2: Backend Setup

#### Create Python Virtual Environment

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskmanager_db
SECRET_KEY=your-super-secret-key-change-in-production-12345678901234567890
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
APP_NAME=Task Management API
APP_VERSION=1.0.0
DEBUG=True
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### Step 3: Frontend Setup

#### Install Node Dependencies

```bash
cd ../frontend
npm install
```

#### Configure Environment

Create `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000
```

---

## Database Setup

### Step 1: Start PostgreSQL

#### Windows (if installed)
```bash
# PostgreSQL should auto-start
# Or start from Services
```

#### macOS (using Homebrew)
```bash
brew services start postgresql
```

#### Linux (Ubuntu/Debian)
```bash
sudo systemctl start postgresql
```

### Step 2: Create Database

```bash
# Open PostgreSQL prompt
psql -U postgres

# Create database
CREATE DATABASE taskmanager_db;

# List databases
\l

# Exit
\q
```

Or use one command:
```bash
createdb taskmanager_db
```

### Step 3: Verify Connection

```bash
psql -U postgres -d taskmanager_db -c "SELECT version();"
```

---

## Running Backend

### Terminal 1: Start Backend Server

```bash
cd backend

# Activate virtual environment (if not already)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run development server
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Verify Backend

```bash
# In another terminal
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "1.0.0",
#   "app_name": "Task Management API"
# }
```

### View API Documentation

- Swagger: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

---

## Running Frontend

### Terminal 2: Start Frontend Server

```bash
cd frontend
npm start
```

Expected output:
```
Compiled successfully!

You can now view task-management-frontend in the browser.

  Local:            http://localhost:3000
```

Browser should automatically open to http://localhost:3000

### Verify Frontend

- Page loads without errors
- Can navigate to login page
- API connection working (check browser console)

---

## Testing

### Backend Tests

```bash
cd backend

# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=app --cov-report=html tests/

# View coverage report
open htmlcov/index.html
```

### Test Files Included

1. **tests/test_auth.py** - Authentication tests
   - User registration
   - User login
   - Token validation
   - Current user retrieval

2. **tests/test_tasks.py** - Task CRUD tests
   - Task creation
   - Task listing
   - Task updates
   - Task deletion
   - Permission checks

### Example Test Output

```
tests/test_auth.py::test_register_user PASSED           [ 10%]
tests/test_auth.py::test_register_duplicate_email PASSED [ 20%]
tests/test_auth.py::test_login_user PASSED              [ 30%]
...
======================= 12 passed in 0.45s =======================
```

---

## Production Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` to secure random string
- [ ] Set `DEBUG=False`
- [ ] Use environment-specific `.env` files
- [ ] Setup HTTPS/SSL
- [ ] Configure proper logging
- [ ] Setup database backups
- [ ] Enable connection pooling
- [ ] Implement rate limiting
- [ ] Setup error tracking (Sentry)
- [ ] Configure health checks
- [ ] Setup monitoring and alerts

### 1. Production Environment Variables

Create `backend/.env.production`:

```env
DATABASE_URL=postgresql://prod_user:secure_password@prod-host:5432/taskmanager_prod
SECRET_KEY=generate-new-secure-32-character-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

Generate secure secret key:
```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or using OpenSSL
openssl rand -hex 32
```

### 2. Production Build

#### Backend (Gunicorn)

```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

#### Frontend (Build)

```bash
cd frontend
npm run build

# Output in build/ directory
# Deploy to web server (Nginx, Apache, S3, etc.)
```

### 3. Docker Production Build

```bash
# Build images
docker build -t taskmanager-api:latest ./backend
docker build -t taskmanager-frontend:latest ./frontend

# Push to registry
docker push your-registry/taskmanager-api:latest
docker push your-registry/taskmanager-frontend:latest

# Deploy using docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Nginx Configuration

```nginx
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Frontend
    location / {
        root /var/www/frontend;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Cloud Deployment Options

#### Heroku

```bash
# Login
heroku login

# Create app
heroku create taskmanager-app

# Set environment
heroku config:set -a taskmanager-app DATABASE_URL=...

# Deploy
git push heroku main
```

#### AWS

- **Backend**: ECS, Fargate, or EC2
- **Frontend**: S3 + CloudFront
- **Database**: RDS for PostgreSQL
- **DNS**: Route 53

#### DigitalOcean

- **App Platform**: Automated deployment
- **Database**: Managed PostgreSQL
- **App**: Auto-scaling droplets

---

## Troubleshooting

### Python/Backend Issues

**Issue: `ModuleNotFoundError: No module named 'app'`**

```bash
# Solution: Make sure you're in backend directory
cd backend
python -c "import app; print('OK')"
```

**Issue: Database connection error**

```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Verify CONNECTION string
# Format: postgresql://user:password@host:port/database

# Test connection
python -c "from sqlalchemy import create_engine; \
  engine = create_engine('postgresql://postgres:postgres@localhost:5432/taskmanager_db'); \
  print(engine.execute('SELECT 1').fetchone())"
```

**Issue: Port 8000 already in use**

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001 --reload
```

### Node/Frontend Issues

**Issue: `npm: command not found`**

```bash
# Reinstall Node.js from https://nodejs.org/
# Or use package manager:

# macOS (Homebrew)
brew install node

# Windows (Scoop)
scoop install nodejs
```

**Issue: Module not found errors**

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue: Cannot connect to backend**

```bash
# Check API_URL in frontend/.env
# Verify backend is running
curl http://localhost:8000/health

# Check for CORS errors in browser console
# Update CORS_ORIGINS in backend/.env
```

### Database Issues

**Issue: Database doesn't exist**

```bash
createdb taskmanager_db
```

**Issue: Permission denied**

```bash
# Connect as superuser
psql -U postgres
# Then create database
CREATE DATABASE taskmanager_db;
```

**Issue: Cannot connect to database**

```bash
# Verify PostgreSQL is running
psql -U postgres

# Check connection string
# postgresql://username:password@localhost:5432/dbname
```

### Docker Issues

**Issue: Port already in use**

```bash
# Stop other containers
docker ps
docker stop <container-id>

# Or use different port
PORT=8001 docker-compose up
```

**Issue: Build fails**

```bash
# Clear Docker cache and rebuild
docker-compose down -v
docker-compose up --build --no-cache

# Check logs
docker-compose logs backend
```

---

## Performance Tips

### Backend Optimization

1. **Use uvicorn workers**
   ```bash
   uvicorn app.main:app --workers 4
   ```

2. **Enable async**
   ```python
   async def get_user():
       result = await db.query(...)
       return result
   ```

3. **Add caching**
   ```python
   from functools import lru_cache
   @lru_cache(maxsize=128)
   def get_config():
       return settings
   ```

### Frontend Optimization

1. **Code splitting**
   ```javascript
   const Dashboard = React.lazy(() => import('./Dashboard'));
   ```

2. **Memoization**
   ```javascript
   const TaskList = React.memo(({ tasks }) => {
       return tasks.map(task => <TaskCard key={task.id} {...task} />);
   });
   ```

3. **Production build**
   ```bash
   npm run build
   npm install -g serve
   serve -s build
   ```

---

## Monitoring & Logging

### Setup Logging

```python
# backend/app/core/config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### View Logs

```bash
# Real-time logs
tail -f app.log

# Filter by level
grep ERROR app.log
grep INFO app.log
```

### Setup Monitoring

Consider adding:
- **Sentry** - Error tracking
- **DataDog** - Performance monitoring
- **New Relic** - APM
- **Prometheus** + **Grafana** - Metrics

---

## Maintenance

### Regular Tasks

1. **Weekly**
   - Check error logs
   - Monitor disk usage
   - Verify backups

2. **Monthly**
   - Update dependencies
   - Review security logs
   - Performance analysis

3. **Quarterly**
   - Security audit
   - Dependency updates
   - Load testing

### Backup Strategy

```bash
# Backup database
pg_dump taskmanager_db > backup.sql

# Restore database
psql taskmanager_db < backup.sql

# Backup files
tar -czf backup.tar.gz app/
```

### Updates

```bash
# Backend dependencies
pip install -r requirements.txt --upgrade
pip freeze > requirements.txt

# Frontend dependencies
npm update
npm audit fix
```

---

## Support & Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Tools & Services
- [Swagger/OpenAPI](https://swagger.io/)
- [Docker Hub](https://hub.docker.com/)
- [GitHub](https://github.com/)
- [Stack Overflow](https://stackoverflow.com/)

### Community Support
- FastAPI GitHub Discussions
- React Community Discord
- PostgreSQL Support IRC
- Stack Overflow tags: fastapi, react, postgresql

---

**Congratulations! You now have a complete, production-ready task management system running!** 🎉

For questions or issues, refer to the detailed README files in the backend/ and frontend/ directories.
