"""Evaluation metrics tests."""

from llm_evaluation_toolkit.evaluation.metrics import (
    LatencyMetric,
    TokenUsageMetric,
)
from llm_evaluation_toolkit.evaluation.models import (
    EvaluationCase,
)
from llm_evaluation_toolkit.generation import (
    GenerationMessage,
    GenerationRequest,
    GenerationResponse,
    TokenUsage,
)


def build_case() -> EvaluationCase:
    """Create evaluation case."""

    return EvaluationCase(
        id="1",
        request=GenerationRequest(
            messages=[
                GenerationMessage(
                    role="user",
                    content="test",
                )
            ],
        ),
        expected_output="test",
        metadata={
            "latency": "0.5",
        },
    )


def test_latency_metric() -> None:
    """Latency metric returns normalized score."""

    metric = LatencyMetric()

    response = GenerationResponse(
        content="test",
        model="test-model",
    )

    score = metric.score(
        build_case(),
        response,
    )

    assert score == 1.0


def test_token_usage_metric() -> None:
    """Token metric evaluates efficiency."""

    metric = TokenUsageMetric()

    response = GenerationResponse(
        content="test",
        model="test-model",
        usage=TokenUsage(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30,
        ),
    )

    score = metric.score(
        build_case(),
        response,
    )

    assert score == 1.0