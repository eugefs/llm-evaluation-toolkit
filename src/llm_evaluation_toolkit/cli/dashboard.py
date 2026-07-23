"""Dashboard helpers."""

from llm_evaluation_toolkit.experiments import (
    HistoryStorage,
)


class Dashboard:
    """Generate evaluation dashboard information."""

    def __init__(
        self,
        history_path: str = "results/history.json",
    ) -> None:
        """Initialize dashboard."""

        self._storage = HistoryStorage(
            history_path,
        )

    def summary(
        self,
    ) -> dict[str, object]:
        """Generate summary."""

        runs = self._storage.list()

        completed = [
            run
            for run in runs
            if run.status == "completed"
        ]

        failed = [
            run
            for run in runs
            if run.status == "failed"
        ]

        success_rate = (
            len(completed)
            / len(runs)
            * 100
            if runs
            else 0.0
        )

        return {
            "total_runs": len(runs),
            "completed": len(completed),
            "failed": len(failed),
            "success_rate": round(
                success_rate,
                2,
            ),
        }