import pytest

from sae.analytics.delay.result import DelayResult
from sae.kernel.foundation import Number


def build_delays() -> dict[Number, int | None]:
    return {
        Number(1): 0,
        Number(2): 1,
        Number(3): 4,
        Number(4): None,
    }


def test_create_delay_result() -> None:
    delays = build_delays()

    result = DelayResult(
        draw_count=5,
        delays=delays,
    )

    assert result.draw_count == 5
    assert result.delay(Number(1)) == 0
    assert result.delay(Number(2)) == 1
    assert result.delay(Number(3)) == 4
    assert result.delay(Number(4)) is None


def test_delays_are_exposed_as_immutable_mapping() -> None:
    result = DelayResult(
        draw_count=5,
        delays=build_delays(),
    )

    assert result.delays[Number(1)] == 0

    with pytest.raises(TypeError):
        result.delays[Number(1)] = 99  # type: ignore[index]


def test_delay_result_is_immutable() -> None:
    result = DelayResult(
        draw_count=5,
        delays=build_delays(),
    )

    with pytest.raises(AttributeError):
        result.draw_count = 10  # type: ignore[misc]


def test_delay_of_missing_number_is_none() -> None:
    result = DelayResult(
        draw_count=5,
        delays=build_delays(),
    )

    assert result.delay(Number(90)) is None


def test_delays_are_keyed_by_number() -> None:
    result = DelayResult(
        draw_count=5,
        delays=build_delays(),
    )

    assert all(isinstance(number, Number) for number in result.delays)


def test_delays_are_read_only_from_result() -> None:
    delays = build_delays()

    result = DelayResult(
        draw_count=5,
        delays=delays,
    )

    delays[Number(1)] = 999

    assert result.delay(Number(1)) == 0


def test_zero_draw_count_is_valid() -> None:
    result = DelayResult(
        draw_count=0,
        delays={},
    )

    assert result.draw_count == 0
    assert result.delay(Number(1)) is None
