"""Example script demonstrating configuration management in the package."""
import os
import sys
import yaml
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.utils.config import ConfigManager

def create_sample_config():
    """Create a sample configuration file with different settings."""
    config = {
        'paths': {
            'output_dir': 'custom_output',
            'temp_dir': 'custom_temp',
            'log_dir': 'custom_logs'
        },
        'api': {
            'openai': {
                'api_key': 'your_openai_api_key',
                'model': 'gpt-4-turbo-preview',
                'temperature': 0.8,
                'max_tokens': 3000
            },
            'openrouter': {
                'api_key': 'your_openrouter_api_key',
                'model': 'anthropic/claude-3-opus-20240229',
                'temperature': 0.8,
                'max_tokens': 3000
            }
        },
        'blog': {
            'default_tone': 'casual',
            'default_style': 'concise',
            'output_format': 'markdown'
        },
        'logging': {
            'level': 'DEBUG',
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'file': 'custom_logs/app.log'
        }
    }
    
    config_path = 'custom_config.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    return config_path

def demonstrate_config_usage():
    """Demonstrate various configuration management features."""
    print("Starting configuration management demonstration...")
    
    # Create a sample configuration file
    config_path = create_sample_config()
    print(f"\nCreated sample configuration file: {config_path}")
    
    # Initialize configuration manager
    config = ConfigManager(config_path)
    
    # Demonstrate getting configuration values
    print("\nGetting configuration values:")
    print(f"Output directory: {config.get('paths.output_dir')}")
    print(f"OpenAI model: {config.get('api.openai.model')}")
    print(f"Default blog tone: {config.get('blog.default_tone')}")
    
    # Demonstrate getting values with defaults
    print("\nGetting values with defaults:")
    print(f"Custom setting (with default): {config.get('custom.setting', 'default_value')}")
    
    # Demonstrate updating configuration
    print("\nUpdating configuration:")
    config.set('blog.default_tone', 'formal')
    print(f"Updated blog tone: {config.get('blog.default_tone')}")
    
    # Demonstrate nested configuration access
    print("\nAccessing nested configuration:")
    openai_config = config.get('api.openai')
    print(f"OpenAI configuration: {openai_config}")
    
    # Demonstrate error handling
    print("\nDemonstrating error handling:")
    try:
        invalid_path = config.get('invalid.path')
        print("This should not be printed")
    except KeyError as e:
        print(f"✓ Caught expected KeyError: {str(e)}")
    
    print("\nConfiguration management demonstration completed!")

if __name__ == "__main__":
    demonstrate_config_usage() 