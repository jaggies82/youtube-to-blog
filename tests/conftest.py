"""Test configuration and shared fixtures."""
import os
import pytest
import yaml
from pathlib import Path
from com.brykly.config.configuration_manager import ConfigurationManager
from com.brykly.utils.logger import Logger
from com.brykly.output_management.output_manager import OutputManager

@pytest.fixture
def test_config():
    """Create test configuration data."""
    return {
        'openai': {
            'api_key': 'test_key',
            'model': 'gpt-4',
            'temperature': 0.7,
            'max_tokens': 2000
        },
        'openrouter': {
            'api_key': 'test_key',
            'model': 'anthropic/claude-3-opus',
            'temperature': 0.7,
            'max_tokens': 2000
        },
        'youtube': {
            'api_key': 'test_key'
        },
        'paths': {
            'temp_dir': '/tmp/test',
            'output_dir': '/tmp/test/output'
        },
        'logging': {
            'level': 'DEBUG',
            'file': '/tmp/test/app.log'
        },
        'output': {
            'directory': '/tmp/test/output',
            'file_naming': '{title}_{date}',
            'templates': {
                'markdown': 'blog_post.md.j2',
                'html': 'blog_post.html.j2',
                'pdf': 'blog_post.pdf.j2'
            }
        }
    }

@pytest.fixture
def test_config_file(test_config, tmp_path):
    """Create a temporary configuration file."""
    config_file = tmp_path / 'config.yaml'
    with open(config_file, 'w') as f:
        yaml.dump(test_config, f)
    return str(config_file)

@pytest.fixture
def test_dirs(tmp_path):
    """Create test directories."""
    temp_dir = tmp_path / 'temp'
    output_dir = tmp_path / 'output'
    temp_dir.mkdir()
    output_dir.mkdir()
    return {'temp_dir': str(temp_dir), 'output_dir': str(output_dir)}

@pytest.fixture
def config_manager(test_config_file):
    """Create a configuration manager instance."""
    return ConfigurationManager(test_config_file)

@pytest.fixture
def output_manager(config_manager):
    """Create an output manager instance."""
    return OutputManager(config_manager)

@pytest.fixture
def logger():
    """Fixture for logger."""
    return Logger()

@pytest.fixture
def sample_blog_post():
    """Create a sample blog post for testing."""
    return {
        'title': 'Test Blog Post',
        'content': '# Test Blog Post\n\nThis is a test blog post.',
        'metadata': {
            'author': 'Test Author',
            'date': '2024-03-20',
            'tags': ['test', 'blog']
        }
    }

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / 'output'
    output_dir.mkdir()
    return str(output_dir)

@pytest.fixture
def mock_config():
    """Fixture for mock configuration."""
    return {
        "api": {
            "openai": {
                "model": "gpt-4-turbo-preview",
                "temperature": 0.7
            },
            "yolo": {
                "model": "yolov8n.pt",
                "confidence_threshold": 0.5
            }
        },
        "output": {
            "formats": ["markdown", "html", "pdf"],
            "directory": "./output",
            "file_naming": "{title}_{date}"
        },
        "logging": {
            "level": "INFO",
            "file": "logs/test.log"
        }
    } 