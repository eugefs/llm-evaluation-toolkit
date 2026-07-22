"""Anthropic client."""

from anthropic import Anthropic
from anthropic.types import MessageParam, TextBlock, TextBlockParam

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
    TokenUsage,
)

from .config import AnthropicProviderConfig


class AnthropicClient:
    """Wrapper around the official Anthropic SDK."""

    def __init__(self, config: AnthropicProviderConfig) -> None:
        """Initialize the SDK client."""
        self._config = config

        self._client = Anthropic(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
            max_retries=config.max_retries,
            default_headers=config.default_headers,
        )

    @property
    def config(self) -> AnthropicProviderConfig:
        """Return the client configuration."""
        return self._config

    @property
    def sdk(self) -> Anthropic:
        """Return the underlying SDK client."""
        return self._client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response using the Anthropic Messages API."""

        system: str | list[TextBlockParam] | None = None
        messages: list[MessageParam] = []

        for message in request.messages:
            if message.role == "system":
                system = message.content
            elif message.role in ("user", "assistant"):
                messages.append(
                    {
                        "role": message.role,
                        "content": message.content,
                    }
                )
            elif message.role == "tool":
                raise NotImplementedError(
                    "Tool messages are not supported yet."
                )

        if system is None:
            response = self._client.messages.create(
                model=self._config.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
                or self._config.max_tokens,
            )
        else:
            response = self._client.messages.create(
                model=self._config.model,
                messages=messages,
                system=system,
                temperature=request.temperature,
                max_tokens=request.max_tokens
                or self._config.max_tokens,
            )

        text_parts: list[str] = []

        for block in response.content:
            if isinstance(block, TextBlock):
                text_parts.append(block.text)

        usage = TokenUsage(
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            total_tokens=(
                response.usage.input_tokens
                + response.usage.output_tokens
            ),
        )

        return GenerationResponse(
            content="".join(text_parts),
            finish_reason=response.stop_reason,
            model=response.model,
            usage=usage,
        )