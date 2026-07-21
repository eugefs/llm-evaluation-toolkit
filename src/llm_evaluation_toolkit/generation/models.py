"""Provider-agnostic generation models."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class GenerationMessage(BaseModel):
    """A single message in a generation request."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    role: Literal["system", "user", "assistant", "tool"]
    content: str


class TokenUsage(BaseModel):
    """Token usage reported by a provider."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class GenerationRequest(BaseModel):
    """A provider-independent generation request."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    messages: list[GenerationMessage]

    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, gt=0)


class GenerationResponse(BaseModel):
    """A provider-independent generation response."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    content: str
    finish_reason: str | None = None
    model: str
    usage: TokenUsage | None = None