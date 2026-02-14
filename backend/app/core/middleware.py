"""Logging middleware for FastAPI application"""
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests and responses"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        """
        Log incoming requests and outgoing responses
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/route handler
            
        Returns:
            Response object
        """
        # Start timer
        start_time = time.time()
        
        # Get request details
        method = request.method
        url = str(request.url)
        client_host = request.client.host if request.client else "unknown"
        
        # Process request
        try:
            response = await call_next(request)
            status_code = response.status_code
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log request and response
            log_message = (
                f"{method} {url} - "
                f"Status: {status_code} - "
                f"Client: {client_host} - "
                f"Duration: {process_time:.3f}s"
            )
            
            # Use different log levels based on status code
            if status_code >= 500:
                logger.error(log_message)
            elif status_code >= 400:
                logger.warning(log_message)
            else:
                logger.info(log_message)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"{method} {url} - "
                f"Error: {str(e)} - "
                f"Client: {client_host} - "
                f"Duration: {process_time:.3f}s",
                exc_info=True
            )
            raise
