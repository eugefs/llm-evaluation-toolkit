"""Command line interface."""

from pathlib import Path
from typing import Annotated

import typer

from llm_evaluation_toolkit.plugins import (
    PluginLoader,
    PluginRegistry,
)

from llm_evaluation_toolkit.benchmarks import (
    BenchmarkLoader,
    BenchmarkRegistry,
    BenchmarkSchema,
)
from datetime import datetime

from llm_evaluation_toolkit.experiments import (
    ExperimentComparator,
    ExperimentStorage,
    HistoryStorage,
    RunRecord,
)

from .main import run_benchmark
from .output import OutputFormatter


app = typer.Typer(
    name="llm-eval",
    help="LLM Evaluation Toolkit",
)


@app.command()
def run(
    benchmark: str,
    output: str = "results",
    profile: str | None = None,
    format: str = "table",
) -> None:
    """Run benchmark."""

    try:
        run_benchmark(
            benchmark_path=benchmark,
            output=output,
            profile=profile,
        )

        history = HistoryStorage(
            f"{output}/history.json",
        )

        history.add(
            RunRecord(
                name=benchmark,
                created_at=datetime.now(),
                status="completed",
                output=output,
            ),
        )

        if format == "json":
            OutputFormatter.json(
                {
                    "benchmark": benchmark,
                    "status": "completed",
                },
            )
        else:
            OutputFormatter.message(
                "Benchmark completed",
            )

    except Exception as exc:
        typer.echo(
            f"Error: {exc}",
        )
        raise typer.Exit(
            code=1,
        )

@app.command()
def validate(
    benchmark: str,
) -> None:
    """Validate benchmark file."""

    try:
        BenchmarkLoader().load(
            benchmark,
        )

        OutputFormatter.message(
            "Benchmark is valid",
        )

    except Exception as exc:
        typer.echo(
            f"Error: {exc}",
        )
        raise typer.Exit(
            code=1,
        )


@app.command()
def schema(
    output: str = "benchmark-schema.json",
) -> None:
    """Generate benchmark JSON schema."""

    path = BenchmarkSchema.save(
        output,
    )

    OutputFormatter.message(
        f"Schema saved: {path}",
    )


@app.command(name="list")
def list_command(
    directory: str = "examples",
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            help="Output JSON format.",
        ),
    ] = False,
) -> None:
    """List available benchmarks."""

    registry = BenchmarkRegistry(
        directory,
    )

    benchmarks = [
        str(path)
        for path in registry.list()
    ]

    if json_output:
        OutputFormatter.json(
            {
                "benchmarks": benchmarks,
            },
        )
        return

    if not benchmarks:
        OutputFormatter.message(
            "No benchmarks found",
        )
        return

    OutputFormatter.message(
        "Available benchmarks:",
    )

    for benchmark in benchmarks:
        OutputFormatter.message(
            f"- {benchmark}",
        )


@app.command()
def info(
    benchmark: str,
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            help="Output JSON format.",
        ),
    ] = False,
) -> None:
    """Show benchmark metadata."""

    loaded = BenchmarkLoader().load(
        benchmark,
    )

    data = {
        "name": loaded.name,
        "version": loaded.version,
        "description": loaded.description,
        "author": (
            loaded.metadata.author
            if loaded.metadata
            else None
        ),
        "tags": (
            loaded.metadata.tags
            if loaded.metadata
            else []
        ),
    }

    if json_output:
        OutputFormatter.json(
            data,
        )
        return

    OutputFormatter.table(
        "Benchmark Info",
        [
            (
                "Name",
                loaded.name,
            ),
            (
                "Version",
                loaded.version,
            ),
        ],
    )


@app.command()
def history(
    path: str = "results/history.json",
) -> None:
    """Show experiment history."""

    storage = HistoryStorage(
        path,
    )

    records = storage.list()

    if not records:
        OutputFormatter.message(
            "No runs found",
        )
        return

    OutputFormatter.message(
        "Run History",
    )

    for record in records:
        OutputFormatter.message(
            (
                f"{record.name} | "
                f"{record.created_at} | "
                f"{record.status}"
            ),
        )
@app.command()
def plugins() -> None:
    """List installed plugins."""

    PluginLoader.discover()

    available = PluginRegistry.available()

    if not available:
        OutputFormatter.message(
            "No plugins installed",
        )
        return

    OutputFormatter.message(
        "Installed plugins:",
    )

    for plugin in available:
        OutputFormatter.message(
            f"- {plugin}",
        )