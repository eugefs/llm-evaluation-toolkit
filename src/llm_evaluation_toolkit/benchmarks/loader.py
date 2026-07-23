"""Benchmark loader."""

import json
from pathlib import Path
from typing import Any

import yaml

from .env import EnvironmentResolver
from .models import Benchmark


class BenchmarkLoader:
    """Load benchmark definitions."""

    def load(
        self,
        path: str | Path,
    ) -> Benchmark:
        """Load benchmark definition."""

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(
                file_path,
            )

        content = file_path.read_text(
            encoding="utf-8",
        )

        if file_path.suffix in {
            ".yaml",
            ".yml",
        }:
            data = yaml.safe_load(
                content,
            )
        elif file_path.suffix == ".json":
            data = json.loads(
                content,
            )
        else:
            raise ValueError(
                f"Unsupported format: {file_path.suffix}",
            )

        resolved = self._resolve_values(
            data,
        )

        return Benchmark.model_validate(
            resolved,
        )

    def _resolve_values(
        self,
        value: Any,
    ) -> Any:
        """Resolve environment variables recursively."""

        if isinstance(value, dict):
            return {
                key: self._resolve_values(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                self._resolve_values(item)
                for item in value
            ]

        if isinstance(value, str):
            return EnvironmentResolver.resolve(
                value,
            )

        return value