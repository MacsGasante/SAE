"""
Dataset collection protocol tests.
"""

from __future__ import annotations

from sae.kernel.dataset import Dataset
from tests.kernel.types import DrawFactory


def test_len(
    make_draw: DrawFactory,
) -> None:
    """
    Dataset implements the __len__ protocol.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    dataset = Dataset([draw])

    assert dataset.size == 1
    assert dataset.count == 1
    assert len(dataset) == 1


def test_bool_empty() -> None:
    """
    Empty Dataset evaluates to False.
    """
    dataset = Dataset([])

    assert bool(dataset) is False


def test_bool_non_empty(
    make_draw: DrawFactory,
) -> None:
    """
    Non-empty Dataset evaluates to True.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    dataset = Dataset([draw])

    assert bool(dataset) is True


def test_iteration(
    make_draw: DrawFactory,
) -> None:
    """
    Dataset preserves chronological iteration.
    """
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
        1,
        8,
        (10, 11, 12, 13, 14, 15),
    )

    dataset = Dataset([draw1, draw2])

    assert list(dataset) == [
        draw1,
        draw2,
    ]


def test_contains(
    make_draw: DrawFactory,
) -> None:
    """
    Dataset implements membership testing.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    dataset = Dataset([draw])

    assert draw in dataset

    other = make_draw(
        2,
        2024,
        1,
        8,
        (10, 11, 12, 13, 14, 15),
    )

    assert other not in dataset


def test_getitem(
    make_draw: DrawFactory,
) -> None:
    """
    Dataset supports indexing.
    """
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    dataset = Dataset([draw])

    assert dataset[0] == draw
    assert dataset[-1] == draw


def test_reversed(
    make_draw: DrawFactory,
) -> None:
    """
    Dataset supports reversed iteration.
    """
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
        1,
        8,
        (10, 11, 12, 13, 14, 15),
    )

    dataset = Dataset([draw1, draw2])

    assert list(reversed(dataset)) == [
        draw2,
        draw1,
    ]


def test_iteration_returns_draw_objects(
    make_draw: DrawFactory,
) -> None:
    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    dataset = Dataset([draw])

    for item in dataset:
        assert item is draw
