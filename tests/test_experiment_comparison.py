"""Experiment comparison tests."""

from llm_evaluation_toolkit.evaluation import (
    EvaluationReport,
    EvaluationResult,
)
from llm_evaluation_toolkit.experiments import (
    ExperimentComparison,
    ExperimentResult,
)
from llm_evaluation_toolkit.generation import (
    GenerationResponse,
)


def build_report(
    score: float,
) -> EvaluationReport:
    """Create report with score."""

    return EvaluationReport(
        results=[
            EvaluationResult(
                case_id="1",
                response=GenerationResponse(
                    content="test",
                    model="test-model",
                ),
                score=score,
                passed=score >= 1.0,
            ),
        ],
    )


def test_experiment_comparison_ranking() -> None:
    """Rank providers by average score."""

    results = {
        "openai": ExperimentResult(
            name="openai-run",
            reports={
                "evaluation": build_report(0.9),
            },
        ),
        "anthropic": ExperimentResult(
            name="anthropic-run",
            reports={
                "evaluation": build_report(0.8),
            },
        ),
    }

    comparison = ExperimentComparison.from_results(
        results,
    )

    assert len(comparison.ranking) == 2
    assert comparison.ranking[0].provider == "openai"
    assert comparison.ranking[1].provider == "anthropic"