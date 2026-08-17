"""
DatasetQuery facade tests.
"""

from __future__ import annotations

import pytest

from sae.kernel.dataset import Dataset
from sae.kernel.domain import DrawDate, DrawId
from sae.kernel.query import DatasetQuery


def test_dataset_exposes_query(
    dataset,
) -> None:
    """
    Dataset.query returns a DatasetQuery facade bound to the Dataset.
    """
    query = dataset.query

    assert isinstance(query, DatasetQuery)
    assert query.dataset is dataset


def test_query_operation_returns_new_query(
    dataset,
) -> None:
    """
    Query operations return a new DatasetQuery.
    """
    query = dataset.query

    result = query.by_year(2024)

    assert isinstance(result, DatasetQuery)
    assert result is not query
    assert result.dataset is not dataset


def test_query_operations_do_not_modify_original_dataset(
    dataset,
) -> None:
    """
    Query operations never modify the original Dataset.
    """
    original = dataset.draws

    _ = dataset.query.by_year(2024)

    assert dataset.draws is original
    assert dataset.draws == original


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


def test_query_result_preserves_dataset_order(
    dataset,
) -> None:
    """
    Query results preserve chronological Dataset ordering.
    """
    result = dataset.query.by_year(2024).dataset

    assert tuple(result.draws) == tuple(
        sorted(
            result.draws,
            key=lambda draw: draw.date,
        )
    )


def test_query_with_no_matches_returns_empty_dataset(
    dataset,
) -> None:
    """
    A query with no matches returns an empty Dataset.
    """
    result = dataset.query.by_year(1999).dataset

    assert isinstance(result, Dataset)
    assert result.is_empty
    assert result.size == 0


def test_independent_queries_do_not_share_query_state(
    dataset,
) -> None:
    """
    Query operations create independent DatasetQuery objects.
    """
    query = dataset.query

    by_2024 = query.by_year(2024)
    by_2025 = query.by_year(2025)

    assert by_2024 is not by_2025
    assert by_2024.dataset is not by_2025.dataset


def test_by_day_is_exposed_by_query_facade(
    dataset,
) -> None:
    """
    by_day is available through DatasetQuery.
    """
    result = dataset.query.by_day(1).dataset

    assert result
    assert all(draw.date.day == 1 for draw in result)


def test_by_draw_id_is_exposed_by_query_facade(
    dataset,
) -> None:
    """
    by_draw_id is available through DatasetQuery.
    """
    identifier = dataset.first.id

    result = dataset.query.by_draw_id(identifier).dataset

    assert result.draws == (dataset.first,)


def test_by_draw_id_returns_empty_dataset_for_unknown_id(
    dataset,
) -> None:
    """
    by_draw_id returns an empty Dataset for an unknown DrawId.
    """
    result = dataset.query.by_draw_id(
        DrawId(999999),
    ).dataset

    assert result.is_empty


def test_filter_is_alias_of_where(
    dataset,
) -> None:
    """
    filter and where provide equivalent query semantics.
    """

    def predicate(draw) -> bool:
        return draw.date.year == 2024

    filtered = dataset.query.filter(predicate).dataset
    selected = dataset.query.where(predicate).dataset

    assert tuple(filtered) == tuple(selected)


def test_matches_rejects_zero_at_least(
    dataset,
    reference_combination,
) -> None:
    """
    matches rejects at_least=0.
    """
    with pytest.raises(
        ValueError,
        match="between 1 and 6",
    ):
        dataset.query.matches(
            reference_combination,
            at_least=0,
        )


def test_matches_rejects_negative_at_least(
    dataset,
    reference_combination,
) -> None:
    """
    matches rejects negative at_least values.
    """
    with pytest.raises(
        ValueError,
        match="between 1 and 6",
    ):
        dataset.query.matches(
            reference_combination,
            at_least=-1,
        )


def test_matches_rejects_more_than_combination_size(
    dataset,
    reference_combination,
) -> None:
    """
    matches rejects at_least values greater than six.
    """
    with pytest.raises(
        ValueError,
        match="between 1 and 6",
    ):
        dataset.query.matches(
            reference_combination,
            at_least=7,
        )


def test_matches_accepts_one(
    dataset,
    reference_combination,
) -> None:
    """
    matches accepts the minimum valid threshold.
    """
    result = dataset.query.matches(
        reference_combination,
        at_least=1,
    ).dataset

    assert tuple(result) == tuple(
        dataset.query.intersects(
            reference_combination,
        ).dataset
    )


def test_matches_accepts_six(
    dataset,
    reference_combination,
) -> None:
    """
    matches accepts the maximum valid threshold.
    """
    result = dataset.query.matches(
        reference_combination,
        at_least=6,
    ).dataset

    expected = dataset.query.contains_exactly(
        reference_combination,
    ).dataset

    assert tuple(result) == tuple(expected)
