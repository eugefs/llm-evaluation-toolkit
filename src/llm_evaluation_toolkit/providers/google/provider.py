"""Google provider."""

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
)
from llm_evaluation_toolkit.providers.base import Provider
from llm_evaluation_toolkit.providers.generator import Generator

from .client import GoogleClient
from .config import GoogleProviderConfig


class GoogleProvider(Provider, Generator):
    """Google provider implementation."""

    def __init__(self, config: GoogleProviderConfig) -> None:
        """Initialize the provider."""
        self._config = config
        self._client = GoogleClient(config)

    @property
    def config(self) -> GoogleProviderConfig:
        """Return the provider configuration."""
        return self._config

    @property
    def client(self) -> GoogleClient:
        """Return the underlying client."""
        return self._client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response."""
        return self._client.generate(request)