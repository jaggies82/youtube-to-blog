from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..config.configuration_manager import ConfigurationManager
from ..utils.logger import Logger

class ExternalAPIAdapter(ABC):
    """Base class for all external API adapters."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.config_manager = ConfigurationManager()
        self.logger = Logger()
        self.config = self.config_manager.get_api_config(service_name)
        self._authenticated = False

    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the external API."""
        pass

    @abstractmethod
    def execute(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the API request."""
        pass

    def set_configuration(self, config: Dict[str, Any]) -> None:
        """Update the adapter's configuration."""
        self.config.update(config)
        self._authenticated = False  # Reset authentication when config changes

    def validate_config(self, required_keys: list[str]) -> bool:
        """Validate that all required configuration keys are present."""
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            self.logger.error(f"Missing required configuration keys for {self.service_name}: {missing_keys}")
            return False
        return True

    def handle_error(self, error: Exception, context: str) -> None:
        """Handle API errors with proper logging."""
        self.logger.error(f"Error in {self.service_name} during {context}: {str(error)}")
        raise

    def is_authenticated(self) -> bool:
        """Check if the adapter is authenticated."""
        return self._authenticated

    def _set_authenticated(self, status: bool) -> None:
        """Set the authentication status."""
        self._authenticated = status
        if status:
            self.logger.info(f"Successfully authenticated with {self.service_name}")
        else:
            self.logger.warning(f"Authentication failed for {self.service_name}") 