"""Tests for the exceptions module."""

import pytest
from com.brykly.utils.exceptions import (
    AgenticError,
    ConfigurationError,
    APIError,
    VideoProcessingError,
    TranscriptError,
    BlogGenerationError,
    StorageError,
    ValidationError
)

def test_agentic_error():
    """Test base AgenticError class."""
    error = AgenticError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)

def test_configuration_error():
    """Test ConfigurationError class."""
    error = ConfigurationError("Missing config")
    assert str(error) == "Missing config"
    assert isinstance(error, AgenticError)

def test_api_error():
    """Test APIError class."""
    error = APIError("API failed", status_code=404)
    assert str(error) == "API failed"
    assert error.status_code == 404
    assert isinstance(error, AgenticError)

def test_video_processing_error():
    """Test VideoProcessingError class."""
    error = VideoProcessingError("Video processing failed")
    assert str(error) == "Video processing failed"
    assert isinstance(error, AgenticError)

def test_transcript_error():
    """Test TranscriptError class."""
    error = TranscriptError("Transcript extraction failed")
    assert str(error) == "Transcript extraction failed"
    assert isinstance(error, AgenticError)

def test_blog_generation_error():
    """Test BlogGenerationError class."""
    error = BlogGenerationError("Blog generation failed")
    assert str(error) == "Blog generation failed"
    assert isinstance(error, AgenticError)

def test_storage_error():
    """Test StorageError class."""
    error = StorageError("Storage operation failed")
    assert str(error) == "Storage operation failed"
    assert isinstance(error, AgenticError)

def test_validation_error():
    """Test ValidationError class."""
    error = ValidationError("Invalid input")
    assert str(error) == "Invalid input"
    assert isinstance(error, AgenticError)

def test_error_hierarchy():
    """Test error hierarchy."""
    # Test that specific errors can be caught by base class
    try:
        raise BlogGenerationError("Test error")
    except AgenticError as e:
        assert str(e) == "Test error"
        assert isinstance(e, BlogGenerationError)
    else:
        pytest.fail("Expected AgenticError to catch BlogGenerationError") 