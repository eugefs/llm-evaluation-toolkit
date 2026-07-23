"""Environment variable resolver."""

import os
import re


_ENV_PATTERN = re.compile(
    r"\$\{([^}]+)\}",
)


class EnvironmentResolver:
    """Resolve environment variables in strings."""

    @staticmethod
    def resolve(
        value: str,
    ) -> str:
        """Replace environment placeholders."""

        def replace(
            match: re.Match[str],
        ) -> str:
            name = match.group(1)

            result = os.getenv(
                name,
            )

            if result is None:
                raise ValueError(
                    f"Missing environment variable: {name}",
                )

            return result

        return _ENV_PATTERN.sub(
            replace,
            value,
        )