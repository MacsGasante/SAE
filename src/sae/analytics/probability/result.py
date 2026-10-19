"""Immutable result types for probability analytics."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from sae.kernel.foundation import Number


@dataclass(frozen=True)
class ProbabilityResult:
    """Empirical marginal inclusion rates for valid numbers.

    Attributes:
        draw_count: Number of draws included in the analysis.
        probabilities: Read-only mapping from each valid Number to the
            fraction of analyzed draws containing that number.
    """

    draw_count: int
    probabilities: Mapping[Number, float]

    def __post_init__(self) -> None:
        """Copy the supplied mapping into immutable storage."""
        object.__setattr__(
            self,
            "probabilities",
            MappingProxyType(dict(self.probabilities)),
        )

    def probability(self, number: Number) -> float:
        """Return the empirical rate, or zero if the key is absent."""
        return self.probabilities.get(number, 0.0)
