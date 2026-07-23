"""Provider contract tests."""

import pytest

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
    TokenUsage,
)
from llm_evaluation_toolkit.providers import (
    AnthropicProvider,
    AnthropicProviderConfig,
    GoogleProvider,
    GoogleProviderConfig,
    OpenAICompatibleProvider,
    OpenAIProviderConfig,
    Provider,
    XAIProvider,
    XAIProviderConfig,
)


class MockClient:
    """Fake client for provider contract tests."""

    def generate(
        self,
        generation_request: GenerationRequest,
    ) -> GenerationResponse:
        """Return deterministic response."""
        return GenerationResponse(
            content="mock response",
            finish_reason="stop",
            model="mock-model",
            usage=TokenUsage(
                prompt_tokens=1,
                completion_tokens=1,
                total_tokens=2,
            ),
        )


@pytest.fixture
def generation_request() -> GenerationRequest:
    """Create test generation request."""
    return GenerationRequest(
        messages=[
            {
                "role": "user",
                "content": "Hello",
            }
        ],
    )


@pytest.fixture
def providers() -> list[Provider]:
    """Create provider instances."""
    return [
        OpenAICompatibleProvider(
            OpenAIProviderConfig(
                api_key="test-key",
                model="test-model",
            )
        ),
        AnthropicProvider(
            AnthropicProviderConfig(
                api_key="test-key",
                model="test-model",
            )
        ),
        GoogleProvider(
            GoogleProviderConfig(
                api_key="test-key",
                model="test-model",
            )
        ),
        XAIProvider(
            XAIProviderConfig(
                api_key="test-key",
                model="test-model",
            )
        ),
    ]


@pytest.mark.parametrize(
    "provider_index",
    range(4),
)
def test_provider_has_generate_contract(
    providers: list[Provider],
    provider_index: int,
    monkeypatch,
    generation_request: GenerationRequest,
) -> None:
    """All providers implement generation contract."""

    provider = providers[provider_index]

    monkeypatch.setattr(
        provider,
        "_client",
        MockClient(),
    )

    response = provider.generate(
        generation_request,
    )

    assert isinstance(
        response,
        GenerationResponse,
    )

    assert response.content
    assert response.model
    assert response.usage.total_tokens >= 0


def test_provider_names_are_unique(
    providers: list[Provider],
) -> None:
    """Providers should have unique identities."""

    names = [
        provider.name
        for provider in providers
    ]

    assert len(names) == len(set(names))