"""Tests for the OpenAI-compatible provider."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from pydantic import ValidationError

from llm_evaluation_toolkit.generation import (
    GenerationMessage,
    GenerationRequest,
)
from llm_evaluation_toolkit.providers.openai import (
    OpenAIClient,
    OpenAICompatibleProvider,
    OpenAIProviderConfig,
)


def make_config() -> OpenAIProviderConfig:
    """Create a valid provider configuration."""
    return OpenAIProviderConfig(
        api_key="test-key",
        model="gpt-4.1-mini",
    )


def test_config_defaults() -> None:
    config = make_config()

    assert config.provider == "openai"
    assert config.base_url == "https://api.openai.com/v1"
    assert config.timeout == 60.0
    assert config.max_retries == 3
    assert config.temperature == 0.0
    assert config.max_tokens is None
    assert config.organization is None
    assert config.default_headers == {}


def test_config_requires_api_key() -> None:
    with pytest.raises(ValidationError):
        OpenAIProviderConfig(
            api_key="",
            model="gpt-4.1-mini",
        )


def test_generation_message() -> None:
    message = GenerationMessage(
        role="user",
        content="Hello!",
    )

    assert message.role == "user"
    assert message.content == "Hello!"


def test_generation_request() -> None:
    request = GenerationRequest(
        messages=[
            GenerationMessage(
                role="user",
                content="Hello!",
            )
        ]
    )

    assert len(request.messages) == 1


def test_client_holds_configuration() -> None:
    config = make_config()
    client = OpenAIClient(config)

    assert client.config is config


def test_client_generate() -> None:
    """The client converts an OpenAI SDK response."""

    config = make_config()
    client = OpenAIClient(config)

    sdk_response = SimpleNamespace(
        model="gpt-4.1-mini",
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content="Hello back!"),
                finish_reason="stop",
            )
        ],
        usage=SimpleNamespace(
            prompt_tokens=5,
            completion_tokens=2,
            total_tokens=7,
        ),
    )

    with patch.object(
        client.sdk.chat.completions,
        "create",
        return_value=sdk_response,
    ) as mock_create:
        response = client.generate(
            GenerationRequest(
                messages=[
                    GenerationMessage(
                        role="user",
                        content="Hello!",
                    )
                ]
            )
        )

    assert response.content == "Hello back!"
    assert response.finish_reason == "stop"
    assert response.model == "gpt-4.1-mini"

    assert response.usage is not None
    assert response.usage.prompt_tokens == 5
    assert response.usage.completion_tokens == 2
    assert response.usage.total_tokens == 7

    mock_create.assert_called_once()


def test_provider_initialization() -> None:
    config = make_config()
    provider = OpenAICompatibleProvider(config)

    assert provider.name == "openai"
    assert provider.config is config
    assert isinstance(provider.client, OpenAIClient)