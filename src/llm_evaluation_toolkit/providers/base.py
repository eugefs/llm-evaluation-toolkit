"""Provider base interfaces."""

from typing import Protocol, runtime_checkable

from llm_evaluation_toolkit.generation.models import (
    GenerationRequest,
    GenerationResponse,
)


@runtime_checkable
class Provider(Protocol):
    """Basic provider contract."""

    @property
    def name(self) -> str:
        """Provider name."""
        ...


@runtime_checkable
class Generator(Provider, Protocol):
    """Text generation provider contract."""

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate response."""
        ...


@runtime_checkable
class AsyncGenerator(Provider, Protocol):
    """Async text generation provider contract."""

    async def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate async response."""
        ...


__all__ = [
    "Provider",
    "Generator",
    "AsyncGenerator",
]