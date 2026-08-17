"""
Dataset construction tests.
"""

from __future__ import annotations

from sae.kernel.dataset import Dataset
from tests.kernel.types import DrawFactory


def test_create_empty_dataset() -> None:
    """
    An empty iterable creates an empty Dataset.
    """
    dataset = Dataset([])

    assert dataset.draws == ()

    assert dataset.is_empty
    assert dataset.size == 0
    assert dataset.count == 0
    assert len(dataset) == 0

    assert bool(dataset) is False


def test_create_dataset_from_single_draw(
    make_draw: DrawFactory,
) -> None:
    """
    A Dataset containing one Draw exposes the same object
    as first and last.
    """
    draw = make_draw(
        1,
        2024,
        1,
        4,
        (1, 2, 3, 4, 5, 6),
    )

    dataset = Dataset([draw])

    assert dataset.draws == (draw,)

    assert dataset.size == 1
    assert dataset.count == 1
    assert len(dataset) == 1

    assert dataset.first == draw
    assert dataset.last == draw

    assert not dataset.is_empty
    assert bool(dataset) is True


def test_dataset_is_sorted_by_date(
    make_draw: DrawFactory,
) -> None:
    """
    Draws are automatically sorted chronologically.
    """
    newer = make_draw(
        2,
        2024,
        2,
        1,
        (10, 11, 12, 13, 14, 15),
    )

    older = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    dataset = Dataset([newer, older])

    assert dataset.first == older
    assert dataset.last == newer

    assert dataset.draws == (
        older,
        newer,
    )

    assert list(dataset) == [
        older,
        newer,
    ]


def test_dataset_sorts_multiple_draws(
    make_draw: DrawFactory,
) -> None:
    """
    Multiple Draws are always sorted chronologically.
    """
    draw3 = make_draw(
        3,
        2024,
        3,
        1,
        (20, 21, 22, 23, 24, 25),
    )

    draw1 = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    draw2 = make_draw(
        2,
        2024,
        2,
        1,
        (10, 11, 12, 13, 14, 15),
    )

    dataset = Dataset([draw3, draw1, draw2])

    assert tuple(dataset) == (
        draw1,
        draw2,
        draw3,
    )
