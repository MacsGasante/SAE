from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from sae.kernel.foundation import Number


@dataclass(frozen=True)
class DelayResult:
    draw_count: int
    delays: Mapping[Number, int | None]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "delays",
            MappingProxyType(dict(self.delays)),
        )

    def delay(self, number: Number) -> int | None:
        return self.delays.get(number)
