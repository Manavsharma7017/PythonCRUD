"""FastAPI Application Entry Point"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.v1.auth import router as auth_router
from app.api.v1.tasks import router as tasks_router
from app.core.logger import get_logger, LoggerSetup
from app.core.middleware import LoggingMiddleware

# Initialize logging
LoggerSetup.setup_logger()
logger = get_logger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created/verified successfully")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready task management API with JWT authentication and role-based access control",
    version=settings.APP_VERSION,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

logger.info(f"FastAPI application initialized: {settings.APP_NAME} v{settings.APP_VERSION}")

# Add logging middleware (before CORS to log all requests)
app.add_middleware(LoggingMiddleware)
logger.info("Logging middleware added")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"CORS middleware added with origins: {settings.CORS_ORIGINS}")


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Log application startup"""
    logger.info("="*60)
    logger.info(f"Application starting up: {settings.APP_NAME}")
    logger.info(f"Version: {settings.APP_VERSION}")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    logger.info(f"Server: {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    logger.info("="*60)


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown"""
    logger.info("="*60)
    logger.info(f"Application shutting down: {settings.APP_NAME}")
    logger.info("="*60)


# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(
        f"Validation error on {request.method} {request.url.path}: {exc.errors()}"
    )
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
        },
    )


# Global exception handler for unhandled errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred",
        },
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
    }


# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)
logger.info("API routers registered successfully")


@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/api/v1/docs",
        "redoc": "/api/v1/redoc",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug",
    )
