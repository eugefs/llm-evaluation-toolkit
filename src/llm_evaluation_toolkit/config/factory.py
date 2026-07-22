"""Provider factory from configuration."""

from typing import Any

from llm_evaluation_toolkit.providers import Provider, ProviderRegistry
from llm_evaluation_toolkit.providers.anthropic import (
    AnthropicProviderConfig,
)
from llm_evaluation_toolkit.providers.google import (
    GoogleProviderConfig,
)
from llm_evaluation_toolkit.providers.openai import (
    OpenAIProviderConfig,
)
from llm_evaluation_toolkit.providers.xai import (
    XAIProviderConfig,
)

from .loader import load_config
from .models import ProviderRunConfig


ProviderConfig = (
    OpenAIProviderConfig
    | AnthropicProviderConfig
    | GoogleProviderConfig
    | XAIProviderConfig
)


def _build_provider_config(
    config: ProviderRunConfig,
) -> ProviderConfig:
    """Convert runtime config to provider config."""

    common: dict[str, Any] = {
        "api_key": config.api_key,
        "model": config.model.name,
        "temperature": config.model.temperature,
        "max_tokens": config.model.max_tokens,
    }

    match config.provider:
        case "openai":
            return OpenAIProviderConfig(
                **common,
            )

        case "anthropic":
            return AnthropicProviderConfig(
                **common,
            )

        case "google":
            return GoogleProviderConfig(
                **common,
            )

        case "xai":
            return XAIProviderConfig(
                **common,
            )

        case _:
            raise ValueError(
                f"Unsupported provider: {config.provider}"
            )


def create_provider_from_config(
    path: str,
) -> Provider:
    """Create provider from YAML configuration."""

    runtime_config = load_config(path)

    provider_config = _build_provider_config(
        runtime_config,
    )

    return ProviderRegistry.create(
        runtime_config.provider,
        provider_config,
    )