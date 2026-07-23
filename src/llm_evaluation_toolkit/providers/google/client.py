"""Google client."""

from google import genai
from google.genai import types

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
    TokenUsage,
)

from .config import GoogleProviderConfig


class GoogleClient:
    """Wrapper around the Google Gen AI SDK."""

    def __init__(self, config: GoogleProviderConfig) -> None:
        """Initialize the SDK client."""
        self._config = config

        if config.base_url is None:
            self._client = genai.Client(
                api_key=config.api_key,
            )
        else:
            self._client = genai.Client(
                api_key=config.api_key,
                http_options=types.HttpOptions(
                    base_url=config.base_url,
                    timeout=int(config.timeout),
                ),
            )

    @property
    def config(self) -> GoogleProviderConfig:
        """Return the client configuration."""
        return self._config

    @property
    def sdk(self) -> genai.Client:
        """Return the underlying SDK client."""
        return self._client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response using the Google Gen AI API."""

        prompt = "\n".join(
            f"{message.role}: {message.content}"
            for message in request.messages
        )

        response = self._client.models.generate_content(
            model=self._config.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=request.temperature,
                max_output_tokens=(
                    request.max_tokens
                    or self._config.max_tokens
                ),
            ),
        )

        usage_metadata = response.usage_metadata

        usage = TokenUsage(
            prompt_tokens=(
                usage_metadata.prompt_token_count or 0
            )
            if usage_metadata
            else 0,
            completion_tokens=(
                usage_metadata.candidates_token_count or 0
            )
            if usage_metadata
            else 0,
            total_tokens=(
                usage_metadata.total_token_count or 0
            )
            if usage_metadata
            else 0,
        )

        return GenerationResponse(
            content=response.text or "",
            finish_reason=None,
            model=self._config.model,
            usage=usage,
        )