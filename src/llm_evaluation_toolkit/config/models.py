"""Configuration models."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class ModelConfig(BaseModel):
    """Model generation configuration."""

    model_config = ConfigDict(
        extra="forbid",
    )

    name: str
    temperature: float = 0.0
    max_tokens: int = 1024


class ProviderRunConfig(BaseModel):
    """Runtime provider configuration."""

    model_config = ConfigDict(
        extra="forbid",
    )

    provider: Literal[
        "openai",
        "anthropic",
        "google",
        "xai",
    ]

    api_key: str

    model: ModelConfig

    extra: dict[str, Any] = {}