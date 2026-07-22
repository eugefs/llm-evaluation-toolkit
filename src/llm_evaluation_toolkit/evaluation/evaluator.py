"""Evaluation engine."""

from llm_evaluation_toolkit.evaluation import (
    EvaluationCase,
    EvaluationResult,
)
from llm_evaluation_toolkit.evaluation.metrics import Metric
from llm_evaluation_toolkit.providers import Generator


class Evaluator:
    """Runs evaluation cases against a generator using a metric."""

    def __init__(
        self,
        generator: Generator,
        metric: Metric,
    ) -> None:
        self._generator = generator
        self._metric = metric

    def evaluate(
        self,
        case: EvaluationCase,
    ) -> EvaluationResult:
        """Evaluate a single case."""

        response = self._generator.generate(case.request)
        score = self._metric.score(case, response)

        return EvaluationResult(
            case_id=case.id,
            response=response,
            score=score,
            passed=score >= 1.0,
        )