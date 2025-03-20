"""Example script demonstrating exception handling in the package."""
import asyncio
import os
import sys
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

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
from com.brykly.utils.logging_config import setup_logging

class ExceptionDemo:
    """Class to demonstrate exception handling."""
    
    def __init__(self):
        """Initialize the demo class."""
        self.logger = setup_logging('exception_demo', {
            'level': 'DEBUG',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': 'logs/exception_demo.log'
        })
    
    async def demonstrate_configuration_error(self):
        """Demonstrate configuration error handling."""
        print("\nDemonstrating configuration error handling...")
        
        try:
            # Simulate missing configuration
            raise ConfigurationError("Missing required configuration: api_key")
        except ConfigurationError as e:
            self.logger.error(f"Configuration error: {str(e)}")
            print(f"✓ Caught ConfigurationError: {str(e)}")
    
    async def demonstrate_api_error(self):
        """Demonstrate API error handling."""
        print("\nDemonstrating API error handling...")
        
        try:
            # Simulate API authentication error
            raise APIError("Invalid API key", status_code=401)
        except APIError as e:
            self.logger.error(f"API error: {str(e)} (Status: {e.status_code})")
            print(f"✓ Caught APIError: {str(e)}")
    
    async def demonstrate_video_processing_error(self):
        """Demonstrate video processing error handling."""
        print("\nDemonstrating video processing error handling...")
        
        try:
            # Simulate video download error
            raise VideoProcessingError("Failed to download video: Network error")
        except VideoProcessingError as e:
            self.logger.error(f"Video processing error: {str(e)}")
            print(f"✓ Caught VideoProcessingError: {str(e)}")
    
    async def demonstrate_transcript_error(self):
        """Demonstrate transcript error handling."""
        print("\nDemonstrating transcript error handling...")
        
        try:
            # Simulate transcript extraction error
            raise TranscriptError("Failed to extract transcript: Invalid video format")
        except TranscriptError as e:
            self.logger.error(f"Transcript error: {str(e)}")
            print(f"✓ Caught TranscriptError: {str(e)}")
    
    async def demonstrate_blog_generation_error(self):
        """Demonstrate blog generation error handling."""
        print("\nDemonstrating blog generation error handling...")
        
        try:
            # Simulate blog generation error
            raise BlogGenerationError("Failed to generate blog post: Invalid prompt")
        except BlogGenerationError as e:
            self.logger.error(f"Blog generation error: {str(e)}")
            print(f"✓ Caught BlogGenerationError: {str(e)}")
    
    async def demonstrate_storage_error(self):
        """Demonstrate storage error handling."""
        print("\nDemonstrating storage error handling...")
        
        try:
            # Simulate storage error
            raise StorageError("Failed to save file: Permission denied")
        except StorageError as e:
            self.logger.error(f"Storage error: {str(e)}")
            print(f"✓ Caught StorageError: {str(e)}")
    
    async def demonstrate_validation_error(self):
        """Demonstrate validation error handling."""
        print("\nDemonstrating validation error handling...")
        
        try:
            # Simulate validation error
            raise ValidationError("Invalid value for field 'temperature': must be between 0 and 1")
        except ValidationError as e:
            self.logger.error(f"Validation error: {str(e)}")
            print(f"✓ Caught ValidationError: {str(e)}")
    
    async def demonstrate_error_hierarchy(self):
        """Demonstrate error hierarchy and catching."""
        print("\nDemonstrating error hierarchy...")
        
        try:
            # Raise a specific error
            raise BlogGenerationError("Blog generation failed")
        except AgenticError as e:
            # Catch the base error class
            self.logger.error(f"Caught base error: {str(e)}")
            print(f"✓ Caught AgenticError: {str(e)}")
    
    async def demonstrate_error_chaining(self):
        """Demonstrate error chaining."""
        print("\nDemonstrating error chaining...")
        
        try:
            try:
                # Simulate a low-level error
                raise ConnectionError("Failed to connect to API")
            except ConnectionError as e:
                # Chain it with a higher-level error
                raise APIError("API request failed") from e
        except APIError as e:
            self.logger.error(f"API error: {str(e)}", exc_info=True)
            print(f"✓ Caught chained error: {str(e)}")
            if e.__cause__:
                print(f"  Caused by: {str(e.__cause__)}")
    
    async def run_demos(self):
        """Run all exception handling demonstrations."""
        print("Starting exception handling demonstration...")
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        try:
            # Run all demonstrations
            await self.demonstrate_configuration_error()
            await self.demonstrate_api_error()
            await self.demonstrate_video_processing_error()
            await self.demonstrate_transcript_error()
            await self.demonstrate_blog_generation_error()
            await self.demonstrate_storage_error()
            await self.demonstrate_validation_error()
            await self.demonstrate_error_hierarchy()
            await self.demonstrate_error_chaining()
            
        except Exception as e:
            self.logger.critical(f"Unexpected error in demonstration: {str(e)}", exc_info=True)
            print(f"✗ Unexpected error: {str(e)}")
        
        print("\nException handling demonstration completed!")

async def main():
    """Main function to run the demonstration."""
    demo = ExceptionDemo()
    await demo.run_demos()

if __name__ == "__main__":
    asyncio.run(main()) 