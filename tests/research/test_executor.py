"""Tests for the Research Module contract and controlled executor."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from sae.research import (
    ExecutionContext,
    Experiment,
    ExperimentConfiguration,
    ResearchProvenance,
    ResearchResult,
)
from sae.research.executor import ResearchExecutionError, execute_research_module


def make_experiment(
    *,
    module_id: str = "test-module",
    module_version: str = "1.0.0",
) -> Experiment:
    return Experiment(
        experiment_id="experiment-001",
        module_id=module_id,
        module_version=module_version,
        input_fingerprint="sha256:input",
        configuration=ExperimentConfiguration({"runs": 10}),
        execution_context=ExecutionContext(random_seed=17),
    )


@dataclass
class ExampleModule:
    module_id: str = "test-module"
    module_version: str = "1.0.0"

    def execute(self, input_data: object, experiment: Experiment) -> ResearchResult:
        return ResearchResult(
            provenance=ResearchProvenance.from_experiment(experiment),
            payload={"observed": input_data, "runs": 10},
        )


def test_executor_returns_result_with_matching_provenance() -> None:
    experiment = make_experiment()
    input_data = {"read_only_by_contract": True}

    result = execute_research_module(ExampleModule(), input_data, experiment)

    assert result.experiment_id == experiment.experiment_id
    assert result.module_id == experiment.module_id
    assert result.module_version == experiment.module_version
    assert result.provenance == ResearchProvenance.from_experiment(experiment)
    assert result.payload["observed"]["read_only_by_contract"] is True  # type: ignore[index]


@pytest.mark.parametrize(
    ("module", "experiment"),
    [
        (ExampleModule(module_id="other-module"), make_experiment()),
        (
            ExampleModule(module_version="2.0.0"),
            make_experiment(),
        ),
    ],
)
def test_executor_rejects_module_identity_mismatch(
    module: ExampleModule,
    experiment: Experiment,
) -> None:
    with pytest.raises(ResearchExecutionError):
        execute_research_module(module, object(), experiment)


@pytest.mark.parametrize(
    ("field", "value", "error_type"),
    [
        ("module_id", "", ValueError),
        ("module_version", "", ValueError),
        ("module_id", 3, TypeError),
        ("module_version", None, TypeError),
    ],
)
def test_executor_rejects_invalid_module_identity(
    field: str,
    value: object,
    error_type: type[Exception],
) -> None:
    module = ExampleModule()
    setattr(module, field, value)

    with pytest.raises(error_type):
        execute_research_module(module, None, make_experiment())


def test_executor_rejects_non_module_and_invalid_experiment() -> None:
    with pytest.raises(TypeError, match="ResearchModule"):
        execute_research_module(object(), None, make_experiment())  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="experiment"):
        execute_research_module(ExampleModule(), None, object())  # type: ignore[arg-type]


class InvalidResultModule(ExampleModule):
    def execute(self, input_data: object, experiment: Experiment) -> ResearchResult:
        return object()  # type: ignore[return-value]


def test_executor_rejects_non_research_result() -> None:
    with pytest.raises(ResearchExecutionError, match="must return a ResearchResult"):
        execute_research_module(
            InvalidResultModule(),
            None,
            make_experiment(),
        )


class WrongProvenanceModule(ExampleModule):
    def execute(self, input_data: object, experiment: Experiment) -> ResearchResult:
        other_experiment = make_experiment(module_id="other-module")
        return ResearchResult(
            provenance=ResearchProvenance.from_experiment(other_experiment),
            payload={"ok": True},
        )


def test_executor_rejects_result_with_mismatched_provenance() -> None:
    with pytest.raises(ResearchExecutionError, match="provenance"):
        execute_research_module(
            WrongProvenanceModule(),
            None,
            make_experiment(),
        )


class FailingModule(ExampleModule):
    def execute(self, input_data: object, experiment: Experiment) -> ResearchResult:
        raise ArithmeticError("experimental calculation failed")


def test_executor_wraps_module_failure_and_preserves_cause() -> None:
    with pytest.raises(ResearchExecutionError, match="execution failed") as exc_info:
        execute_research_module(FailingModule(), None, make_experiment())

    assert isinstance(exc_info.value.__cause__, ArithmeticError)
