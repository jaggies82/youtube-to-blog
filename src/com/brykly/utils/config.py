"""Configuration management module."""

import os
import yaml
from typing import Dict, Any, Optional

class ConfigManager:
    """Configuration manager class."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize the configuration manager."""
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and save to file."""
        self.config[key] = value
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f) 