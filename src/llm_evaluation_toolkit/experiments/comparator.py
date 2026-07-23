"""Experiment comparator."""

from .comparison_report import (
    ComparisonEntry,
    ComparisonReport,
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

            first_score = len(
                first_reports[name].results,
            )

            second_score = len(
                second_reports[name].results,
            )

            entries.append(
                ComparisonEntry(
                    name=name,
                    first=float(first_score),
                    second=float(second_score),
                    delta=float(
                        second_score - first_score,
                    ),
                ),
            )

        return ComparisonReport(
            entries=entries,
        )