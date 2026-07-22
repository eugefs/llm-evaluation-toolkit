"""Metric abstractions."""

from abc import ABC, abstractmethod
from typing import Any


class Metric(ABC):
    """Base evaluation metric."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return metric name."""
        ...

    @abstractmethod
    def compute(
        self,
        data: dict[str, Any],
    ) -> float:
        """Compute metric value."""
        ...