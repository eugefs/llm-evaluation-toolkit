"""xAI client."""

from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
    TokenUsage,
)

from .config import XAIProviderConfig


class XAIClient:
    """Wrapper around the xAI SDK."""

    def __init__(self, config: XAIProviderConfig) -> None:
        """Initialize the SDK client."""
        self._config = config

        self._client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url or "https://api.x.ai/v1",
            timeout=config.timeout,
        )

    @property
    def config(self) -> XAIProviderConfig:
        """Return the client configuration."""
        return self._config

    @property
    def sdk(self) -> OpenAI:
        """Return the underlying SDK client."""
        return self._client

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response using the xAI Chat Completions API."""

        messages: list[ChatCompletionMessageParam] = [
            cast(
                ChatCompletionMessageParam,
                {
                    "role": message.role,
                    "content": message.content,
                },
            )
            for message in request.messages
        ]

        response = self._client.chat.completions.create(
            model=self._config.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens or self._config.max_tokens,
        )

        choice = response.choices[0]
        usage = response.usage

        return GenerationResponse(
            content=choice.message.content or "",
            finish_reason=choice.finish_reason,
            model=response.model,
            usage=TokenUsage(
                prompt_tokens=usage.prompt_tokens if usage else 0,
                completion_tokens=usage.completion_tokens if usage else 0,
                total_tokens=usage.total_tokens if usage else 0,
            ),
        )