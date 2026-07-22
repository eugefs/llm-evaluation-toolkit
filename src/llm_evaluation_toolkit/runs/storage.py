"""Run storage."""

import json
from pathlib import Path

from .models import (
    RunMetadata,
    RunRequest,
    RunResponse,
)


class RunStorage:
    """Persist evaluation runs."""

    def __init__(
        self,
        root: str | Path = "runs",
    ) -> None:
        """Initialize storage."""

        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        metadata: RunMetadata,
        request: RunRequest,
        response: RunResponse,
    ) -> Path:
        """Save a run."""

        run_dir = self.root / metadata.run_id

        run_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        (run_dir / "metadata.json").write_text(
            metadata.model_dump_json(
                indent=2,
            ),
            encoding="utf-8",
        )

        (run_dir / "request.json").write_text(
            request.model_dump_json(
                indent=2,
            ),
            encoding="utf-8",
        )

        (run_dir / "response.json").write_text(
            response.model_dump_json(
                indent=2,
            ),
            encoding="utf-8",
        )

        return run_dir