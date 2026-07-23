"""Command line interface."""

from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from llm_evaluation_toolkit.benchmarks import (
    BenchmarkLoader,
    BenchmarkRegistry,
    BenchmarkSchema,
)

from llm_evaluation_toolkit.experiments import (
    ExperimentComparator,
    ExperimentStorage,
    HistoryStorage,
    RunRecord,
)

from llm_evaluation_toolkit.plugins import (
    PluginLoader,
    PluginRegistry,
)

from .dashboard import Dashboard
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


@app.command()
def compare(
    first: str,
    second: str,
    directory: str = "results",
) -> None:
    """Compare two experiment results."""

    try:
        storage = ExperimentStorage(
            Path(directory),
        )

        first_result = storage.load(
            first,
        )

        second_result = storage.load(
            second,
        )

        report = ExperimentComparator().compare(
            first_result,
            second_result,
        )

    except FileNotFoundError as exc:
        OutputFormatter.message(
            f"Experiment not found: {exc.filename}",
        )

        OutputFormatter.message(
            "Available results:",
        )

        result_path = Path(directory)

        if result_path.exists():
            for item in result_path.glob("*.json"):
                OutputFormatter.message(
                    f"- {item.stem}",
                )

        raise typer.Exit(
            code=1,
        )

    OutputFormatter.message(
        "Comparison Report",
    )

    for entry in report.entries:
        OutputFormatter.message(
            (
                f"{entry.name}: "
                f"{entry.delta:+}"
            ),
        )

    OutputFormatter.message(
        (
            f"Latency: "
            f"{report.latency_delta:+.2f} ms"
        ),
    )

    OutputFormatter.message(
        (
            f"Cost: "
            f"{report.cost_delta:+.6f}"
        ),
    )

    OutputFormatter.message(
        (
            f"Tokens: "
            f"{report.token_delta:+d}"
        ),
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


@app.command()
def dashboard() -> None:
    """Show evaluation dashboard."""

    data = Dashboard().summary()

    OutputFormatter.message(
        "Evaluation Dashboard",
    )

    OutputFormatter.message(
        f"Runs: {data['total_runs']}",
    )

    OutputFormatter.message(
        f"Completed: {data['completed']}",
    )

    OutputFormatter.message(
        f"Failed: {data['failed']}",
    )

    OutputFormatter.message(
        f"Success Rate: {data['success_rate']}%",
    )