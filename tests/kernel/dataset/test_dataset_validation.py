"""
Dataset validation tests.
"""

from __future__ import annotations

import pytest

from sae.kernel.dataset import Dataset
from sae.kernel.dataset.exceptions import InvalidDatasetError
from tests.kernel.types import DrawFactory


def test_duplicate_draw_id_raises(
    make_draw: DrawFactory,
) -> None:
    """
    Draw identifiers must be unique.
    """
    draw1 = make_draw(
        1,
        2024,
        1,
        1,
        (1, 2, 3, 4, 5, 6),
    )

    draw2 = make_draw(
        1,
        2024,
        1,
        8,
        (10, 11, 12, 13, 14, 15),
    )

    with pytest.raises(
        InvalidDatasetError,
        match="Duplicate DrawId",
    ):
        Dataset([draw1, draw2])


def test_duplicate_draw_date_raises(
    make_draw: DrawFactory,
) -> None:
    """
    Draw dates must be unique.
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
        1,
        (10, 11, 12, 13, 14, 15),
    )

    with pytest.raises(
        InvalidDatasetError,
        match="Duplicate DrawDate",
    ):
        Dataset([draw1, draw2])


def test_invalid_type_raises() -> None:
    """
    Dataset accepts only Draw instances.
    """
    with pytest.raises(
        InvalidDatasetError,
        match="Dataset accepts only Draw instances.",
    ):
        Dataset([object()])


def test_first_on_empty_dataset_raises() -> None:
    """
    Accessing first on an empty Dataset raises.
    """
    dataset = Dataset([])

    with pytest.raises(InvalidDatasetError):
        _ = dataset.first


def test_last_on_empty_dataset_raises() -> None:
    """
    Accessing last on an empty Dataset raises.
    """
    dataset = Dataset([])

    with pytest.raises(InvalidDatasetError):
        _ = dataset.last
