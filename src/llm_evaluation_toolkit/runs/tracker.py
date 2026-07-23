"""Run tracker."""

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .models import (
    RunMetadata,
    RunRequest,
    RunResponse,
)
from .storage import RunStorage


class RunTracker:
    """Track and persist evaluation runs."""

    def __init__(
        self,
        storage: RunStorage | None = None,
    ) -> None:
        """Initialize tracker."""

        self._storage = storage or RunStorage()

    @property
    def storage(self) -> RunStorage:
        """Return underlying storage."""
        return self._storage

    def record(
        self,
        provider: str,
        model: str,
        temperature: float,
        max_tokens: int,
        prompt: str,
        content: str,
        finish_reason: str | None = None,
        total_tokens: int | None = None,
    ) -> Path:
        """Record an evaluation run."""

        run_id = str(uuid4())

        metadata = RunMetadata(
            run_id=run_id,
            created_at=datetime.now(
                timezone.utc,
            ),
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        request = RunRequest(
            prompt=prompt,
        )

        response = RunResponse(
            content=content,
            finish_reason=finish_reason,
            total_tokens=total_tokens,
        )

        return self._storage.save(
            metadata,
            request,
            response,
        )