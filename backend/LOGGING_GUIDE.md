# Production Logging Guide

## Overview
This FastAPI application now includes comprehensive production-ready logging that captures all critical events, requests, and errors.

## Features

### ✅ Implemented Logging Features

1. **Dual Output**: Logs are written to both `logs/server.log` and console
2. **Auto-directory Creation**: `logs/` directory is created automatically
3. **Structured Format**: Includes timestamp, log level, module name, function, line number, and message
4. **Log Rotation**: Files rotate at 10MB with 5 backup files
5. **Request/Response Logging**: Middleware logs all HTTP requests automatically
6. **No Duplicates**: Configured to prevent duplicate log entries

## Log Locations

- **File**: `backend/logs/server.log`
- **Console**: stdout (visible when running the server)
- **Rotated files**: `server.log.1`, `server.log.2`, etc.

## Log Format

### File Logs (Detailed)
```
2026-02-14 10:30:45 - INFO - app.main - startup_event:42 - Application starting up: Task Manager API
```

### Console Logs (Simplified)
```
2026-02-14 10:30:45 - INFO - app.main - Application starting up: Task Manager API
```

## What Gets Logged

### 1. Application Lifecycle
```python
# Startup
"Application starting up: Task Manager API"
"Version: 1.0.0"
"Environment: Production"
"Server: 0.0.0.0:8000"

# Shutdown
"Application shutting down: Task Manager API"
```

### 2. User Registration
```python
# Success
"New user registered successfully: user@example.com (ID: 123)"

# Failure (email exists)
"Registration attempt with already registered email: user@example.com"
```

### 3. User Login
```python
# Success
"User logged in successfully: user@example.com (ID: 123)"

# Failed (wrong password)
"Failed login attempt for email: user@example.com"

# Failed (inactive account)
"Login attempt for inactive user: user@example.com"
```

### 4. Task Operations
```python
# Create
"Task created: ID=42, Title='Complete project', Owner=user@example.com"

# Update
"Task updated: ID=42, Title='Complete project', User=user@example.com"

# Delete
"Task deleted: ID=42, User=user@example.com"
```

### 5. Unauthorized Access Attempts
```python
# Invalid token
"Invalid token provided - token verification failed"

# Missing user
"User not found for token - User ID: 999"

# Permission denied (admin required)
"Admin access denied for user: user@example.com"

# Permission denied (task access)
"Unauthorized task access attempt: Task ID=42, User=other@example.com"

# Permission denied (task update)
"Unauthorized task update attempt: Task ID=42, User=other@example.com"

# Permission denied (task delete)
"Unauthorized task deletion attempt: Task ID=42, User=other@example.com"
```

### 6. HTTP Requests (Via Middleware)
```python
# Successful request
"POST /api/v1/auth/login - Status: 200 - Client: 192.168.1.100 - Duration: 0.234s"

# Client error
"GET /api/v1/tasks/999 - Status: 404 - Client: 192.168.1.100 - Duration: 0.045s"

# Server error
"POST /api/v1/tasks - Status: 500 - Client: 192.168.1.100 - Duration: 0.123s"
```

## Usage Examples

### Basic Usage in New Modules
```python
from app.core.logger import get_logger

logger = get_logger(__name__)

def my_function():
    logger.info("Function started")
    logger.warning("Something unusual happened")
    logger.error("An error occurred", exc_info=True)
```

### Logging with Context
```python
logger.info(f"User {user.email} performed action on resource {resource_id}")
```

### Error Logging with Traceback
```python
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {str(e)}", exc_info=True)
    raise
```

## Log Levels

The application uses the following log levels:

| Level | Usage | Example |
|-------|-------|---------|
| **INFO** | Normal operations | User login, task creation |
| **WARNING** | Unexpected but handled events | Failed login, unauthorized access |
| **ERROR** | Errors and exceptions | Server errors, database failures |
| **DEBUG** | Detailed diagnostic info | (Not used in production by default) |

## Configuration

### Changing Log Level
Edit `app/core/logger.py`:
```python
LoggerSetup.setup_logger(log_level="DEBUG")  # or "WARNING", "ERROR"
```

### Changing Log File Location
```python
LoggerSetup.setup_logger(log_file="logs/custom.log")
```

### Adjusting Rotation Settings
```python
LoggerSetup.setup_logger(
    max_bytes=20971520,  # 20MB
    backup_count=10      # Keep 10 backup files
)
```

## Testing the Logging

### 1. Start the Server
```bash
cd backend
python -app/main.py
```

