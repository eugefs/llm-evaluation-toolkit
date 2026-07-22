"""Tests for the evaluation framework."""

from llm_evaluation_toolkit.evaluation import (
    EvaluationCase,
    EvaluationResult,
    Evaluator,
    ExactMatchMetric,
)
from llm_evaluation_toolkit.generation import (
    GenerationMessage,
    GenerationRequest,
    GenerationResponse,
    TokenUsage,
)
from llm_evaluation_toolkit.providers import Generator


class FakeGenerator(Generator):
    """Simple generator used for evaluation tests."""

    def __init__(self, response: GenerationResponse) -> None:
        self._response = response

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        return self._response


def make_request() -> GenerationRequest:
    """Create a simple generation request."""
    return GenerationRequest(
        messages=[
            GenerationMessage(
                role="user",
                content="Hello!",
            )
        ]
    )


def make_response(content: str) -> GenerationResponse:
    """Create a generation response."""
    return GenerationResponse(
        content=content,
        finish_reason="stop",
        model="test-model",
        usage=TokenUsage(
            prompt_tokens=1,
            completion_tokens=1,
            total_tokens=2,
        ),
    )


def test_exact_match_metric_match() -> None:
    metric = ExactMatchMetric()

    case = EvaluationCase(
        id="case-1",
        request=make_request(),
        expected_output="Hello!",
    )

    score = metric.score(
        case,
        make_response("Hello!"),
    )

    assert metric.name == "exact_match"
    assert score == 1.0


def test_exact_match_metric_mismatch() -> None:
    metric = ExactMatchMetric()

    case = EvaluationCase(
        id="case-1",
        request=make_request(),
        expected_output="Hello!",
    )

    score = metric.score(
        case,
        make_response("Goodbye!"),
    )

    assert score == 0.0


def test_evaluator_returns_result() -> None:
    response = make_response("Hello!")

    evaluator = Evaluator(
        generator=FakeGenerator(response),
        metric=ExactMatchMetric(),
    )

    case = EvaluationCase(
        id="case-1",
        request=make_request(),
        expected_output="Hello!",
    )

    result = evaluator.evaluate(case)

    assert isinstance(result, EvaluationResult)
    assert result.case_id == "case-1"
    assert result.response is response
    assert result.score == 1.0
    assert result.passed is True


def test_evaluator_failed_result() -> None:
    response = make_response("Wrong answer")

    evaluator = Evaluator(
        generator=FakeGenerator(response),
        metric=ExactMatchMetric(),
    )

    case = EvaluationCase(
        id="case-1",
        request=make_request(),
        expected_output="Hello!",
    )

    result = evaluator.evaluate(case)

    assert result.score == 0.0
    assert result.passed is False