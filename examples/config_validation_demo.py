"""Example script demonstrating configuration validation functionality in the package."""
import os
import sys
import yaml
from pathlib import Path

# Add the package root to the Python path
package_root = Path(__file__).parent.parent
sys.path.append(str(package_root))

from com.brykly.utils.config import ConfigManager
from com.brykly.utils.validation import ConfigValidator

def create_test_configs():
    """Create test configuration files with various scenarios."""
    # Valid configuration
    valid_config = {
        'paths': {
            'output_dir': 'output',
            'temp_dir': 'temp',
            'log_dir': 'logs'
        },
        'api': {
            'openai': {
                'api_key': 'test_key',
                'model': 'gpt-4-turbo-preview',
                'temperature': 0.7,
                'max_tokens': 2000
            },
            'openrouter': {
                'api_key': 'test_key',
                'model': 'anthropic/claude-3-opus-20240229',
                'temperature': 0.7,
                'max_tokens': 2000
            }
        },
        'blog': {
            'default_tone': 'professional',
            'default_style': 'comprehensive'
        }
    }
    
    # Invalid configuration (missing required fields)
    invalid_config_missing = {
        'paths': {
            'output_dir': 'output'
            # Missing temp_dir and log_dir
        },
        'api': {
            'openai': {
                # Missing api_key
                'model': 'gpt-4-turbo-preview'
            }
        }
    }
    
    # Invalid configuration (wrong types)
    invalid_config_types = {
        'paths': {
            'output_dir': 123,  # Should be string
            'temp_dir': 'temp',
            'log_dir': 'logs'
        },
        'api': {
            'openai': {
                'api_key': 'test_key',
                'temperature': 'high'  # Should be float
            }
        }
    }
    
    # Write configurations to files
    configs = {
        'valid_config.yaml': valid_config,
        'invalid_config_missing.yaml': invalid_config_missing,
        'invalid_config_types.yaml': invalid_config_types
    }
    
    for filename, config in configs.items():
        with open(filename, 'w') as f:
            yaml.dump(config, f)
    
    return configs.keys()

def demonstrate_config_validation():
    """Demonstrate configuration validation features."""
    print("Starting configuration validation demonstration...")
    
    # Create test configuration files
    config_files = create_test_configs()
    print(f"\nCreated test configuration files: {', '.join(config_files)}")
    
    # Initialize validator
    validator = ConfigValidator()
    
    # Test valid configuration
    print("\nValidating valid configuration...")
    try:
        config = ConfigManager('valid_config.yaml')
        validator.validate_config(config)
        print("✓ Valid configuration passed validation")
    except Exception as e:
        print(f"✗ Unexpected error with valid configuration: {str(e)}")
    
    # Test configuration with missing fields
    print("\nValidating configuration with missing fields...")
    try:
        config = ConfigManager('invalid_config_missing.yaml')
        validator.validate_config(config)
        print("✗ Invalid configuration unexpectedly passed validation")
    except Exception as e:
        print(f"✓ Caught expected error: {str(e)}")
    
    # Test configuration with wrong types
    print("\nValidating configuration with wrong types...")
    try:
        config = ConfigManager('invalid_config_types.yaml')
        validator.validate_config(config)
        print("✗ Invalid configuration unexpectedly passed validation")
    except Exception as e:
        print(f"✓ Caught expected error: {str(e)}")
    
    # Demonstrate field validation
    print("\nDemonstrating field validation...")
    
    # Validate API key format
    print("\nValidating API key format...")
    api_keys = ['valid_key_123', 'invalid key', '', '123']
    for key in api_keys:
        try:
            validator.validate_api_key(key)
            print(f"API key '{key}': ✓ Valid")
        except Exception as e:
            print(f"API key '{key}': ✗ Invalid - {str(e)}")
    
    # Validate temperature values
    print("\nValidating temperature values...")
    temperatures = [0.0, 0.7, 1.0, -0.1, 1.1, 'invalid']
    for temp in temperatures:
        try:
            validator.validate_temperature(temp)
            print(f"Temperature {temp}: ✓ Valid")
        except Exception as e:
            print(f"Temperature {temp}: ✗ Invalid - {str(e)}")
    
    # Validate directory paths
    print("\nValidating directory paths...")
    paths = ['valid/path', '/absolute/path', '', '../invalid../path']
    for path in paths:
        try:
            validator.validate_path(path)
            print(f"Path '{path}': ✓ Valid")
        except Exception as e:
            print(f"Path '{path}': ✗ Invalid - {str(e)}")
    
    # Clean up test files
    print("\nCleaning up test files...")
    for filename in config_files:
        try:
            os.remove(filename)
            print(f"✓ Removed {filename}")
        except Exception as e:
            print(f"✗ Failed to remove {filename}: {str(e)}")
    
    print("\nConfiguration validation demonstration completed!")

if __name__ == "__main__":
    demonstrate_config_validation() 