You should see:
```
2026-02-14 10:30:45 - INFO - app.main - Database tables created/verified successfully
2026-02-14 10:30:45 - INFO - app.main - FastAPI application initialized: Task Manager API v1.0.0
2026-02-14 10:30:45 - INFO - app.main - Logging middleware added
2026-02-14 10:30:45 - INFO - app.main - CORS middleware added with origins: ['http://localhost:3000']
2026-02-14 10:30:45 - INFO - app.main - API routers registered successfully
2026-02-14 10:30:45 - INFO - app.main - ============================================================
2026-02-14 10:30:45 - INFO - app.main - Application starting up: Task Manager API
2026-02-14 10:30:45 - INFO - app.main - Version: 1.0.0
2026-02-14 10:30:45 - INFO - app.main - Environment: Production
2026-02-14 10:30:45 - INFO - app.main - Server: 0.0.0.0:8000
2026-02-14 10:30:45 - INFO - app.main - ============================================================
```

### 2. Register a User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Expected log:
```
2026-02-14 10:31:00 - INFO - app.api.v1.auth - New user registered successfully: test@example.com (ID: 1)
2026-02-14 10:31:00 - INFO - app.core.middleware - POST http://localhost:8000/api/v1/auth/register - Status: 201 - Client: 127.0.0.1 - Duration: 0.156s
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

Expected log:
```
2026-02-14 10:32:00 - INFO - app.api.v1.auth - User logged in successfully: test@example.com (ID: 1)
2026-02-14 10:32:00 - INFO - app.core.middleware - POST http://localhost:8000/api/v1/auth/login - Status: 200 - Client: 127.0.0.1 - Duration: 0.089s
```

### 4. Failed Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"wrongpassword"}'
```

Expected log:
```
2026-02-14 10:33:00 - WARNING - app.api.v1.auth - Failed login attempt for email: test@example.com
2026-02-14 10:33:00 - WARNING - app.core.middleware - POST http://localhost:8000/api/v1/auth/login - Status: 401 - Client: 127.0.0.1 - Duration: 0.045s
```

### 5. Create a Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"Test Task","description":"Test","status":"todo"}'
```

Expected log:
```
2026-02-14 10:34:00 - INFO - app.api.v1.tasks - Task created: ID=1, Title='Test Task', Owner=test@example.com
2026-02-14 10:34:00 - INFO - app.core.middleware - POST http://localhost:8000/api/v1/tasks - Status: 201 - Client: 127.0.0.1 - Duration: 0.067s
```

### 6. Unauthorized Access
```bash
curl -X GET http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer INVALID_TOKEN"
```

Expected log:
```
2026-02-14 10:35:00 - WARNING - app.core.dependencies - Invalid token provided - token verification failed
2026-02-14 10:35:00 - WARNING - app.core.middleware - GET http://localhost:8000/api/v1/tasks/1 - Status: 401 - Client: 127.0.0.1 - Duration: 0.012s
```

## Checking Log Files

### View Recent Logs
```bash
# Linux/Mac
tail -f backend/logs/server.log

# Windows PowerShell
Get-Content backend\logs\server.log -Wait -Tail 50
```

### Search Logs
```bash
# Linux/Mac
grep "ERROR" backend/logs/server.log
grep "user@example.com" backend/logs/server.log

# Windows PowerShell
Select-String -Path backend\logs\server.log -Pattern "ERROR"
Select-String -Path backend\logs\server.log -Pattern "user@example.com"
```

## Best Practices

1. **Don't log sensitive data**: Passwords, tokens, or personal data
2. **Use appropriate log levels**: INFO for normal ops, WARNING for issues, ERROR for failures
3. **Include context**: User IDs, resource IDs, relevant details
4. **Be concise**: Clear but brief messages
5. **Use structured logging**: Consistent format for easy parsing

## Troubleshooting

### Logs Directory Not Created
The directory is created automatically. If you see errors, check write permissions:
```bash
chmod 755 backend/logs  # Linux/Mac
```

### No Logs Appearing
1. Check that the application started without errors
2. Verify `logs/server.log` exists
3. Check file permissions
4. Ensure logger is initialized in `main.py`

### Duplicate Logs
The configuration prevents duplicates by:
- Setting `logger.propagate = False`
- Checking for existing handlers before adding new ones
- Initializing the root logger only once

### Log Files Growing Too Large
Adjust rotation settings in `logger.py`:
```python
LoggerSetup.setup_logger(
    max_bytes=5242880,   # 5MB (smaller)
    backup_count=3       # Fewer backups
)
```

## Files Modified

1. **Created**:
   - `app/core/logger.py` - Logging configuration
   - `app/core/middleware.py` - Request/response logging middleware

2. **Modified**:
   - `app/main.py` - Integration and startup logging
   - `app/api/v1/auth.py` - Authentication event logging
   - `app/api/v1/tasks.py` - Task operation logging
   - `app/core/dependencies.py` - Authorization failure logging

## Summary

✅ Production-ready logging is now fully integrated
✅ All requirements met (timestamps, dual output, auto-creation, etc.)
✅ Comprehensive event coverage (startup, auth, tasks, errors)
✅ Request/response middleware active
✅ No code changes needed - works out of the box
✅ Clean, scalable, maintainable structure
