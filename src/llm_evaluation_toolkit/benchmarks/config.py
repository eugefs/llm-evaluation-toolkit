"""Benchmark execution configuration."""

from pydantic import BaseModel, ConfigDict, Field


class ProviderConfig(BaseModel):
    """Provider execution configuration."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    model: str | None = None

    temperature: float | None = None


class ExecutionConfig(BaseModel):
    """Benchmark execution options."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    timeout: float = 60.0

    retries: int = 0

    concurrency: int = 1


class BenchmarkConfig(BaseModel):
    """Full benchmark configuration."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    providers: list[ProviderConfig] = Field(
        default_factory=list,
    )

    execution: ExecutionConfig = Field(
        default_factory=ExecutionConfig,
    )