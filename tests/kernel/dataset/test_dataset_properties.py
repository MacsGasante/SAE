"""
Dataset property tests.
"""

from __future__ import annotations

from sae.kernel.dataset import Dataset
from tests.kernel.types import DrawFactory


def test_draws_returns_tuple(
    make_draw: DrawFactory,
) -> None:
    """
    Dataset exposes an immutable tuple of draws.
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

    assert dataset.draws == (
        draw1,
        draw2,
    )

    assert isinstance(
        dataset.draws,
        tuple,
    )

    assert tuple(dataset) == dataset.draws
    assert dataset.draws is dataset.draws


def test_first_returns_oldest_draw(
    make_draw: DrawFactory,
) -> None:
    """
    first returns the chronologically oldest draw.
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

    dataset = Dataset(
        [
            newer,
            older,
        ]
    )

    assert dataset.first == older


def test_last_returns_newest_draw(
    make_draw: DrawFactory,
) -> None:
    """
    last returns the chronologically newest draw.
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

    dataset = Dataset(
        [
            newer,
            older,
        ]
    )

    assert dataset.last == newer


def test_size_matches_count(
    make_draw: DrawFactory,
) -> None:
    """
    size and count always expose the same value.
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
    assert len(dataset.draws) == dataset.size


def test_is_empty_reflects_content(
    make_draw: DrawFactory,
) -> None:
    """
    is_empty reflects the dataset content.
    """
    empty = Dataset([])

    assert empty.is_empty

    draw = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    dataset = Dataset([draw])

    assert not dataset.is_empty
