"""Tests for the Research experiment context contracts."""

from __future__ import annotations

import pytest

from sae.research import (
    ExecutionContext,
    Experiment,
    ExperimentConfiguration,
)


def test_configuration_preserves_values_and_stable_json() -> None:
    configuration = ExperimentConfiguration(
        {"replicates": 100, "options": {"replacement": False}, "labels": ["a", "b"]}
    )

    assert configuration.to_json() == (
        '{"labels":["a","b"],"options":{"replacement":false},"replicates":100}'
    )


def test_configuration_is_immutable_at_every_level() -> None:
    source = {"options": {"limits": [1, 2]}}
    configuration = ExperimentConfiguration(source)
    source["options"]["limits"].append(3)

    assert configuration.values["options"]["limits"] == (1, 2)
    with pytest.raises(TypeError):
        configuration.values["new"] = "value"  # type: ignore[index]
    with pytest.raises(TypeError):
        configuration.values["options"]["new"] = "value"  # type: ignore[index]


@pytest.mark.parametrize(
    "invalid",
    [object(), {1: "non-string key"}, {"x": float("nan")}],
)
def test_configuration_rejects_non_json_values(invalid: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        ExperimentConfiguration({"parameter": invalid})


def test_execution_context_accepts_optional_non_negative_seed() -> None:
    assert ExecutionContext().random_seed is None
    assert ExecutionContext(random_seed=0).random_seed == 0


@pytest.mark.parametrize("seed", [-1, True, 1.5, "42"])
def test_execution_context_rejects_invalid_seed(seed: object) -> None:
    with pytest.raises(ValueError):
        ExecutionContext(random_seed=seed)  # type: ignore[arg-type]


def test_experiment_is_immutable_and_keeps_explicit_context() -> None:
    configuration = ExperimentConfiguration({"replicates": 10})
    context = ExecutionContext(random_seed=1234)
    experiment = Experiment(
        experiment_id="exp-001",
        module_id="random-simulation",
        module_version="0.1.0",
        input_fingerprint="sha256:abc123",
        configuration=configuration,
        execution_context=context,
    )

    assert experiment.configuration is configuration
    assert experiment.execution_context is context
    with pytest.raises((AttributeError, TypeError)):
        experiment.module_id = "other"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("experiment_id", ""),
        ("module_id", ""),
        ("module_version", ""),
        ("input_fingerprint", ""),
    ],
)
def test_experiment_rejects_empty_identifiers(field: str, value: str) -> None:
    values = {
        "experiment_id": "exp-001",
        "module_id": "module",
        "module_version": "0.1.0",
        "input_fingerprint": "sha256:abc123",
        "configuration": ExperimentConfiguration({}),
        "execution_context": ExecutionContext(),
    }
    values[field] = value

    with pytest.raises(ValueError):
        Experiment(**values)  # type: ignore[arg-type]


def test_experiment_rejects_wrong_configuration_type() -> None:
    with pytest.raises(TypeError):
        Experiment(
            experiment_id="exp-001",
            module_id="module",
            module_version="0.1.0",
            input_fingerprint="sha256:abc123",
            configuration={},  # type: ignore[arg-type]
        )
