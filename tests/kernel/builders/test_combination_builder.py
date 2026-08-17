"""
Tests for CombinationBuilder.
"""

from __future__ import annotations

import pytest

from sae.kernel.builders import CombinationBuilder
from sae.kernel.collections.combination import Combination
from sae.kernel.exceptions import InvalidCombinationError
from sae.kernel.foundation.number import Number


def test_create_empty_builder() -> None:
    builder = CombinationBuilder()

    assert builder.numbers == ()
    assert len(builder.numbers) == 0


def test_add_number() -> None:
    builder = CombinationBuilder()

    builder.add(Number(10))

    assert builder.numbers == (Number(10),)


def test_extend_numbers() -> None:
    builder = CombinationBuilder()

    builder.extend(
        (
            Number(1),
            Number(2),
            Number(3),
        )
    )

    assert builder.numbers == (
        Number(1),
        Number(2),
        Number(3),
    )


def test_clear_builder() -> None:
    builder = CombinationBuilder()

    builder.add(Number(10))
    builder.add(Number(20))

    builder.clear()

    assert builder.numbers == ()


def test_reset_builder() -> None:
    builder = CombinationBuilder()

    builder.add(Number(10))
    builder.add(Number(20))

    builder.reset()

    builder.add(Number(30))

    assert builder.numbers == (Number(30),)


def test_from_numbers() -> None:
    builder = CombinationBuilder.from_numbers(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert builder.numbers == (
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )


def test_build_valid_combination() -> None:
    combination = (
        CombinationBuilder()
        .add(Number(1))
        .add(Number(2))
        .add(Number(3))
        .add(Number(4))
        .add(Number(5))
        .add(Number(6))
        .build()
    )

    assert isinstance(combination, Combination)

    assert combination.numbers == (
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )


def test_build_returns_new_instance() -> None:
    builder = CombinationBuilder.from_numbers(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    first = builder.build()
    second = builder.build()

    assert first is not second
    assert first == second


def test_build_invalid_combination_raises() -> None:
    builder = CombinationBuilder()

    builder.add(Number(1))

    with pytest.raises(
        InvalidCombinationError,
        match="exactly 6 numbers",
    ):
        builder.build()


def test_duplicate_numbers_raise() -> None:
    builder = CombinationBuilder()

    builder.add(Number(10))
    builder.add(Number(10))
    builder.add(Number(20))
    builder.add(Number(30))
    builder.add(Number(40))
    builder.add(Number(50))

    with pytest.raises(
        InvalidCombinationError,
        match="Duplicate",
    ):
        builder.build()


def test_builder_preserves_insertion_order() -> None:
    builder = CombinationBuilder()

    builder.add(Number(30))
    builder.add(Number(10))
    builder.add(Number(50))

    assert builder.numbers == (
        Number(30),
        Number(10),
        Number(50),
    )


def test_combination_is_sorted_after_build() -> None:
    combination = (
        CombinationBuilder()
        .add(Number(30))
        .add(Number(10))
        .add(Number(50))
        .add(Number(2))
        .add(Number(90))
        .add(Number(1))
        .build()
    )

    assert combination.numbers == (
        Number(1),
        Number(2),
        Number(10),
        Number(30),
        Number(50),
        Number(90),
    )


def test_build_does_not_modify_builder() -> None:
    builder = CombinationBuilder.from_numbers(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    _ = builder.build()

    assert builder.numbers == (
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )
