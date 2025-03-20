"""Logging configuration module."""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any

from .config import ConfigManager
from .constants import DEFAULT_LOG_LEVEL, DEFAULT_LOG_FORMAT, DEFAULT_LOG_FILE

def setup_logging(name: str, config: Dict[str, Any] = None) -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        name: Name of the logger
        config: Optional dictionary containing logging configuration
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Set log level
    log_level = config.get('level', DEFAULT_LOG_LEVEL) if config else DEFAULT_LOG_LEVEL
    try:
        logger.setLevel(getattr(logging, log_level.upper()))
    except AttributeError:
        raise AttributeError(f"Invalid log level: {log_level}")
    
    # Create formatters
    formatter = logging.Formatter(
        config.get('format', DEFAULT_LOG_FORMAT) if config else DEFAULT_LOG_FORMAT
    )
    
    # Create handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)
    
    # File handler if file path is provided
    if config and 'file' in config:
        log_file = config['file']
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            # Create rotating file handler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=config.get('max_size', 10 * 1024 * 1024),  # 10MB default
                backupCount=config.get('backup_count', 5)
            )
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
        except (PermissionError, OSError) as e:
            # Log a warning and continue with console handler only
            logging.warning(f"Failed to create file handler: {e}")
    
    # Add handlers to logger
    for handler in handlers:
        logger.addHandler(handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger

# Set specific log levels for third-party libraries
logging.getLogger('yt_dlp').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.INFO)
logging.getLogger('youtube_transcript_api').setLevel(logging.WARNING)

# Log startup message
logging.getLogger().info('Logging configured successfully') 