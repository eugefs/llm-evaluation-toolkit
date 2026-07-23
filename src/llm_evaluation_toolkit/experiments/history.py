"""Experiment run history models."""

import json
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class RunRecord(BaseModel):
    """Single experiment execution record."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        min_length=1,
    )

    created_at: datetime

    status: str = Field(
        min_length=1,
    )

    output: str | None = None


class HistoryStorage:
    """Persist run history."""

    def __init__(
        self,
        path: str = "results/history.json",
    ) -> None:
        """Initialize storage."""

        self._path = Path(path)

    def list(self) -> list[RunRecord]:
        """Return stored runs."""

        if not self._path.exists():
            return []

        data = json.loads(
            self._path.read_text(
                encoding="utf-8",
            ),
        )

        return [
            RunRecord.model_validate(
                item,
            )
            for item in data
        ]

    def add(
        self,
        record: RunRecord,
    ) -> None:
        """Add run record."""

        records = self.list()

        records.append(
            record,
        )

        self._path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._path.write_text(
            json.dumps(
                [
                    item.model_dump(
                        mode="json",
                    )
                    for item in records
                ],
                indent=2,
            ),
            encoding="utf-8",
        )