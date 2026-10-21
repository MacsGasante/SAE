"""Immutable identity and execution context for a research experiment."""

from dataclasses import dataclass

from .execution_context import ExecutionContext
from .experiment_configuration import ExperimentConfiguration


@dataclass(frozen=True, slots=True)
class Experiment:
    """Describe a single research execution without performing it.

    The input is identified by a stable fingerprint rather than holding a
    mutable or infrastructure-specific input object. The module and input
    identities are explicit so that result provenance can refer back to them.
    """

    experiment_id: str
    module_id: str
    module_version: str
    input_fingerprint: str
    configuration: ExperimentConfiguration
    execution_context: ExecutionContext = ExecutionContext()

    def __post_init__(self) -> None:
        for field_name in (
            "experiment_id",
            "module_id",
            "module_version",
            "input_fingerprint",
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
