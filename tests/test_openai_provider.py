"""Tests for the OpenAI-compatible provider skeleton."""

import pytest
from pydantic import ValidationError

from llm_evaluation_toolkit.providers.openai import (
    OpenAIClient,
    OpenAICompatibleProvider,
    OpenAIProviderConfig,
)
from llm_evaluation_toolkit.providers.openai.models import (
    ChatMessage,
    ChatRequest,
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
        OpenAIProviderConfig(model="gpt-4.1-mini")


def test_chat_message() -> None:
    message = ChatMessage(
        role="user",
        content="Hello!",
    )

    assert message.role == "user"
    assert message.content == "Hello!"


def test_chat_request() -> None:
    request = ChatRequest(
        messages=[
            ChatMessage(role="user", content="Hello!")
        ]
    )

    assert len(request.messages) == 1


def test_client_holds_configuration() -> None:
    config = make_config()
    client = OpenAIClient(config)

    assert client.config is config


def test_client_generate_not_implemented() -> None:
    config = make_config()
    client = OpenAIClient(config)

    request = ChatRequest(
        messages=[
            ChatMessage(role="user", content="Hello!")
        ]
    )

    with pytest.raises(NotImplementedError):
        client.generate(request)


def test_provider_initialization() -> None:
    config = make_config()
    provider = OpenAICompatibleProvider(config)

    assert provider.name == "openai"
    assert provider.config is config
    assert isinstance(provider.client, OpenAIClient)