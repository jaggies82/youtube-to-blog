"""Example script demonstrating utility functions in the package."""
import os
import sys
import asyncio
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.utils.config import ConfigManager
from com.brykly.utils.validation import ConfigValidator
from com.brykly.utils.logging_config import setup_logging
from com.brykly.utils.text import TextProcessor
from com.brykly.utils.file import FileHandler

def demonstrate_config_utils():
    """Demonstrate configuration utility functions."""
    print("\nDemonstrating configuration utilities...")
    
    # Create test configuration
    config_data = {
        'paths': {
            'output_dir': 'output',
            'temp_dir': 'temp',
            'log_dir': 'logs'
        },
        'api': {
            'openai': {
                'api_key': 'test_key',
                'model': 'gpt-4-turbo-preview'
            }
        }
    }
    
    # Initialize configuration manager
    config = ConfigManager.from_dict(config_data)
    
    # Demonstrate configuration access
    print("\nAccessing configuration values:")
    print(f"Output directory: {config.get('paths.output_dir')}")
    print(f"OpenAI model: {config.get('api.openai.model')}")
    
    # Demonstrate configuration validation
    validator = ConfigValidator()
    try:
        validator.validate_config(config)
        print("✓ Configuration validation passed")
    except Exception as e:
        print(f"✗ Configuration validation failed: {str(e)}")

def demonstrate_text_utils():
    """Demonstrate text processing utility functions."""
    print("\nDemonstrating text utilities...")
    
    processor = TextProcessor()
    
    # Test text cleaning
    text = """[00:00] This is a test transcript.
    It has multiple lines and timestamps.
    [00:15] Some unnecessary whitespace   and formatting."""
    
    cleaned_text = processor.clean_text(text)
    print("\nCleaned text:")
    print(cleaned_text)
    
    # Test text formatting
    formatted_text = processor.format_text(text)
    print("\nFormatted text:")
    print(formatted_text)
    
    # Test text statistics
    stats = processor.get_text_stats(text)
    print("\nText statistics:")
    print(f"Word count: {stats['word_count']}")
    print(f"Character count: {stats['char_count']}")
    print(f"Line count: {stats['line_count']}")
    
    # Test text summarization
    summary = processor.summarize_text(text)
    print("\nText summary:")
    print(summary)

async def demonstrate_file_utils():
    """Demonstrate file handling utility functions."""
    print("\nDemonstrating file utilities...")
    
    handler = FileHandler()
    
    # Create test content
    test_content = "This is test content for file operations."
    
    # Test file operations
    print("\nTesting file operations:")
    
    # Write file
    await handler.write_file("test.txt", test_content)
    print("✓ File written successfully")
    
    # Read file
    content = await handler.read_file("test.txt")
    print(f"✓ File read successfully: {content}")
    
    # Copy file
    await handler.copy_file("test.txt", "test_copy.txt")
    print("✓ File copied successfully")
    
    # Move file
    await handler.move_file("test_copy.txt", "test_moved.txt")
    print("✓ File moved successfully")
    
    # List files
    files = await handler.list_files(".")
    print(f"✓ Files in directory: {', '.join(files)}")
    
    # Clean up test files
    for file in ["test.txt", "test_moved.txt"]:
        if os.path.exists(file):
            os.remove(file)
    print("✓ Test files cleaned up")

def demonstrate_logging_utils():
    """Demonstrate logging utility functions."""
    print("\nDemonstrating logging utilities...")
    
    # Setup logging configuration
    log_config = {
        'level': 'DEBUG',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'test.log'
    }
    
    # Create logger
    logger = setup_logging('utils_demo', log_config)
    
    # Demonstrate different log levels
    print("\nLogging at different levels:")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Clean up log file
    if os.path.exists(log_config['file']):
        os.remove(log_config['file'])
        print("✓ Log file cleaned up")

async def main():
    """Main function demonstrating utility functions."""
    print("Starting utility functions demonstration...")
    
    try:
        # Demonstrate configuration utilities
        demonstrate_config_utils()
        
        # Demonstrate text utilities
        demonstrate_text_utils()
        
        # Demonstrate file utilities
        await demonstrate_file_utils()
        
        # Demonstrate logging utilities
        demonstrate_logging_utils()
        
    except Exception as e:
        print(f"✗ Error during demonstration: {str(e)}")
    
    print("\nUtility functions demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main()) 