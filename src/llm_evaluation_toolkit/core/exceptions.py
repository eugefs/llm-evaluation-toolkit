"""Toolkit exception hierarchy."""


class LLMEvaluationError(Exception):
    """Base exception for all toolkit errors."""


class ConfigurationError(LLMEvaluationError):
    """Raised when configuration is invalid."""


class ProviderError(LLMEvaluationError):
    """Raised when a provider operation fails."""


class GenerationError(ProviderError):
    """Raised when a generation request fails."""


class EvaluationError(LLMEvaluationError):
    """Raised when evaluation execution fails."""


class MetricError(LLMEvaluationError):
    """Raised when metric execution fails."""


class ReportingError(LLMEvaluationError):
    """Raised when report generation fails."""
