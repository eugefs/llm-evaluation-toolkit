"""Run models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RunMetadata(BaseModel):
    """Metadata for an evaluation run."""

    model_config = ConfigDict(
        frozen=True,
    )

    run_id: str
    created_at: datetime

    provider: str
    model: str

    temperature: float
    max_tokens: int


class RunRequest(BaseModel):
    """Stored generation request."""

    prompt: str


class RunResponse(BaseModel):
    """Stored generation response."""

    content: str
    finish_reason: str | None = None
    total_tokens: int | None = None