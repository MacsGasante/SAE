"""Tests for the seeded Monte Carlo Research Module."""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from sae.research import (
    ExecutionContext,
    Experiment,
    ExperimentConfiguration,
    ResearchModule,
    ResearchResult,
    execute_research_module,
)
from sae.research.monte_carlo import MonteCarloDrawSimulation


def _experiment(
    *,
    draw_count: int = 250,
    seed: int | None = 1729,
    module_id: str | None = None,
    module_version: str | None = None,
) -> Experiment:
    module = MonteCarloDrawSimulation()
    return Experiment(
        experiment_id="mc-test",
        module_id=module.module_id if module_id is None else module_id,
        module_version=(
            module.module_version if module_version is None else module_version
        ),
        input_fingerprint="self-contained:none",
        configuration=ExperimentConfiguration({"draw_count": draw_count}),
        execution_context=ExecutionContext(random_seed=seed),
    )


def test_module_satisfies_research_module_protocol() -> None:
    assert isinstance(MonteCarloDrawSimulation(), ResearchModule)


def test_simulation_is_reproducible_for_same_seed_and_configuration() -> None:
    module = MonteCarloDrawSimulation()
    experiment = _experiment()
    first = execute_research_module(module, None, experiment)
    second = execute_research_module(module, None, experiment)

    assert first == second
    assert first.payload == second.payload
    assert first.provenance == second.provenance


def test_simulation_records_frequency_totals_and_provenance() -> None:
    result = execute_research_module(
        MonteCarloDrawSimulation(),
        None,
        _experiment(draw_count=100, seed=42),
    )

    assert isinstance(result, ResearchResult)
    assert isinstance(result.payload, Mapping)
    payload = result.payload
    assert payload["draw_count"] == 100
    assert payload["number_domain_max"] == 90
    assert payload["numbers_per_draw"] == 6

    frequencies = payload["number_frequencies"]
    assert isinstance(frequencies, Mapping)
    assert len(frequencies) == 90
    assert sum(frequencies.values()) == 600
    assert all(0 <= count <= 100 for count in frequencies.values())
    assert result.provenance.execution_context.random_seed == 42
    assert isinstance(result.execution_metadata, Mapping)
    assert result.execution_metadata["random_seed"] == 42


@pytest.mark.parametrize("draw_count", [0, -1, True, 1.5, "10"])
def test_simulation_rejects_invalid_draw_count(draw_count: object) -> None:
    experiment = Experiment(
        experiment_id="mc-invalid-config",
        module_id=MonteCarloDrawSimulation().module_id,
        module_version=MonteCarloDrawSimulation().module_version,
        input_fingerprint="self-contained:none",
        configuration=ExperimentConfiguration({"draw_count": draw_count}),
        execution_context=ExecutionContext(random_seed=1),
    )

    with pytest.raises(ValueError, match="draw_count"):
        MonteCarloDrawSimulation().execute(None, experiment)


def test_simulation_requires_explicit_seed() -> None:
    with pytest.raises(ValueError, match="random_seed"):
        MonteCarloDrawSimulation().execute(None, _experiment(seed=None))


def test_simulation_rejects_nonempty_input() -> None:
    with pytest.raises(TypeError, match="input_data"):
        MonteCarloDrawSimulation().execute([], _experiment())


def test_simulation_rejects_experiment_for_another_module() -> None:
    with pytest.raises(ValueError, match="module_id"):
        MonteCarloDrawSimulation().execute(
            None,
            _experiment(module_id="other.module"),
        )


def test_simulation_rejects_incompatible_module_version() -> None:
    with pytest.raises(ValueError, match="module_version"):
        MonteCarloDrawSimulation().execute(
            None,
            _experiment(module_version="99.0"),
        )


def test_simulation_result_is_immutable() -> None:
    result = MonteCarloDrawSimulation().execute(None, _experiment())
    assert isinstance(result.payload, Mapping)
    frequencies = result.payload["number_frequencies"]
    assert isinstance(frequencies, Mapping)

    with pytest.raises(TypeError):
        frequencies["1"] = 999  # type: ignore[index]
