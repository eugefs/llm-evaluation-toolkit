"""Configuration models for the xAI provider."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class XAIProviderConfig(BaseModel):
    """Configuration for the xAI provider."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    provider: Literal["xai"] = "xai"
    api_key: str = Field(min_length=1)
    model: str

    base_url: str | None = None
    timeout: float = 60.0

    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, gt=0)