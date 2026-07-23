"""Benchmark profiles."""

from pydantic import BaseModel, ConfigDict, Field

from .config import ProviderConfig


class BenchmarkProfile(BaseModel):
    """Named benchmark execution profile."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    providers: list[ProviderConfig] = Field(
        default_factory=list,
    )