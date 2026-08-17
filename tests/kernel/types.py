"""
Shared type aliases for the Kernel test suite.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

from sae.kernel.collections import Combination
from sae.kernel.domain import Draw
from sae.kernel.foundation import Number

type NumberFactory = Callable[
    [int],
    Number,
]

type CombinationFactory = Callable[
    [Iterable[int]],
    Combination,
]

type DrawFactory = Callable[
    [
        int,
        int,
        int,
        int,
        Iterable[int],
    ],
    Draw,
]
