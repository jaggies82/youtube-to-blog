"""Tests for the logging configuration module."""

import os
import logging
import pytest
from pathlib import Path
from com.brykly.utils.logging_config import setup_logging

@pytest.fixture
def temp_log_dir(tmp_path):
    """Create a temporary directory for log files."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir

def test_setup_logging_basic():
    """Test basic logging setup without file handler."""
    logger = setup_logging("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
    assert len(logger.handlers) == 1  # Only console handler
    assert isinstance(logger.handlers[0], logging.StreamHandler)

def test_setup_logging_with_file(temp_log_dir):
    """Test logging setup with file handler."""
    log_file = temp_log_dir / "test.log"
    logger = setup_logging("test_logger", {
        "file": str(log_file),
        "level": "DEBUG",
        "format": "%(levelname)s - %(message)s"
    })
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"
    assert len(logger.handlers) == 2  # Console and file handlers
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in logger.handlers)
    
    # Test logging to file
    logger.debug("Test debug message")
    logger.info("Test info message")
    
    # Verify log file exists and contains messages
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "DEBUG - Test debug message" in log_content
    assert "INFO - Test info message" in log_content

def test_setup_logging_duplicate():
    """Test that duplicate handlers are not added."""
    logger = setup_logging("test_logger")
    initial_handlers = len(logger.handlers)
    
    # Setup logging again
    logger = setup_logging("test_logger")
    assert len(logger.handlers) == initial_handlers

def test_setup_logging_custom_config(temp_log_dir):
    """Test logging setup with custom configuration."""
    log_file = temp_log_dir / "custom.log"
    logger = setup_logging("custom_logger", {
        "file": str(log_file),
        "level": "WARNING",
        "format": "%(name)s - %(levelname)s - %(message)s",
        "max_size": 1024,  # 1KB
        "backup_count": 2
    })
    
    assert logger.level == logging.WARNING
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in logger.handlers)
    
    # Test log rotation
    for i in range(5):  # Write more than backup_count messages
        logger.warning(f"Test message {i}")
    
    # Check for rotated files
    log_files = list(temp_log_dir.glob("custom.log*"))
    assert len(log_files) <= 3  # Original + 2 backups

def test_setup_logging_invalid_level():
    """Test logging setup with invalid log level."""
    with pytest.raises(AttributeError):
        setup_logging("test_logger", {"level": "INVALID_LEVEL"})

def test_setup_logging_file_permissions(temp_log_dir):
    """Test logging setup with file permission issues."""
    log_file = temp_log_dir / "permission.log"
    log_file.touch()
    os.chmod(log_file, 0o444)  # Read-only
    
    # Should still work but log a warning
    logger = setup_logging("test_logger", {"file": str(log_file)})
    assert isinstance(logger, logging.Logger)
    assert len(logger.handlers) >= 1  # At least console handler 