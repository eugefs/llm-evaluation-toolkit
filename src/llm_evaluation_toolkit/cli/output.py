"""CLI output formatting."""

import json
from typing import Any

from rich.console import Console
from rich.table import Table


console = Console()


class OutputFormatter:
    """Format CLI output."""

    @staticmethod
    def json(
        data: Any,
    ) -> None:
        """Print JSON output."""

        console.print(
            json.dumps(
                data,
                indent=2,
                default=str,
            ),
        )

    @staticmethod
    def table(
        title: str,
        rows: list[tuple[str, str]],
    ) -> None:
        """Print table output."""

        table = Table(
            title=title,
        )

        table.add_column(
            "Name",
        )

        table.add_column(
            "Value",
        )

        for name, value in rows:
            table.add_row(
                name,
                value,
            )

        console.print(
            table,
        )

    @staticmethod
    def message(
        text: str,
    ) -> None:
        """Print plain message."""

        console.print(
            text,
        )