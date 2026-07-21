"""OpenAI-compatible client placeholder."""

from .config import OpenAIProviderConfig
from .models import ChatRequest, ChatResponse


class OpenAIClient:
    """Placeholder client for an OpenAI-compatible API."""

    def __init__(self, config: OpenAIProviderConfig) -> None:
        """Initialize the client."""
        self._config = config

    @property
    def config(self) -> OpenAIProviderConfig:
        """Return the client configuration."""
        return self._config

    def generate(self, request: ChatRequest) -> ChatResponse:
        """Generate a chat completion."""
        raise NotImplementedError(
            "OpenAIClient.generate() will be implemented in Milestone 9.2."
        )