from pathlib import Path
from typing import Optional
from loguru import logger
from ..config.configuration_manager import ConfigurationManager

class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._setup_logger()
            self._initialized = True

    def _setup_logger(self) -> None:
        """Configure logger with settings from configuration."""
        config_manager = ConfigurationManager()
        log_config = config_manager.get_logging_config()

        # Remove default logger
        logger.remove()

        # Add console logger
        logger.add(
            lambda msg: print(msg),
            format=log_config.get("format", "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"),
            level=log_config.get("level", "INFO"),
            colorize=True
        )

        # Add file logger if file path is specified
        if log_config.get("file"):
            log_path = Path(log_config["file"])
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            logger.add(
                log_path,
                format=log_config.get("format", "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"),
                level=log_config.get("level", "INFO"),
                rotation=log_config.get("rotation", "1 day"),
                retention=log_config.get("retention", "7 days")
            )

    def debug(self, message: str) -> None:
        """Log debug message."""
        logger.debug(message)

    def info(self, message: str) -> None:
        """Log info message."""
        logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning message."""
        logger.warning(message)

    def error(self, message: str) -> None:
        """Log error message."""
        logger.error(message)

    def critical(self, message: str) -> None:
        """Log critical message."""
        logger.critical(message)

    def exception(self, message: str) -> None:
        """Log exception with traceback."""
        logger.exception(message) 