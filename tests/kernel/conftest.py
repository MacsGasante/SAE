"""
Shared pytest fixtures for the Kernel test suite.
"""

from __future__ import annotations

from collections.abc import Iterable

import pytest

from sae.kernel.collections import Combination
from sae.kernel.dataset import Dataset
from sae.kernel.domain import Draw, DrawDate, DrawId
from sae.kernel.foundation import Number

from .types import (
    CombinationFactory,
    DrawFactory,
    NumberFactory,
)


@pytest.fixture
def make_number() -> NumberFactory:
    """
    Factory fixture creating Number instances.
    """

    def factory(value: int) -> Number:
        return Number(value)

    return factory


@pytest.fixture
def make_combination(
    make_number: NumberFactory,
) -> CombinationFactory:
    """
    Factory fixture producing immutable Combination objects.
    """

    def factory(
        numbers: Iterable[int],
    ) -> Combination:
        converted = tuple(make_number(number) for number in numbers)

        return Combination(*converted)

    return factory


@pytest.fixture
def make_draw(
    make_combination: CombinationFactory,
) -> DrawFactory:
    """
    Factory fixture creating Draw instances.
    """

    def factory(
        draw_id: int,
        year: int,
        month: int,
        day: int,
        numbers: Iterable[int],
    ) -> Draw:
        return Draw(
            id=DrawId(draw_id),
            date=DrawDate.from_parts(
                year,
                month,
                day,
            ),
            combination=make_combination(numbers),
        )

    return factory


@pytest.fixture
def empty_dataset() -> Dataset:
    """
    Return an empty Dataset.
    """
    return Dataset([])


@pytest.fixture
def reference_combination(
    make_combination: CombinationFactory,
) -> Combination:
    """
    Canonical Combination used by Query Layer tests.
    """
    return make_combination(
        (
            1,
            2,
            3,
            4,
            5,
            6,
        )
    )


@pytest.fixture
def impossible_combination(
    make_combination: CombinationFactory,
) -> Combination:
    """
    Combination unlikely to appear in fixture datasets.
    """
    return make_combination(
        (
            85,
            86,
            87,
            88,
            89,
            90,
        )
    )


@pytest.fixture
def dataset(
    make_draw: DrawFactory,
) -> Dataset:
    """
    Small immutable Dataset used by query tests.
    """
    return Dataset(
        (
            make_draw(
                1,
                2023,
                1,
                5,
                (1, 2, 3, 4, 5, 6),
            ),
            make_draw(
                2,
                2024,
                2,
                10,
                (7, 8, 9, 10, 11, 12),
            ),
            make_draw(
                3,
                2024,
                6,
                20,
                (1, 7, 20, 30, 40, 50),
            ),
            make_draw(
                4,
                2025,
                3,
                1,
                (2, 8, 14, 21, 42, 77),
            ),
        )
    )
