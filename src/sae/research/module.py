"""Research Module protocol and controlled execution boundary."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .experiment import Experiment
from .result import ResearchResult


@runtime_checkable
class ResearchModule(Protocol):
    """Describe an experimental procedure without coupling it to the executor.

    Implementations expose stable identity and return a ResearchResult whose
    provenance refers to the supplied experiment. The executor validates this
    contract before exposing the result to callers.
    """

    @property
    def module_id(self) -> str:
        """Return the stable identifier for this module."""

    @property
    def module_version(self) -> str:
        """Return the explicit version of this module."""

    def execute(self, input_data: object, experiment: Experiment) -> ResearchResult:
        """Execute the module using the declared input and experiment context."""
