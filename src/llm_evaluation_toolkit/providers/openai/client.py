"""OpenAI-compatible client."""

from openai import OpenAI

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
)

from .config import OpenAIProviderConfig


class OpenAIClient:
    """Wrapper around the official OpenAI SDK."""

    def __init__(self, config: OpenAIProviderConfig) -> None:
        """Initialize the SDK client."""
        self._config = config
        self._client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
            max_retries=config.max_retries,
            organization=config.organization,
            default_headers=config.default_headers,
        )

    @property
    def config(self) -> OpenAIProviderConfig:
        """Return the client configuration."""
        return self._config

    @property
    def sdk(self) -> OpenAI:
        """Return the underlying OpenAI SDK client."""
        return self._client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response."""
        raise NotImplementedError(
            "OpenAIClient.generate() will be implemented in Milestone 9.3."
        )