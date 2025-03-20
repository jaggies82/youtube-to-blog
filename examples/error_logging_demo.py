"""Example script demonstrating error handling and logging integration in the package."""
import asyncio
import os
import sys
import logging
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.utils.logging_config import setup_logging
from com.brykly.utils.config import ConfigManager
from com.brykly.services.youtube import YouTubeService
from com.brykly.services.transcript import TranscriptManager
from com.brykly.services.openai import OpenAIService

class CustomError(Exception):
    """Custom error for demonstration purposes."""
    pass

async def simulate_service_error(logger):
    """Simulate a service error with proper logging."""
    try:
        logger.info("Attempting a service operation that will fail...")
        raise CustomError("Simulated service error")
    except CustomError as e:
        logger.error(f"Service operation failed: {str(e)}", exc_info=True)
        raise

async def demonstrate_error_handling(logger):
    """Demonstrate error handling with logging."""
    print("\nDemonstrating error handling with logging...")
    
    try:
        # Simulate a service error
        await simulate_service_error(logger)
    except CustomError as e:
        logger.warning("Caught CustomError, attempting recovery...")
        print(f"✓ Successfully caught and handled CustomError: {str(e)}")
    
    # Demonstrate error handling with YouTube service
    try:
        logger.info("Attempting to process invalid YouTube URL...")
        service = YouTubeService("config.yaml")
        await service.get_video_info("invalid_url")
    except Exception as e:
        logger.error(f"YouTube service error: {str(e)}", exc_info=True)
        print(f"✓ Successfully caught YouTube service error: {str(e)}")
    
    # Demonstrate error handling with transcript service
    try:
        logger.info("Attempting to process non-existent video file...")
        service = TranscriptManager("config.yaml")
        await service.extract_transcript("nonexistent.mp4")
    except Exception as e:
        logger.error(f"Transcript service error: {str(e)}", exc_info=True)
        print(f"✓ Successfully caught transcript service error: {str(e)}")
    
    # Demonstrate error handling with OpenAI service
    try:
        logger.info("Attempting to generate blog post without API key...")
        service = OpenAIService("config.yaml")
        await service.generate_blog_post("test content", "casual", "concise")
    except Exception as e:
        logger.error(f"OpenAI service error: {str(e)}", exc_info=True)
        print(f"✓ Successfully caught OpenAI service error: {str(e)}")

async def demonstrate_logging_levels(logger):
    """Demonstrate different logging levels."""
    print("\nDemonstrating logging levels...")
    
    logger.debug("This is a DEBUG message - detailed information for debugging")
    logger.info("This is an INFO message - general information about program execution")
    logger.warning("This is a WARNING message - something unexpected happened")
    logger.error("This is an ERROR message - the software failed to perform some function")
    logger.critical("This is a CRITICAL message - program may not be able to continue")

async def demonstrate_structured_logging(logger):
    """Demonstrate structured logging with context."""
    print("\nDemonstrating structured logging...")
    
    # Log with extra context
    context = {
        'user_id': 'test_user',
        'operation': 'video_processing',
        'video_url': 'https://youtube.com/watch?v=test'
    }
    
    logger.info("Starting video processing operation", extra=context)
    
    try:
        raise CustomError("Operation failed")
    except CustomError as e:
        logger.error(
            "Video processing failed",
            extra={**context, 'error': str(e), 'error_type': type(e).__name__}
        )

async def main():
    """Main function demonstrating error handling and logging features."""
    print("Starting error handling and logging demonstration...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Setup logging
    log_config = {
        'level': 'DEBUG',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'logs/error_demo.log'
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Setup logger
    logger = setup_logging('error_demo', log_config)
    
    try:
        # Demonstrate error handling
        await demonstrate_error_handling(logger)
        
        # Demonstrate logging levels
        await demonstrate_logging_levels(logger)
        
        # Demonstrate structured logging
        await demonstrate_structured_logging(logger)
        
    except Exception as e:
        logger.critical(f"Unexpected error in demonstration: {str(e)}", exc_info=True)
        raise
    finally:
        print(f"\nLog file location: {os.path.abspath(log_config['file'])}")
    
    print("\nError handling and logging demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main()) 