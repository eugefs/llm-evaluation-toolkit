"""Token usage metric."""

from llm_evaluation_toolkit.evaluation.models import (
    EvaluationCase,
)
from llm_evaluation_toolkit.generation import (
    GenerationResponse,
)


class TokenUsageMetric:
    """Measure token efficiency."""

    @property
    def name(self) -> str:
        """Return metric name."""
        return "token_usage"

    def score(
        self,
        case: EvaluationCase,
        response: GenerationResponse,
    ) -> float:
        """Return normalized token score."""

        usage = response.usage

        if usage is None:
            return 0.0

        if usage.total_tokens <= 100:
            return 1.0

        if usage.total_tokens >= 1000:
            return 0.0

        return max(
            0.0,
            1.0
            - (
                (usage.total_tokens - 100)
                / 900
            ),
        )