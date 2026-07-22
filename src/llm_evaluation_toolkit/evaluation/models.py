"""Provider-independent evaluation models."""

from pydantic import BaseModel, ConfigDict, Field

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
)


class EvaluationCase(BaseModel):
    """A single evaluation example."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    id: str
    request: GenerationRequest
    expected_output: str
    metadata: dict[str, str] = Field(default_factory=dict)


class EvaluationResult(BaseModel):
    """The result of evaluating a single case."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    case_id: str
    response: GenerationResponse
    score: float = Field(ge=0.0, le=1.0)
    passed: bool
    metadata: dict[str, str] = Field(default_factory=dict)
