from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from sae.kernel.foundation import Number


@dataclass(frozen=True)
class FrequencyResult:
    draw_count: int
    frequencies: Mapping[Number, int]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "frequencies",
            MappingProxyType(dict(self.frequencies)),
        )

    def frequency(self, number: Number) -> int:
        return self.frequencies.get(number, 0)
