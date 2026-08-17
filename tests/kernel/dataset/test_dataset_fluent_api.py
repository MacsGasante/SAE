"""
Dataset Query Fluent API tests.
"""

from __future__ import annotations

from sae.kernel.dataset import Dataset
from sae.kernel.domain import DrawDate


def test_query_returns_new_query(
    dataset,
) -> None:
    """
    Every query operation returns another DatasetQuery.
    """
    result = dataset.query.by_year(2024)

    assert result is not dataset.query
    assert result.dataset is not dataset


def test_query_chain_returns_expected_dataset(
    dataset,
) -> None:
    """
    Query operations are composable.
    """
    result = (
        dataset.query.by_year(2024)
        .after(
            DrawDate.from_ymd(
                2024,
                1,
                1,
            )
        )
        .dataset
    )

    assert result.draws == (
        dataset.draws[1],
        dataset.draws[2],
    )


def test_query_is_immutable(
    dataset,
) -> None:
    """
    Query operations never modify the original Dataset.
    """
    original = dataset.draws

    _ = dataset.query.by_year(2024).dataset

    assert dataset.draws == original


def test_query_preserves_chronological_order(
    dataset,
) -> None:
    """
    Query results preserve Dataset ordering.
    """
    result = dataset.query.by_year(2024).dataset

    assert tuple(result.draws) == tuple(
        sorted(
            result.draws,
            key=lambda draw: draw.date,
        )
    )


def test_query_empty_result_is_dataset(
    dataset,
) -> None:
    """
    Queries with no matches return an empty Dataset.
    """
    result = dataset.query.by_year(1999).dataset

    assert isinstance(result, Dataset)
    assert result.is_empty
    assert result.size == 0
