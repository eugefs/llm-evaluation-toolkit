"""Data models for the OpenAI-compatible provider."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class ChatMessage(BaseModel):
    """A single chat message."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """A chat completion request."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    """A chat completion response."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    content: str
    finish_reason: str | None = None
    model: str
    usage: dict[str, int] | None = None
