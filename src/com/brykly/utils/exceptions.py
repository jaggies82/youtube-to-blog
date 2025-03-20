"""Custom exceptions for the package."""

class AgenticError(Exception):
    """Base exception class for all package errors."""
    pass

class ConfigurationError(AgenticError):
    """Exception raised for configuration-related errors."""
    pass

class APIError(AgenticError):
    """Exception raised for API-related errors."""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class VideoProcessingError(AgenticError):
    """Exception raised for video processing errors."""
    pass

class TranscriptError(AgenticError):
    """Exception raised for transcript-related errors."""
    pass

class BlogGenerationError(AgenticError):
    """Exception raised for blog generation errors."""
    pass

class StorageError(AgenticError):
    """Exception raised for storage-related errors."""
    pass

class ValidationError(AgenticError):
    """Exception raised for validation errors."""
    pass 