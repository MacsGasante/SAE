"""
Dataset protocol mixin.

Provides the standard Python collection protocol.
"""

from __future__ import annotations

from collections.abc import Iterator

from ..domain import Draw


class DatasetProtocolMixin:
    """
    Standard Python collection protocol.
    """

    _draws: tuple[Draw, ...]

    def __len__(self) -> int:
        return len(self._draws)

    def __bool__(self) -> bool:
        return bool(self._draws)

    def __iter__(self) -> Iterator[Draw]:
        return iter(self._draws)

    def __reversed__(self) -> Iterator[Draw]:
        return reversed(self._draws)

    def __contains__(self, item: object) -> bool:
        return item in self._draws

    def __getitem__(self, index: int) -> Draw:
        return self._draws[index]
