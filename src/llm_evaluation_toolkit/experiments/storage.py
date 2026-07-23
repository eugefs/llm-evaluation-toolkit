"""Experiment result storage."""

import json
from pathlib import Path

from .result import ExperimentResult


class ExperimentStorage:
    """Persist experiment results as JSON."""

    def __init__(
        self,
        directory: Path,
    ) -> None:
        """Initialize storage."""

        self._directory = directory
        self._directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        result: ExperimentResult,
    ) -> Path:
        """Save experiment result."""

        path = self._directory / (
            f"{result.name}.json"
        )

        path.write_text(
            result.model_dump_json(
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    def load(
        self,
        name: str,
    ) -> ExperimentResult:
        """Load experiment result."""

        path = self._directory / (
            f"{name}.json"
        )

        data = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )

        return ExperimentResult.model_validate(
            data,
        )