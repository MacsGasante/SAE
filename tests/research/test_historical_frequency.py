"""Tests for the historical-frequency Monte Carlo null-model Research Module."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date

import pytest

from sae.kernel import Combination, Draw, DrawDate, DrawId, Number
from sae.kernel.dataset import Dataset
from sae.research import (
    ExecutionContext,
    Experiment,
    ExperimentConfiguration,
    HistoricalFrequencyNullModel,
    ResearchModule,
    ResearchResult,
    dataset_fingerprint,
    execute_research_module,
)


def _dataset(*rows: tuple[int, date, tuple[int, ...]]) -> Dataset:
    return Dataset(
        Draw(
            DrawId(draw_id),
            DrawDate.from_date(draw_date),
            Combination(*(Number(value) for value in numbers)),
        )
        for draw_id, draw_date, numbers in rows
    )


def _experiment(
    dataset: Dataset,
    *,
    replicate_count: int = 25,
    seed: int | None = 1729,
    module_id: str | None = None,
    module_version: str | None = None,
    fingerprint: str | None = None,
) -> Experiment:
    module = HistoricalFrequencyNullModel()
    return Experiment(
        experiment_id="historical-null-test",
        module_id=module.module_id if module_id is None else module_id,
        module_version=(
            module.module_version if module_version is None else module_version
        ),
        input_fingerprint=(
            dataset_fingerprint(dataset) if fingerprint is None else fingerprint
        ),
        configuration=ExperimentConfiguration({"replicate_count": replicate_count}),
        execution_context=ExecutionContext(random_seed=seed),
    )


@pytest.fixture
def small_dataset() -> Dataset:
    return _dataset(
        (2023001, date(2023, 1, 1), (1, 2, 3, 4, 5, 6)),
        (2023002, date(2023, 1, 3), (7, 8, 9, 10, 11, 12)),
        (2023003, date(2023, 1, 5), (1, 7, 20, 30, 40, 50)),
    )


def test_module_satisfies_research_module_protocol() -> None:
    assert isinstance(HistoricalFrequencyNullModel(), ResearchModule)


def test_dataset_fingerprint_is_stable_and_sensitive_to_content(
    small_dataset: Dataset,
) -> None:
    same_content = _dataset(
        (2023001, date(2023, 1, 1), (1, 2, 3, 4, 5, 6)),
        (2023002, date(2023, 1, 3), (7, 8, 9, 10, 11, 12)),
        (2023003, date(2023, 1, 5), (1, 7, 20, 30, 40, 50)),
    )
    changed_content = _dataset(
        (2023001, date(2023, 1, 1), (1, 2, 3, 4, 5, 6)),
        (2023002, date(2023, 1, 3), (7, 8, 9, 10, 11, 12)),
        (2023003, date(2023, 1, 5), (1, 7, 20, 30, 40, 51)),
    )

    assert dataset_fingerprint(small_dataset) == dataset_fingerprint(same_content)
    assert dataset_fingerprint(small_dataset) != dataset_fingerprint(changed_content)
    assert len(dataset_fingerprint(small_dataset)) == 64


def test_test_is_reproducible_and_records_statistical_invariants(
    small_dataset: Dataset,
) -> None:
    module = HistoricalFrequencyNullModel()
    experiment = _experiment(small_dataset, replicate_count=40, seed=42)
    first = execute_research_module(module, small_dataset, experiment)
    second = execute_research_module(module, small_dataset, experiment)

    assert first == second
    assert isinstance(first, ResearchResult)
    assert isinstance(first.payload, Mapping)
    payload = first.payload
    frequencies = payload["number_frequencies"]
    assert isinstance(frequencies, Mapping)
    assert len(frequencies) == 90
    assert set(frequencies) == {str(number) for number in range(1, 91)}
    assert sum(frequencies.values()) == 6 * small_dataset.size
    assert payload["replicate_count"] == 40
    assert 0 <= payload["exceedance_count"] <= 40
    assert payload["monte_carlo_p_value"] == ((payload["exceedance_count"] + 1) / 41)
    assert payload["observed_max_absolute_standardized_deviation"] >= 0
    assert first.provenance.execution_context.random_seed == 42
    assert first.provenance.input_fingerprint == dataset_fingerprint(small_dataset)
    assert isinstance(first.execution_metadata, Mapping)
    assert first.execution_metadata["dataset_fingerprint"] == dataset_fingerprint(
        small_dataset
    )


def test_rejects_non_dataset_input(small_dataset: Dataset) -> None:
    with pytest.raises(TypeError, match="input_data"):
        HistoricalFrequencyNullModel().execute([], _experiment(small_dataset))


def test_rejects_empty_dataset() -> None:
    empty = Dataset([])
    with pytest.raises(ValueError, match="non-empty"):
        HistoricalFrequencyNullModel().execute(empty, _experiment(empty))


def test_rejects_fingerprint_mismatch(small_dataset: Dataset) -> None:
    experiment = _experiment(small_dataset, fingerprint="not-the-dataset-fingerprint")
    with pytest.raises(ValueError, match="input_fingerprint"):
        HistoricalFrequencyNullModel().execute(small_dataset, experiment)


@pytest.mark.parametrize("replicate_count", [0, -1, True, 1.5, "20", None])
def test_rejects_invalid_replicate_count(
    small_dataset: Dataset,
    replicate_count: object,
) -> None:
    experiment = Experiment(
        experiment_id="invalid-replicates",
        module_id=HistoricalFrequencyNullModel().module_id,
        module_version=HistoricalFrequencyNullModel().module_version,
        input_fingerprint=dataset_fingerprint(small_dataset),
        configuration=ExperimentConfiguration({"replicate_count": replicate_count}),
        execution_context=ExecutionContext(random_seed=1),
    )
    with pytest.raises(ValueError, match="replicate_count"):
        HistoricalFrequencyNullModel().execute(small_dataset, experiment)


def test_requires_explicit_seed(small_dataset: Dataset) -> None:
    with pytest.raises(ValueError, match="random_seed"):
        HistoricalFrequencyNullModel().execute(
            small_dataset,
            _experiment(small_dataset, seed=None),
        )


def test_rejects_experiment_for_another_module(small_dataset: Dataset) -> None:
    with pytest.raises(ValueError, match="module_id"):
        HistoricalFrequencyNullModel().execute(
            small_dataset,
            _experiment(small_dataset, module_id="other.module"),
        )


def test_rejects_incompatible_module_version(small_dataset: Dataset) -> None:
    with pytest.raises(ValueError, match="module_version"):
        HistoricalFrequencyNullModel().execute(
            small_dataset,
            _experiment(small_dataset, module_version="99.0"),
        )


def test_dataset_fingerprint_rejects_non_dataset_input() -> None:
    with pytest.raises(TypeError, match="dataset"):
        dataset_fingerprint([])  # type: ignore[arg-type]


def test_rejects_non_experiment_context(small_dataset: Dataset) -> None:
    with pytest.raises(TypeError, match="experiment"):
        HistoricalFrequencyNullModel().execute(small_dataset, object())
