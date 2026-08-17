"""
Number query tests.
"""

from __future__ import annotations

from sae.kernel.foundation import Number


def test_by_number_returns_draws_containing_number(
    dataset,
) -> None:
    """
    by_number returns draws containing the requested Number.
    """
    number = next(iter(dataset.first.combination))

    result = dataset.query.by_number(
        number,
    ).dataset

    assert result

    for draw in result:
        assert number in draw.combination


def test_contains_is_equivalent_to_by_number(
    dataset,
) -> None:
    """
    contains and by_number return equivalent results.
    """
    number = next(iter(dataset.first.combination))

    left = dataset.query.contains(
        number,
    ).dataset

    right = dataset.query.by_number(
        number,
    ).dataset

    assert tuple(left) == tuple(right)


def test_contains_any_returns_draws_containing_at_least_one_number(
    dataset,
) -> None:
    """
    contains_any returns draws containing at least one requested Number.
    """
    numbers = tuple(dataset.first.combination)[:2]

    result = dataset.query.contains_any(
        *numbers,
    ).dataset

    assert result

    for draw in result:
        assert any(number in draw.combination for number in numbers)


def test_contains_all_returns_draws_containing_all_numbers(
    dataset,
) -> None:
    """
    contains_all returns draws containing every requested Number.
    """
    numbers = tuple(dataset.first.combination)[:2]

    result = dataset.query.contains_all(
        *numbers,
    ).dataset

    assert result

    for draw in result:
        assert all(number in draw.combination for number in numbers)


def test_contains_any_without_numbers_returns_empty_dataset(
    dataset,
) -> None:
    """
    contains_any with no Numbers returns an empty Dataset.
    """
    result = dataset.query.contains_any().dataset

    assert result.is_empty
    assert result.size == 0


def test_contains_all_without_numbers_returns_original_draws(
    dataset,
) -> None:
    """
    contains_all with no Numbers returns every Draw.
    """
    result = dataset.query.contains_all().dataset

    assert tuple(result) == tuple(dataset)


def test_contains_accepts_number_value_object(
    dataset,
) -> None:
    """
    Number queries operate on Number Value Objects.
    """
    number = Number(
        next(iter(dataset.first.combination)).value,
    )

    result = dataset.query.contains(
        number,
    ).dataset

    assert result

    for draw in result:
        assert number in draw.combination
