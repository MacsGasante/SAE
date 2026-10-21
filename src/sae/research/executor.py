"""Controlled execution for Research Modules."""

from __future__ import annotations

from .experiment import Experiment
from .module import ResearchModule
from .result import ResearchProvenance, ResearchResult


class ResearchExecutionError(RuntimeError):
    """Raised when a Research Module cannot satisfy the execution contract."""


def execute_research_module(
    module: ResearchModule,
    input_data: object,
    experiment: Experiment,
) -> ResearchResult:
    """Execute a module and validate its identity and result provenance.

    This function deliberately does not fingerprint inputs, persist results,
    retry executions, or add statistical interpretation. The caller supplies
    an Experiment whose input fingerprint must describe input_data.
    """
    if not isinstance(experiment, Experiment):
        raise TypeError("experiment must be an Experiment.")

    if not isinstance(module, ResearchModule):
        raise TypeError("module must implement the ResearchModule protocol.")

    module_id = module.module_id
    module_version = module.module_version
    for field_name, value in (
        ("module_id", module_id),
        ("module_version", module_version),
    ):
        if not isinstance(value, str):
            raise TypeError(f"Research Module {field_name} must be a string.")
        if not value.strip():
            raise ValueError(f"Research Module {field_name} must not be empty.")

    if module_id != experiment.module_id:
        raise ResearchExecutionError(
            "Research Module identifier does not match the experiment."
        )
    if module_version != experiment.module_version:
        raise ResearchExecutionError(
            "Research Module version does not match the experiment."
        )

    try:
        result = module.execute(input_data, experiment)
    except Exception as exc:
        raise ResearchExecutionError("Research Module execution failed.") from exc

    if not isinstance(result, ResearchResult):
        raise ResearchExecutionError(
            "Research Module execute() must return a ResearchResult."
        )

    expected_provenance = ResearchProvenance.from_experiment(experiment)
    if result.provenance != expected_provenance:
        raise ResearchExecutionError(
            "Research Result provenance does not match the experiment."
        )

    return result
