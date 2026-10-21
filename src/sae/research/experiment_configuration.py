"""Immutable and stable experiment configuration."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from types import MappingProxyType

type _JSONScalar = str | int | float | bool | None
type _FrozenJSON = _JSONScalar | tuple[_FrozenJSON, ...] | Mapping[str, _FrozenJSON]


def _freeze(value: object) -> _FrozenJSON:
    """Copy a JSON-compatible value into an immutable representation."""
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Configuration floats must be finite.")
        return value

    if isinstance(value, Mapping):
        frozen: dict[str, _FrozenJSON] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("Configuration mapping keys must be strings.")
            frozen[key] = _freeze(item)
        return MappingProxyType(frozen)

    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)

    raise TypeError(
        "Configuration values must contain only JSON-compatible scalars, "
        "mappings, lists, or tuples."
    )


def _thaw(value: _FrozenJSON) -> object:
    """Convert immutable values into JSON-serializable values."""
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


class ExperimentConfiguration:
    """Immutable, JSON-compatible parameters for a research experiment.

    Input mappings are copied on construction. Nested mappings become
    read-only mappings and sequences become tuples, preventing callers from
    mutating the configuration through either the original input or the
    exposed values property.
    """

    __slots__ = ("_values",)

    _values: Mapping[str, _FrozenJSON]

    def __init__(self, values: Mapping[str, object] | None = None) -> None:
        source = {} if values is None else values
        if not isinstance(source, Mapping):
            raise TypeError("Configuration values must be a mapping.")

        frozen = _freeze(source)
        if not isinstance(frozen, Mapping):
            raise TypeError("Configuration values must be a mapping.")
        object.__setattr__(self, "_values", frozen)

    def __setattr__(self, name: str, value: object) -> None:
        """Prevent mutation after construction."""
        raise AttributeError("ExperimentConfiguration is immutable.")

    @property
    def values(self) -> Mapping[str, _FrozenJSON]:
        """Return the immutable configuration values."""
        return self._values

    def to_json(self) -> str:
        """Return a deterministic JSON representation of this configuration."""
        return json.dumps(
            _thaw(self._values),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExperimentConfiguration):
            return NotImplemented
        return self.to_json() == other.to_json()

    def __repr__(self) -> str:
        return f"ExperimentConfiguration(values={dict(self._values)!r})"
