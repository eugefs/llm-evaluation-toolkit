"""Anthropic provider."""

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
)
from llm_evaluation_toolkit.providers.base import Provider
from llm_evaluation_toolkit.providers.generator import Generator

from .client import AnthropicClient
from .config import AnthropicProviderConfig


class AnthropicProvider(Provider, Generator):
    """Anthropic provider implementation."""

    def __init__(self, config: AnthropicProviderConfig) -> None:
        """Initialize the provider."""
        self._config = config
        self._client = AnthropicClient(config)

    @property
    def name(self) -> str:
        """Return provider name."""
        return "anthropic"

    @property
    def config(self) -> AnthropicProviderConfig:
        """Return the provider configuration."""
        return self._config

    @property
    def client(self) -> AnthropicClient:
        """Return the underlying client."""
        return self._client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response."""
        return self._client.generate(request)