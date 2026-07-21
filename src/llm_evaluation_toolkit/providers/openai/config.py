"""Configuration models for the OpenAI-compatible provider."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OpenAIProviderConfig(BaseModel):
    """Configuration for an OpenAI-compatible provider."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    provider: Literal["openai"] = "openai"
    base_url: str = "https://api.openai.com/v1"
    api_key: str
    model: str

    timeout: float = 60.0
    max_retries: int = 3

    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, gt=0)

    organization: str | None = None

    default_headers: dict[str, str] = Field(default_factory=dict)