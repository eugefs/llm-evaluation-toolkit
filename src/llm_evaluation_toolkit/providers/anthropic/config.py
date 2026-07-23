"""Configuration models for the Anthropic provider."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AnthropicProviderConfig(BaseModel):
    """Configuration for the Anthropic provider."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    provider: Literal["anthropic"] = "anthropic"
    api_key: str = Field(min_length=1)
    model: str

    base_url: str | None = None
    timeout: float = 60.0
    max_retries: int = 2

    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1024, gt=0)

    default_headers: dict[str, str] = Field(default_factory=dict)
