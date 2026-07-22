from llm_evaluation_toolkit.providers.openai.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ConnectionError,
    InvalidResponseError,
    ProviderError,
    RateLimitError,
    TimeoutError,
)


def test_provider_error_inheritance() -> None:
    error = ProviderError("provider failure")

    assert isinstance(error, Exception)
    assert str(error) == "provider failure"


def test_authentication_error_inheritance() -> None:
    assert isinstance(AuthenticationError(), ProviderError)


def test_rate_limit_error_inheritance() -> None:
    assert isinstance(RateLimitError(), ProviderError)


def test_connection_error_inheritance() -> None:
    assert isinstance(ConnectionError(), ProviderError)


def test_timeout_error_inheritance() -> None:
    assert isinstance(TimeoutError(), ProviderError)


def test_invalid_response_error_inheritance() -> None:
    assert isinstance(InvalidResponseError(), ProviderError)


def test_configuration_error_inheritance() -> None:
    assert isinstance(ConfigurationError(), ProviderError)
