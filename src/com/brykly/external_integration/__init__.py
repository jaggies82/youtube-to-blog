"""External integration package."""

from .youtube import YouTubeAdapter
from .openai import OpenAIAdapter
from .openrouter import OpenRouterAdapter

__all__ = [
    'YouTubeAdapter',
    'OpenAIAdapter',
    'OpenRouterAdapter'
] 