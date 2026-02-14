"""Production-ready logging configuration for FastAPI application"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


class LoggerSetup:
    """Centralized logging configuration"""
    
    _initialized = False
    
    @staticmethod
    def setup_logger(
        name: Optional[str] = None,
        log_level: str = "INFO",
        log_file: str = "logs/server.log",
        max_bytes: int = 10485760,  # 10MB
        backup_count: int = 5,
    ) -> logging.Logger:
        """
        Configure and return a logger instance
        
        Args:
            name: Logger name (defaults to root logger if None)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            
        Returns:
            Configured logger instance
        """
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get or create logger
        logger = logging.getLogger(name)
        
        # Avoid duplicate handlers if logger is already configured
        if LoggerSetup._initialized and name is None:
            return logger
        
        # Set log level
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        console_formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger (avoid duplicates)
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        # Prevent propagation to avoid duplicate logs
        logger.propagate = False
        
        if name is None:
            LoggerSetup._initialized = True
        
        return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get a logger instance for a specific module
    
    Args:
        name: Name of the module/logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Initialize root logger on module import
root_logger = LoggerSetup.setup_logger()
