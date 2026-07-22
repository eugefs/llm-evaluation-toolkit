from llm_evaluation_toolkit.evaluation import (
    EvaluationCase,
    EvaluationDataset,
    EvaluationResult,
    Evaluator,
    ExactMatchMetric,
)
from llm_evaluation_toolkit.generation import (
    GenerationMessage,
    GenerationRequest,
    GenerationResponse,
)
from llm_evaluation_toolkit.providers import Generator


class FakeGenerator(Generator):
    def __init__(self, response: GenerationResponse) -> None:
        self._response = response

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        return self._response


def make_request(prompt: str) -> GenerationRequest:
    return GenerationRequest(
        messages=[
            GenerationMessage(
                role="user",
                content=prompt,
            )
        ]
    )


def make_response(content: str) -> GenerationResponse:
    return GenerationResponse(
        content=content,
        model="fake-model",
    )


def make_case(
    case_id: str,
    prompt: str,
    expected: str,
) -> EvaluationCase:
    return EvaluationCase(
        id=case_id,
        request=make_request(prompt),
        expected_output=expected,
    )


def test_exact_match_metric_success() -> None:
    metric = ExactMatchMetric()
    case = make_case("1", "Hello", "Paris")
    response = make_response("Paris")

    assert metric.score(case, response) == 1.0


def test_exact_match_metric_failure() -> None:
    metric = ExactMatchMetric()
    case = make_case("1", "Hello", "Paris")
    response = make_response("London")

    assert metric.score(case, response) == 0.0


def test_dataset_size() -> None:
    dataset = EvaluationDataset(
        name="test",
        cases=[
            make_case("1", "A", "1"),
            make_case("2", "B", "2"),
        ],
    )

    assert dataset.size == 2


def test_evaluator_success() -> None:
    evaluator = Evaluator(
        generator=FakeGenerator(make_response("Paris")),
        metric=ExactMatchMetric(),
    )

    result = evaluator.evaluate(
        make_case(
            "1",
            "Capital of France?",
            "Paris",
        )
    )

    assert isinstance(result, EvaluationResult)
    assert result.case_id == "1"
    assert result.response.content == "Paris"
    assert result.score == 1.0
    assert result.passed is True


def test_evaluator_failure() -> None:
    evaluator = Evaluator(
        generator=FakeGenerator(make_response("London")),
        metric=ExactMatchMetric(),
    )

    result = evaluator.evaluate(
        make_case(
            "1",
            "Capital of France?",
            "Paris",
        )
    )

    assert result.score == 0.0
    assert result.passed is False


def test_evaluate_dataset() -> None:
    dataset = EvaluationDataset(
        name="capitals",
        cases=[
            make_case("1", "Capital of France?", "Paris"),
            make_case("2", "Capital of Germany?", "Paris"),
        ],
    )

    evaluator = Evaluator(
        generator=FakeGenerator(make_response("Paris")),
        metric=ExactMatchMetric(),
    )

    results = evaluator.evaluate_dataset(dataset)

    assert len(results) == 2
    assert all(result.score == 1.0 for result in results)