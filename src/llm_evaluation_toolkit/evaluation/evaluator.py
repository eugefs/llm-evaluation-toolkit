"""Evaluation engine."""

from llm_evaluation_toolkit.evaluation.datasets import EvaluationDataset
from llm_evaluation_toolkit.evaluation.models import (
    EvaluationCase,
    EvaluationResult,
)
from llm_evaluation_toolkit.evaluation.protocols import Metric
from llm_evaluation_toolkit.providers import Generator


class Evaluator:
    """Runs evaluation cases and datasets against a generator."""

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

    def evaluate_dataset(
        self,
        dataset: EvaluationDataset,
    ) -> list[EvaluationResult]:
        """Evaluate every case in a dataset."""

        return [self.evaluate(case) for case in dataset.cases]
