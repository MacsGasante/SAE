"""
Tests for Draw.matches().
"""

from __future__ import annotations

from sae.kernel.collections import Combination
from sae.kernel.domain import Draw, DrawDate, DrawId
from sae.kernel.foundation import Number


def make_draw(numbers: tuple[int, ...]) -> Draw:
    return Draw(
        id=DrawId(1),
        date=DrawDate.from_ymd(
            2024,
            1,
            1,
        ),
        combination=Combination(*(Number(n) for n in numbers)),
    )


class TestDrawMatches:
    def test_no_matching_numbers(self) -> None:
        draw = make_draw(
            (10, 20, 30, 40, 50, 60),
        )

        result = draw.matches(
            Combination(
                Number(1),
                Number(2),
                Number(3),
                Number(4),
                Number(5),
                Number(6),
            )
        )

        assert result.is_empty
        assert result.count == 0
        assert result.ratio == 0.0

    def test_single_matching_number(self) -> None:
        draw = make_draw(
            (1, 20, 30, 40, 50, 60),
        )

        result = draw.matches(
            Combination(
                Number(1),
                Number(2),
                Number(3),
                Number(4),
                Number(5),
                Number(6),
            )
        )

        assert result.count == 1
        assert Number(1) in result

    def test_three_matching_numbers(self) -> None:
        draw = make_draw(
            (1, 2, 3, 40, 50, 60),
        )

        result = draw.matches(
            Combination(
                Number(1),
                Number(2),
                Number(3),
                Number(4),
                Number(5),
                Number(6),
            )
        )

        assert result.count == 3
        assert result.numbers == (
            Number(1),
            Number(2),
            Number(3),
        )

    def test_exact_match(self) -> None:
        combination = Combination(
            Number(1),
            Number(2),
            Number(3),
            Number(4),
            Number(5),
            Number(6),
        )

        draw = make_draw(
            (1, 2, 3, 4, 5, 6),
        )

        result = draw.matches(
            combination,
        )

        assert result.is_exact
        assert result.count == 6
        assert result.ratio == 1.0

    def test_match_result_is_immutable(self) -> None:
        draw = make_draw(
            (1, 2, 3, 4, 5, 6),
        )

        combination = Combination(
            Number(1),
            Number(2),
            Number(3),
            Number(7),
            Number(8),
            Number(9),
        )

        first = draw.matches(
            combination,
        )

        second = draw.matches(
            combination,
        )

        assert first == second
