"""Explicit execution metadata relevant to reproducibility."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """Execution settings that affect reproducibility.

    random_seed is optional for deterministic modules and must be set
    explicitly by modules that use randomness. Seed values are non-negative
    integers; booleans are rejected even though bool subclasses int.
    """

    random_seed: int | None = None

    def __post_init__(self) -> None:
        if self.random_seed is not None and (
            type(self.random_seed) is not int or self.random_seed < 0
        ):
            raise ValueError("random_seed must be a non-negative integer or None.")
