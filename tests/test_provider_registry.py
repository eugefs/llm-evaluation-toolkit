"""Provider registry tests."""

from llm_evaluation_toolkit.providers import (
    ProviderRegistry,
)


def test_default_providers_are_registered() -> None:
    """Default providers should be available."""

    providers = ProviderRegistry.available()

    assert "openai" in providers
    assert "anthropic" in providers
    assert "google" in providers
    assert "xai" in providers


def test_unknown_provider_raises_error() -> None:
    """Unknown providers should fail."""

    try:
        ProviderRegistry.create(
            "unknown",
            None,
        )
    except ValueError as exc:
        assert "Unknown provider" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError"
        )