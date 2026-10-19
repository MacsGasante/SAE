"""Immutable result types for frequency analytics."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from sae.kernel.foundation import Number


@dataclass(frozen=True)
class FrequencyResult:
    """Occurrence counts for valid numbers in an analyzed dataset.

    Attributes:
        draw_count: Number of draws included in the analysis.
        frequencies: Read-only mapping from each valid Number to its count.
    """

    draw_count: int
    frequencies: Mapping[Number, int]

    def __post_init__(self) -> None:
        """Copy the supplied mapping into immutable storage."""
        object.__setattr__(
            self,
            "frequencies",
            MappingProxyType(dict(self.frequencies)),
        )

    def frequency(self, number: Number) -> int:
        """Return the occurrence count, or zero if the key is absent."""
        return self.frequencies.get(number, 0)
