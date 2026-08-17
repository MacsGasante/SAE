"""
Tests for MatchResult.
"""

from __future__ import annotations

import pytest

from sae.kernel.domain import MatchResult
from sae.kernel.foundation import Number


class TestMatchResult:
    def test_empty_result(self) -> None:
        result = MatchResult(())

        assert result.numbers == ()
        assert result.count == 0

        assert result.is_empty is True
        assert result.matched is False
        assert result.is_exact is False

        assert result.ratio == 0.0

        assert len(result) == 0
        assert bool(result) is False

        assert tuple(result) == ()

    def test_single_match(self) -> None:
        result = MatchResult((Number(42),))

        assert result.numbers == (Number(42),)
        assert result.count == 1

        assert result.is_empty is False
        assert result.matched is True
        assert result.is_exact is False

        assert result.ratio == 1 / 6

        assert len(result) == 1
        assert bool(result) is True

    def test_three_matches(self) -> None:
        result = MatchResult(
            (
                Number(10),
                Number(20),
                Number(30),
            )
        )

        assert result.count == 3
        assert result.ratio == 0.5

        assert result.is_empty is False
        assert result.matched is True
        assert result.is_exact is False

    def test_exact_match(self) -> None:
        result = MatchResult(
            (
                Number(1),
                Number(2),
                Number(3),
                Number(4),
                Number(5),
                Number(6),
            )
        )

        assert result.count == 6
        assert result.is_exact is True
        assert result.ratio == 1.0

    def test_iteration_preserves_order(self) -> None:
        result = MatchResult(
            (
                Number(7),
                Number(11),
                Number(42),
            )
        )

        assert list(result) == [
            Number(7),
            Number(11),
            Number(42),
        ]

        assert tuple(result) == (
            Number(7),
            Number(11),
            Number(42),
        )

    def test_contains_operator(self) -> None:
        result = MatchResult(
            (
                Number(10),
                Number(20),
                Number(30),
            )
        )

        assert Number(10) in result
        assert Number(20) in result
        assert Number(30) in result

        assert Number(90) not in result

    def test_numbers_property_returns_original_tuple(self) -> None:
        numbers = (
            Number(1),
            Number(2),
            Number(3),
        )

        result = MatchResult(numbers)

        assert result.numbers is numbers

    def test_hashable(self) -> None:
        result1 = MatchResult(
            (
                Number(1),
                Number(2),
            )
        )
        result2 = MatchResult(
            (
                Number(1),
                Number(2),
            )
        )

        assert len({result1, result2}) == 1

    def test_equality(self) -> None:
        assert MatchResult(
            (
                Number(1),
                Number(2),
            )
        ) == MatchResult(
            (
                Number(1),
                Number(2),
            )
        )

        assert MatchResult((Number(1),)) != MatchResult(
            (
                Number(1),
                Number(2),
            )
        )

    def test_non_tuple_numbers_are_rejected(self) -> None:
        with pytest.raises(TypeError):
            MatchResult(
                [  # type: ignore[arg-type]
                    Number(1),
                    Number(2),
                ]
            )

    def test_non_number_values_are_rejected(self) -> None:
        with pytest.raises(TypeError):
            MatchResult(
                (
                    Number(1),
                    2,  # type: ignore[arg-type]
                )
            )

    def test_too_many_numbers_are_rejected(self) -> None:
        numbers = tuple(Number(value) for value in range(1, 8))

        with pytest.raises(ValueError):
            MatchResult(numbers)

    def test_numbers_property_preserves_original_tuple(self) -> None:
        numbers = (
            Number(1),
            Number(2),
            Number(3),
        )

        result = MatchResult(numbers)

        assert result.numbers is numbers
