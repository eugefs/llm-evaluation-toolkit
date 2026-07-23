"""Benchmark schema generation."""

import json
from pathlib import Path

from .models import Benchmark


class BenchmarkSchema:
    """Generate JSON schema for benchmarks."""

    @staticmethod
    def generate() -> dict[str, object]:
        """Return benchmark JSON schema."""

        return Benchmark.model_json_schema()

    @staticmethod
    def save(
        path: str | Path,
    ) -> Path:
        """Save schema to JSON file."""

        output = Path(path)

        output.write_text(
            json.dumps(
                BenchmarkSchema.generate(),
                indent=2,
            ),
            encoding="utf-8",
        )

        return output