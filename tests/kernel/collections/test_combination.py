from __future__ import annotations

import pytest

from sae.kernel.collections import Combination
from sae.kernel.exceptions import InvalidCombinationError
from sae.kernel.foundation import Number

# ---------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------


def test_valid_combination() -> None:
    c = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert c.size == 6


def test_unsorted_input_is_sorted() -> None:
    c = Combination(
        Number(90),
        Number(1),
        Number(17),
        Number(5),
        Number(44),
        Number(12),
    )

    assert tuple(n.value for n in c) == (
        1,
        5,
        12,
        17,
        44,
        90,
    )


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------


def test_duplicate_numbers() -> None:
    with pytest.raises(
        InvalidCombinationError,
        match="Duplicate",
    ):
        Combination(
            Number(1),
            Number(2),
            Number(2),
            Number(4),
            Number(5),
            Number(6),
        )


def test_wrong_cardinality() -> None:
    with pytest.raises(
        InvalidCombinationError,
        match="exactly 6 numbers",
    ):
        Combination(
            Number(1),
            Number(2),
            Number(3),
        )


def test_wrong_type() -> None:
    with pytest.raises(InvalidCombinationError):
        Combination(
            Number(1),
            Number(2),
            Number(3),
            Number(4),
            Number(5),
            6,  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------
# API
# ---------------------------------------------------------------------


def test_minimum() -> None:
    c = Combination(
        Number(4),
        Number(90),
        Number(2),
        Number(30),
        Number(50),
        Number(8),
    )

    assert c.minimum == Number(2)


def test_maximum() -> None:
    c = Combination(
        Number(4),
        Number(90),
        Number(2),
        Number(30),
        Number(50),
        Number(8),
    )

    assert c.maximum == Number(90)


def test_contains_number() -> None:
    c = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert Number(4) in c


def test_contains_int_is_false() -> None:
    c = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert 4 not in c


def test_iteration() -> None:
    c = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert [n.value for n in c] == [1, 2, 3, 4, 5, 6]


def test_repr() -> None:
    c = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert repr(c) == "Combination(1, 2, 3, 4, 5, 6)"


# ---------------------------------------------------------------------
# Equality / Hash
# ---------------------------------------------------------------------


def test_same_numbers_different_order() -> None:
    a = Combination(
        Number(90),
        Number(1),
        Number(17),
        Number(5),
        Number(44),
        Number(12),
    )

    b = Combination(
        Number(1),
        Number(5),
        Number(12),
        Number(17),
        Number(44),
        Number(90),
    )

    assert a == b
    assert hash(a) == hash(b)


def test_hashable() -> None:
    values = {
        Combination(
            Number(1),
            Number(2),
            Number(3),
            Number(4),
            Number(5),
            Number(6),
        ),
        Combination(
            Number(6),
            Number(5),
            Number(4),
            Number(3),
            Number(2),
            Number(1),
        ),
    }

    assert len(values) == 1


def test_numbers_property_returns_sorted_tuple() -> None:
    combination = Combination(
        Number(90),
        Number(1),
        Number(50),
        Number(2),
        Number(30),
        Number(10),
    )

    assert combination.numbers == (
        Number(1),
        Number(2),
        Number(10),
        Number(30),
        Number(50),
        Number(90),
    )


def test_numbers_set_contains_all_numbers() -> None:
    combination = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert combination.numbers_set == {
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    }


def test_numbers_set() -> None:
    combination = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert combination.numbers_set == frozenset(
        {
            Number(1),
            Number(2),
            Number(3),
            Number(4),
            Number(5),
            Number(6),
        }
    )


def test_numbers_set_is_immutable() -> None:
    combination = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    assert isinstance(
        combination.numbers_set,
        frozenset,
    )


def test_combination_is_immutable() -> None:
    combination = Combination(
        Number(1),
        Number(2),
        Number(3),
        Number(4),
        Number(5),
        Number(6),
    )

    with pytest.raises(AttributeError):
        combination._numbers = (  # type: ignore[misc]
            Number(10),
            Number(20),
            Number(30),
            Number(40),
            Number(50),
            Number(60),
        )
