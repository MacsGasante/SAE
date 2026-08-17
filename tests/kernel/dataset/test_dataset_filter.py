"""
Dataset filter() tests.
"""

from __future__ import annotations

from sae.kernel.dataset import Dataset
from tests.kernel.types import DrawFactory


def test_filter_keeps_matching_draws(
    make_draw: DrawFactory,
) -> None:
    draw1 = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    draw2 = make_draw(
        2,
        2025,
        1,
        1,
        (10, 11, 12, 13, 14, 15),
    )

    dataset = Dataset([draw1, draw2])

    filtered = dataset.filter(
        lambda draw: draw.date.year == 2024,
    )

    assert filtered is not dataset
    assert tuple(filtered) == (draw1,)
    assert filtered.size == 1
    assert filtered.first == draw1


def test_filter_empty_result_returns_empty_dataset(
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

    filtered = dataset.filter(lambda _: False)

    assert filtered.is_empty


def test_filter_preserves_order(
    make_draw: DrawFactory,
) -> None:
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

    dataset = Dataset([draw1, draw2])

    filtered = dataset.filter(lambda _: True)

    assert list(filtered) == [
        draw1,
        draw2,
    ]


def test_filter_does_not_modify_original_dataset(
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

    original = dataset.draws

    _ = dataset.filter(lambda _: False)

    assert dataset.draws == original
    assert dataset.size == 1
