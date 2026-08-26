import pytest

from sae.analytics.probability.result import ProbabilityResult
from sae.kernel.foundation import Number


def build_probabilities() -> dict[Number, float]:
    return {
        Number(1): 1.0,
        Number(2): 0.5,
        Number(3): 0.0,
    }


def test_create_probability_result() -> None:
    probabilities = build_probabilities()

    result = ProbabilityResult(
        draw_count=2,
        probabilities=probabilities,
    )

    assert result.draw_count == 2
    assert result.probability(Number(1)) == 1.0
    assert result.probability(Number(2)) == 0.5
    assert result.probability(Number(3)) == 0.0


def test_probabilities_are_exposed_as_immutable_mapping() -> None:
    result = ProbabilityResult(
        draw_count=2,
        probabilities=build_probabilities(),
    )

    assert result.probabilities[Number(1)] == 1.0

    with pytest.raises(TypeError):
        result.probabilities[Number(1)] = 0.25  # type: ignore[index]


def test_probability_result_is_immutable() -> None:
    result = ProbabilityResult(
        draw_count=2,
        probabilities=build_probabilities(),
    )

    with pytest.raises(AttributeError):
        result.draw_count = 10  # type: ignore[misc]


def test_probability_of_missing_number_is_zero() -> None:
    result = ProbabilityResult(
        draw_count=2,
        probabilities=build_probabilities(),
    )

    assert result.probability(Number(90)) == 0.0


def test_probabilities_are_keyed_by_number() -> None:
    result = ProbabilityResult(
        draw_count=2,
        probabilities=build_probabilities(),
    )

    assert all(isinstance(number, Number) for number in result.probabilities)


def test_probabilities_are_read_only_from_result() -> None:
    probabilities = build_probabilities()

    result = ProbabilityResult(
        draw_count=2,
        probabilities=probabilities,
    )

    probabilities[Number(1)] = 0.25

    assert result.probability(Number(1)) == 1.0


def test_zero_draw_count_is_valid() -> None:
    result = ProbabilityResult(
        draw_count=0,
        probabilities={},
    )

    assert result.draw_count == 0
    assert result.probability(Number(1)) == 0.0
