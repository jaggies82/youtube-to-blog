from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from loguru import logger
from dotenv import load_dotenv
import os

class ConfigurationManager:
    _instance = None
    _config: Dict[str, Any] = {}
    _config_path: Optional[Path] = None

    def __new__(cls, config_path: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(cls)
            if config_path:
                cls._config_path = Path(config_path)
        return cls._instance

    def __init__(self, config_path: Optional[str] = None):
        if not self._config:
            if config_path:
                self._config_path = Path(config_path)
            self._load_config()
            self._load_environment_variables()

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if not self._config_path:
            self._config_path = Path(__file__).parent / "config.yaml"
        try:
            with open(self._config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def _load_environment_variables(self) -> None:
        """Load environment variables and override config values."""
        load_dotenv()
        # Override API keys and sensitive data from environment variables
        if os.getenv("OPENAI_API_KEY"):
            self._config["api"]["openai"]["api_key"] = os.getenv("OPENAI_API_KEY")
        if os.getenv("YOLO_MODEL_PATH"):
            self._config["api"]["yolo"]["model"] = os.getenv("YOLO_MODEL_PATH")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key."""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value

    def get_api_config(self, service_name: str) -> Dict[str, Any]:
        """Get API configuration for a specific service."""
        return self.get(f"api.{service_name}", {})

    def get_workflow_config(self) -> Dict[str, Any]:
        """Get workflow configuration."""
        return self.get("workflow", {})

    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration."""
        return self.get("output", {})

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.get("logging", {})

    def get_mode_config(self, mode: str) -> Dict[str, Any]:
        """Get configuration for a specific processing mode."""
        return self.get(f"modes.{mode}", {}) 