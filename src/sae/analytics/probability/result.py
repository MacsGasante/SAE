from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from sae.kernel.foundation import Number


@dataclass(frozen=True)
class ProbabilityResult:
    draw_count: int
    probabilities: Mapping[Number, float]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "probabilities",
            MappingProxyType(dict(self.probabilities)),
        )

    def probability(self, number: Number) -> float:
        return self.probabilities.get(number, 0.0)
