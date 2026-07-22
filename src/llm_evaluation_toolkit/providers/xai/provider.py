"""xAI provider."""

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
)
from llm_evaluation_toolkit.providers.base import Provider
from llm_evaluation_toolkit.providers.generator import Generator

from .client import XAIClient
from .config import XAIProviderConfig


class XAIProvider(Provider, Generator):
    """xAI provider implementation."""

    def __init__(self, config: XAIProviderConfig) -> None:
        """Initialize the provider."""
        self._config = config
        self._client = XAIClient(config)

    @property
    def config(self) -> XAIProviderConfig:
        """Return the provider configuration."""
        return self._config

    @property
    def client(self) -> XAIClient:
        """Return the underlying client."""
        return self._client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response."""
        return self._client.generate(request)