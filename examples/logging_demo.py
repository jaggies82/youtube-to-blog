"""Example script demonstrating logging functionality in the package."""
import os
import sys
import logging
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.utils.logging_config import setup_logging
from com.brykly.utils.config import ConfigManager

def demonstrate_logging():
    """Demonstrate various logging features."""
    print("Starting logging demonstration...")
    
    # Initialize configuration
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    config = ConfigManager(config_path)
    
    # Setup logging with custom configuration
    log_config = {
        'level': 'DEBUG',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'logs/demo.log'
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Setup logging
    logger = setup_logging('demo', log_config)
    
    # Demonstrate different log levels
    print("\nDemonstrating different log levels:")
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")
    
    # Demonstrate logging with context
    print("\nDemonstrating logging with context:")
    try:
        # Simulate some operation that might fail
        result = 1 / 0
    except Exception as e:
        logger.error(f"An error occurred during calculation: {str(e)}", exc_info=True)
    
    # Demonstrate structured logging
    print("\nDemonstrating structured logging:")
    user_data = {
        'user_id': '12345',
        'action': 'process_video',
        'video_url': 'https://youtube.com/watch?v=example'
    }
    logger.info("Processing video request", extra=user_data)
    
    # Demonstrate log rotation (simulated)
    print("\nDemonstrating log rotation:")
    for i in range(5):
        logger.info(f"Log entry {i+1} to demonstrate rotation")
    
    print("\nLogging demonstration completed!")
    print(f"Log file location: {os.path.abspath(log_config['file'])}")

if __name__ == "__main__":
    demonstrate_logging() 