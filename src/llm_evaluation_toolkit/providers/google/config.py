"""Configuration models for the Google provider."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class GoogleProviderConfig(BaseModel):
    """Configuration for the Google provider."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
    )

    provider: Literal["google"] = "google"
    api_key: str = Field(min_length=1)
    model: str

    base_url: str | None = None
    timeout: float = 60.0

    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, gt=0)