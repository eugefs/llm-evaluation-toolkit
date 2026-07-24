"""Experiment comparator."""

from .comparison_report import (
    ComparisonEntry,
    ComparisonReport,
    PerformanceDelta,
)
from .result import ExperimentResult


class ExperimentComparator:
    """Compare experiment results."""

    def compare(
        self,
        first: ExperimentResult,
        second: ExperimentResult,
    ) -> ComparisonReport:
        """Create comparison report."""

        entries: list[ComparisonEntry] = []

        first_reports = first.reports
        second_reports = second.reports

        for name in first_reports:
            if name not in second_reports:
                continue

            first_results = first_reports[name].results
            second_results = second_reports[name].results

            first_score = (
                sum(
                    result.score
                    for result in first_results
                )
                / len(first_results)
                if first_results
                else 0.0
            )

            second_score = (
                sum(
                    result.score
                    for result in second_results
                )
                / len(second_results)
                if second_results
                else 0.0
            )

            entries.append(
                ComparisonEntry(
                    name=name,
                    first_score=first_score,
                    second_score=second_score,
                    score_delta=(
                        second_score
                        -
                        first_score
                    ),
                ),
            )

        return ComparisonReport(
            entries=entries,
            performance=PerformanceDelta(),
        )