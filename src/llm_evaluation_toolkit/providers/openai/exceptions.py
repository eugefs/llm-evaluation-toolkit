"""Exception hierarchy for the OpenAI-compatible provider."""


class ProviderError(Exception):
    """Base exception for provider-related errors."""


class AuthenticationError(ProviderError):
    """Authentication with the provider failed."""


class RateLimitError(ProviderError):
    """The provider rate limit was exceeded."""


class ConnectionError(ProviderError):
    """A connection to the provider could not be established."""


class TimeoutError(ProviderError):
    """The request to the provider timed out."""


class InvalidResponseError(ProviderError):
    """The provider returned an invalid or unexpected response."""


class ConfigurationError(ProviderError):
    """The provider configuration is invalid."""
