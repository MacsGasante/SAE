import pytest

from sae.analytics.frequency.result import FrequencyResult
from sae.kernel.foundation import Number


def build_frequencies() -> dict[Number, int]:
    return {
        Number(1): 3,
        Number(2): 1,
        Number(3): 0,
    }


def test_create_frequency_result() -> None:
    frequencies = build_frequencies()

    result = FrequencyResult(
        draw_count=2,
        frequencies=frequencies,
    )

    assert result.draw_count == 2
    assert result.frequency(Number(1)) == 3
    assert result.frequency(Number(2)) == 1
    assert result.frequency(Number(3)) == 0


def test_frequencies_are_exposed_as_immutable_mapping() -> None:
    result = FrequencyResult(
        draw_count=2,
        frequencies=build_frequencies(),
    )

    assert result.frequencies[Number(1)] == 3

    with pytest.raises(TypeError):
        result.frequencies[Number(1)] = 99  # type: ignore[index]


def test_frequency_result_is_immutable() -> None:
    result = FrequencyResult(
        draw_count=2,
        frequencies=build_frequencies(),
    )

    with pytest.raises(AttributeError):
        result.draw_count = 10  # type: ignore[misc]


def test_frequency_of_missing_number_is_zero() -> None:
    result = FrequencyResult(
        draw_count=2,
        frequencies=build_frequencies(),
    )

    assert result.frequency(Number(90)) == 0


def test_frequencies_are_keyed_by_number() -> None:
    result = FrequencyResult(
        draw_count=2,
        frequencies=build_frequencies(),
    )

    assert all(isinstance(number, Number) for number in result.frequencies)


def test_frequencies_are_read_only_from_result() -> None:
    frequencies = build_frequencies()

    result = FrequencyResult(
        draw_count=2,
        frequencies=frequencies,
    )

    frequencies[Number(1)] = 999

    assert result.frequency(Number(1)) == 3


def test_zero_draw_count_is_valid() -> None:
    result = FrequencyResult(
        draw_count=0,
        frequencies={},
    )

    assert result.draw_count == 0
    assert result.frequency(Number(1)) == 0
