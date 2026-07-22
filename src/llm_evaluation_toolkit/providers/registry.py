"""Provider registry."""

from typing import Any, Protocol

from .base import Provider


class ProviderFactory(Protocol):
    """Protocol for provider constructors."""

    def __call__(
        self,
        config: Any,
    ) -> Provider:
        """Create provider instance."""
        ...


class ProviderRegistry:
    """Registry for provider implementations."""

    _providers: dict[str, ProviderFactory] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider: ProviderFactory,
    ) -> None:
        """Register a provider."""
        cls._providers[name] = provider

    @classmethod
    def create(
        cls,
        name: str,
        config: Any,
    ) -> Provider:
        """Create provider instance."""

        if name not in cls._providers:
            raise ValueError(
                f"Unknown provider: {name}"
            )

        provider_factory = cls._providers[name]

        return provider_factory(config)

    @classmethod
    def available(cls) -> list[str]:
        """Return available providers."""
        return list(cls._providers.keys())


def register_default_providers() -> None:
    """Register built-in providers."""

    from .anthropic import AnthropicProvider
    from .google import GoogleProvider
    from .openai import OpenAICompatibleProvider
    from .xai import XAIProvider

    ProviderRegistry.register(
        "openai",
        OpenAICompatibleProvider,
    )

    ProviderRegistry.register(
        "anthropic",
        AnthropicProvider,
    )

    ProviderRegistry.register(
        "google",
        GoogleProvider,
    )

    ProviderRegistry.register(
        "xai",
        XAIProvider,
    )