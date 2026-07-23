"""Benchmark metadata models."""

from pydantic import BaseModel, ConfigDict, Field


class BenchmarkMetadata(BaseModel):
    """Additional benchmark information."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    author: str | None = None

    created: str | None = None

    license: str | None = None

    tags: list[str] = Field(
        default_factory=list,
    )