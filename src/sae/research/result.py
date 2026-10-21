"""Immutable research results and their reproducibility provenance."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from .execution_context import ExecutionContext
from .experiment import Experiment
from .experiment_configuration import ExperimentConfiguration

type _JSONScalar = str | int | float | bool | None
type _FrozenJSON = _JSONScalar | tuple[_FrozenJSON, ...] | Mapping[str, _FrozenJSON]


def _freeze_json(value: object) -> _FrozenJSON:
    """Copy JSON-compatible data into a deeply immutable representation."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Research result floats must be finite.")
        return value
    if isinstance(value, Mapping):
        frozen: dict[str, _FrozenJSON] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("Research result mapping keys must be strings.")
            frozen[key] = _freeze_json(item)
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item) for item in value)
    raise TypeError(
        "Research result values must contain only JSON-compatible scalars, "
        "mappings, lists, or tuples."
    )


@dataclass(frozen=True, slots=True)
class ResearchProvenance:
    """Identify the experiment context needed to interpret a research result."""

    experiment_id: str
    module_id: str
    module_version: str
    input_fingerprint: str
    configuration: ExperimentConfiguration
    execution_context: ExecutionContext
    schema_version: str = "research-result/v1"

    def __post_init__(self) -> None:
        for field_name in (
            "experiment_id",
            "module_id",
            "module_version",
            "input_fingerprint",
            "schema_version",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str):
                raise TypeError(f"{field_name} must be a string.")
            if not value.strip():
                raise ValueError(f"{field_name} must not be empty.")
        if not isinstance(self.configuration, ExperimentConfiguration):
            raise TypeError("configuration must be an ExperimentConfiguration.")
        if not isinstance(self.execution_context, ExecutionContext):
            raise TypeError("execution_context must be an ExecutionContext.")

    @classmethod
    def from_experiment(cls, experiment: Experiment) -> ResearchProvenance:
        """Capture provenance directly from the declared experiment."""
        if not isinstance(experiment, Experiment):
            raise TypeError("experiment must be an Experiment.")
        return cls(
            experiment_id=experiment.experiment_id,
            module_id=experiment.module_id,
            module_version=experiment.module_version,
            input_fingerprint=experiment.input_fingerprint,
            configuration=experiment.configuration,
            execution_context=experiment.execution_context,
        )


@dataclass(frozen=True, slots=True)
class ResearchResult:
    """Immutable experimental evidence with explicit provenance.

    Payload and execution metadata are restricted to JSON-compatible data and
    defensively frozen. The core does not assign scientific meaning to the
    payload and does not interpret it as a prediction or recommendation.
    """

    provenance: ResearchProvenance
    payload: object
    execution_metadata: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.provenance, ResearchProvenance):
            raise TypeError("provenance must be a ResearchProvenance.")
        object.__setattr__(self, "payload", _freeze_json(self.payload))
        metadata = {} if self.execution_metadata is None else self.execution_metadata
        if not isinstance(metadata, Mapping):
            raise TypeError("execution_metadata must be a mapping.")
        frozen_metadata = _freeze_json(metadata)
        if not isinstance(frozen_metadata, Mapping):
            raise TypeError("execution_metadata must be a mapping.")
        object.__setattr__(self, "execution_metadata", frozen_metadata)

    @property
    def experiment_id(self) -> str:
        """Return the identity of the experiment that produced this result."""
        return self.provenance.experiment_id

    @property
    def module_id(self) -> str:
        """Return the producing Research Module identifier."""
        return self.provenance.module_id

    @property
    def module_version(self) -> str:
        """Return the producing Research Module version."""
        return self.provenance.module_version

    @property
    def input_fingerprint(self) -> str:
        """Return the fingerprint of the declared experiment input."""
        return self.provenance.input_fingerprint
