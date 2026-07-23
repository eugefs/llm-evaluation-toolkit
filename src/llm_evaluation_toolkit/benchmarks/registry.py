"""Benchmark registry."""

from pathlib import Path


class BenchmarkRegistry:
    """Discover benchmark files."""

    def __init__(
        self,
        directory: str | Path,
    ) -> None:
        """Initialize registry."""

        self._directory = Path(directory)

    def list(self) -> list[Path]:
        """Return available benchmarks."""

        if not self._directory.exists():
            return []

        return sorted(
            [
                *self._directory.glob("*.yaml"),
                *self._directory.glob("*.yml"),
                *self._directory.glob("*.json"),
            ],
        )