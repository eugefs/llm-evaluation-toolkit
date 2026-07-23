"""Metric result model."""

from pydantic import BaseModel, ConfigDict, Field


class MetricResult(BaseModel):
    """Single metric evaluation result."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    score: float = Field(
        ge=0.0,
        le=1.0,
    )