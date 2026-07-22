"""OpenAI-compatible client."""

from typing import cast

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
    TokenUsage,
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
        """Generate a response using the OpenAI Chat Completions API."""

        messages: list[ChatCompletionMessageParam] = []

        for message in request.messages:
            if message.role == "system":
                messages.append(
                    cast(
                        ChatCompletionSystemMessageParam,
                        {
                            "role": "system",
                            "content": message.content,
                        },
                    )
                )

            elif message.role == "user":
                messages.append(
                    cast(
                        ChatCompletionUserMessageParam,
                        {
                            "role": "user",
                            "content": message.content,
                        },
                    )
                )

            elif message.role == "assistant":
                messages.append(
                    cast(
                        ChatCompletionAssistantMessageParam,
                        {
                            "role": "assistant",
                            "content": message.content,
                        },
                    )
                )

            elif message.role == "tool":
                raise NotImplementedError(
                    "Tool messages are not supported yet."
                )

        response = self._client.chat.completions.create(
            model=self._config.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        choice = response.choices[0]

        usage = None
        if response.usage is not None:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )

        return GenerationResponse(
            content=choice.message.content or "",
            finish_reason=choice.finish_reason,
            model=response.model,
            usage=usage,
        )