from llm_evaluation_toolkit.providers.openai.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
)


def test_chat_message() -> None:
    message = ChatMessage(
        role="user",
        content="Hello",
    )

    assert message.role == "user"
    assert message.content == "Hello"


def test_chat_request() -> None:
    request = ChatRequest(
        messages=[
            ChatMessage(
                role="user",
                content="Hello",
            )
        ]
    )

    assert len(request.messages) == 1
    assert request.messages[0].content == "Hello"


def test_chat_response() -> None:
    response = ChatResponse(
        content="Hi",
        model="gpt-test",
        finish_reason="stop",
        usage={
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
        },
    )

    assert response.content == "Hi"
    assert response.model == "gpt-test"
    assert response.finish_reason == "stop"
    assert response.usage is not None
    assert response.usage["total_tokens"] == 15
