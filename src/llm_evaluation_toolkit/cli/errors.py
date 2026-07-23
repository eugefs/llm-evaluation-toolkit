"""CLI error handling."""

from pathlib import Path

import typer


def handle_error(
    error: Exception,
) -> None:
    """Handle CLI errors."""

    if isinstance(
        error,
        FileNotFoundError,
    ):
        typer.echo(
            f"Error: File not found: {error}",
        )
        raise typer.Exit(
            code=1,
        )

    if isinstance(
        error,
        ValueError,
    ):
        typer.echo(
            f"Error: {error}",
        )
        raise typer.Exit(
            code=1,
        )

    typer.echo(
        "Error: Unexpected failure",
    )

    raise typer.Exit(
        code=1,
    )