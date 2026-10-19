"""Immutable result types for delay analytics."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from sae.kernel.foundation import Number


@dataclass(frozen=True)
class DelayResult:
    """Last-observed draw delays for numbers in an analyzed dataset.

    Attributes:
        draw_count: Number of draws included in the analysis.
        delays: Read-only mapping to a non-negative delay or None when a
            number does not occur in the analyzed dataset.
    """

    draw_count: int
    delays: Mapping[Number, int | None]

    def __post_init__(self) -> None:
        """Copy the supplied mapping into immutable storage."""
        object.__setattr__(
            self,
            "delays",
            MappingProxyType(dict(self.delays)),
        )

    def delay(self, number: Number) -> int | None:
        """Return the number's delay, or None if the key is absent."""
        return self.delays.get(number)
