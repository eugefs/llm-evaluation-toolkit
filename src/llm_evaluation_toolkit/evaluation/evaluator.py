"""Evaluation engine."""

import asyncio

from llm_evaluation_toolkit.evaluation.datasets import EvaluationDataset
from llm_evaluation_toolkit.evaluation.metric_result import (
    MetricResult,
)
from llm_evaluation_toolkit.evaluation.models import (
    EvaluationCase,
    EvaluationResult,
)
from llm_evaluation_toolkit.evaluation.protocols import Metric
from llm_evaluation_toolkit.providers import (
    AsyncGenerator,
    Generator,
)


class Evaluator:
    """Runs evaluation cases and datasets against a generator."""

    def __init__(
        self,
        generator: Generator,
        metric: Metric | None = None,
        metrics: list[Metric] | None = None,
    ) -> None:
        """Initialize evaluator."""

        self._generator = generator

        if metrics is not None:
            self._metrics = metrics
        elif metric is not None:
            self._metrics = [metric]
        else:
            raise ValueError(
                "At least one metric is required",
            )

    def evaluate(
        self,
        case: EvaluationCase,
    ) -> EvaluationResult:
        """Evaluate a single case."""

        response = self._generator.generate(
            case.request,
        )

        scores = [
            metric.score(
                case,
                response,
            )
            for metric in self._metrics
        ]

        score = sum(scores) / len(scores)

        return EvaluationResult(
            case_id=case.id,
            response=response,
            score=score,
            passed=score >= 1.0,
        )

    def evaluate_metrics(
        self,
        case: EvaluationCase,
    ) -> list[MetricResult]:
        """Return individual metric results."""

        response = self._generator.generate(
            case.request,
        )

        return [
            MetricResult(
                name=metric.name,
                score=metric.score(
                    case,
                    response,
                ),
            )
            for metric in self._metrics
        ]

    def evaluate_dataset(
        self,
        dataset: EvaluationDataset,
    ) -> list[EvaluationResult]:
        """Evaluate every case in a dataset."""

        return [
            self.evaluate(case)
            for case in dataset.cases
        ]

    async def evaluate_async(
        self,
        case: EvaluationCase,
    ) -> EvaluationResult:
        """Evaluate a single case asynchronously."""

        if isinstance(self._generator, AsyncGenerator):
            response = await self._generator.generate_async(
                case.request,
            )
        else:
            response = await asyncio.to_thread(
                self._generator.generate,
                case.request,
            )

        scores = [
            metric.score(
                case,
                response,
            )
            for metric in self._metrics
        ]

        score = sum(scores) / len(scores)

        return EvaluationResult(
            case_id=case.id,
            response=response,
            score=score,
            passed=score >= 1.0,
        )

    async def evaluate_dataset_async(
        self,
        dataset: EvaluationDataset,
    ) -> list[EvaluationResult]:
        """Evaluate every case asynchronously."""

        tasks = [
            self.evaluate_async(case)
            for case in dataset.cases
        ]

        return await asyncio.gather(*tasks)