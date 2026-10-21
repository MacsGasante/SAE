"""Tests for immutable Research Results and provenance."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from sae.research import (
    ExecutionContext,
    Experiment,
    ExperimentConfiguration,
    ResearchProvenance,
    ResearchResult,
)


def make_experiment() -> Experiment:
    return Experiment(
        experiment_id="exp-001",
        module_id="example-module",
        module_version="0.1.0",
        input_fingerprint="sha256:abc123",
        configuration=ExperimentConfiguration({"replicates": 100}),
        execution_context=ExecutionContext(random_seed=42),
    )


def test_provenance_captures_experiment_identity_and_reproducibility_context() -> None:
    experiment = make_experiment()
    provenance = ResearchProvenance.from_experiment(experiment)

    assert provenance.experiment_id == "exp-001"
    assert provenance.module_id == "example-module"
    assert provenance.module_version == "0.1.0"
    assert provenance.input_fingerprint == "sha256:abc123"
    assert provenance.configuration is experiment.configuration
    assert provenance.execution_context is experiment.execution_context
    assert provenance.schema_version == "research-result/v1"


def test_result_exposes_provenance_and_payload() -> None:
    provenance = ResearchProvenance.from_experiment(make_experiment())
    result = ResearchResult(
        provenance=provenance,
        payload={"iterations": 100, "summary": {"accepted": 72}},
    )

    assert result.experiment_id == "exp-001"
    assert result.module_id == "example-module"
    assert result.module_version == "0.1.0"
    assert result.input_fingerprint == "sha256:abc123"
    assert result.payload["iterations"] == 100  # type: ignore[index]
    assert result.payload["summary"]["accepted"] == 72  # type: ignore[index]


def test_result_deeply_freezes_payload_and_execution_metadata() -> None:
    provenance = ResearchProvenance.from_experiment(make_experiment())
    source_payload = {"values": [1, 2], "nested": {"enabled": True}}
    source_metadata = {"runtime": {"python": "3.12"}}
    result = ResearchResult(
        provenance=provenance,
        payload=source_payload,
        execution_metadata=source_metadata,
    )
    source_payload["values"].append(3)
    source_payload["nested"]["enabled"] = False
    source_metadata["runtime"]["python"] = "3.13"

    assert result.payload["values"] == (1, 2)  # type: ignore[index]
    assert result.payload["nested"]["enabled"] is True  # type: ignore[index]
    assert result.execution_metadata["runtime"]["python"] == "3.12"  # type: ignore[index]
    with pytest.raises(TypeError):
        result.payload["new"] = "value"  # type: ignore[index]
    with pytest.raises(TypeError):
        result.payload["nested"]["new"] = "value"  # type: ignore[index]
    with pytest.raises(TypeError):
        result.execution_metadata["new"] = "value"  # type: ignore[index]


def test_result_and_provenance_are_frozen() -> None:
    provenance = ResearchProvenance.from_experiment(make_experiment())
    result = ResearchResult(provenance=provenance, payload={"ok": True})
    with pytest.raises(FrozenInstanceError):
        provenance.module_id = "other"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.payload = {}  # type: ignore[misc]


@pytest.mark.parametrize(
    "invalid_payload",
    [object(), {1: "invalid key"}, {"value": float("nan")}, {"value": float("inf")}],
)
def test_result_rejects_non_json_payload_values(invalid_payload: object) -> None:
    provenance = ResearchProvenance.from_experiment(make_experiment())
    with pytest.raises((TypeError, ValueError)):
        ResearchResult(provenance=provenance, payload=invalid_payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("experiment_id", ""),
        ("module_id", ""),
        ("module_version", ""),
        ("input_fingerprint", ""),
        ("schema_version", ""),
    ],
)
def test_provenance_rejects_empty_identity_fields(field: str, value: str) -> None:
    experiment = make_experiment()
    values = {
        "experiment_id": experiment.experiment_id,
        "module_id": experiment.module_id,
        "module_version": experiment.module_version,
        "input_fingerprint": experiment.input_fingerprint,
        "configuration": experiment.configuration,
        "execution_context": experiment.execution_context,
        "schema_version": "research-result/v1",
    }
    values[field] = value
    with pytest.raises(ValueError):
        ResearchProvenance(**values)  # type: ignore[arg-type]


def test_provenance_rejects_invalid_context_types() -> None:
    experiment = make_experiment()
    values = {
        "experiment_id": experiment.experiment_id,
        "module_id": experiment.module_id,
        "module_version": experiment.module_version,
        "input_fingerprint": experiment.input_fingerprint,
        "configuration": experiment.configuration,
        "execution_context": experiment.execution_context,
    }
    with pytest.raises(TypeError):
        ResearchProvenance(**{**values, "configuration": {}})  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ResearchProvenance(**{**values, "execution_context": {}})  # type: ignore[arg-type]


def test_execution_metadata_must_be_a_mapping() -> None:
    provenance = ResearchProvenance.from_experiment(make_experiment())
    with pytest.raises(TypeError):
        ResearchResult(
            provenance=provenance,
            payload={"ok": True},
            execution_metadata=["not", "a", "mapping"],
        )
