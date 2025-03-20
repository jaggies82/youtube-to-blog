"""Constants module."""

import os
from pathlib import Path

# File paths
DEFAULT_CONFIG_FILE = os.path.join(os.getcwd(), 'config.yaml')
DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
DEFAULT_TEMP_DIR = os.path.join(os.getcwd(), 'temp')
DEFAULT_LOG_DIR = os.path.join(os.getcwd(), 'logs')

# File extensions
TRANSCRIPT_EXT = '.txt'
BLOG_POST_EXT = '.md'

# API settings
DEFAULT_OPENAI_MODEL = 'gpt-4-turbo-preview'
DEFAULT_OPENAI_TEMPERATURE = 0.7
DEFAULT_OPENAI_MAX_TOKENS = 2000

# Blog post settings
DEFAULT_TONE = 'professional'
DEFAULT_STYLE = 'comprehensive'

# Logging settings
DEFAULT_LOG_LEVEL = 'INFO'
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_LOG_FILE = os.path.join(DEFAULT_LOG_DIR, 'app.log') 