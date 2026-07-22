"""Asynchronous generation protocol."""

from typing import Protocol, runtime_checkable

from llm_evaluation_toolkit.generation import (
    GenerationRequest,
    GenerationResponse,
)


@runtime_checkable
class AsyncGenerator(Protocol):
    """Protocol for asynchronous text generation."""

    async def generate_async(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate a response asynchronously."""
        ...