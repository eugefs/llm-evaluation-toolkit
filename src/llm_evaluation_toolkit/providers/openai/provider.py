"""OpenAI-compatible provider."""

from llm_evaluation_toolkit.providers.base import Provider

from .client import OpenAIClient
from .config import OpenAIProviderConfig


class OpenAICompatibleProvider(Provider):
    """Provider implementation for OpenAI-compatible APIs."""

    def __init__(self, config: OpenAIProviderConfig) -> None:
        """Initialize the provider."""
        self._config = config
        self._client = OpenAIClient(config)

    @property
    def name(self) -> str:
        """Return the provider name."""
        return self._config.provider

    @property
    def config(self) -> OpenAIProviderConfig:
        """Return the provider configuration."""
        return self._config

    @property
    def client(self) -> OpenAIClient:
        """Return the underlying client."""
        return self._client