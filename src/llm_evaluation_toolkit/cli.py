"""Command-line interface for llm-evaluation-toolkit."""

from typing import Annotated

import typer

app = typer.Typer(
    help="LLM Evaluation Toolkit",
    no_args_is_help=True,
)


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the toolkit version and exit.",
        ),
    ] = False,
) -> None:
    """LLM Evaluation Toolkit."""
    if version:
        typer.echo("LLM Evaluation Toolkit 0.1.0")
        raise typer.Exit()