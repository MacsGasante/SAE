"""
Tests for combination queries.
"""

from __future__ import annotations

import pytest

from sae.kernel.foundation import Number


class TestCombinationQueries:
    def test_intersects_returns_matching_draws(
        self,
        dataset,
        reference_combination,
    ) -> None:
        result = dataset.query.intersects(
            reference_combination,
        ).dataset

        assert result

        for draw in result:
            assert (
                draw.matches(
                    reference_combination,
                ).count
                >= 1
            )

    def test_matches_returns_draws_with_minimum_matches(
        self,
        dataset,
        reference_combination,
    ) -> None:
        result = dataset.query.matches(
            reference_combination,
            at_least=3,
        ).dataset

        for draw in result:
            assert (
                draw.matches(
                    reference_combination,
                ).count
                >= 3
            )

    def test_matches_rejects_zero_threshold(
        self,
        dataset,
        reference_combination,
    ) -> None:
        with pytest.raises(
            ValueError,
            match="between 1 and 6",
        ):
            dataset.query.matches(
                reference_combination,
                at_least=0,
            )

    def test_matches_rejects_negative_threshold(
        self,
        dataset,
        reference_combination,
    ) -> None:
        with pytest.raises(
            ValueError,
            match="between 1 and 6",
        ):
            dataset.query.matches(
                reference_combination,
                at_least=-1,
            )

    def test_matches_rejects_threshold_above_combination_size(
        self,
        dataset,
        reference_combination,
    ) -> None:
        with pytest.raises(
            ValueError,
            match="between 1 and 6",
        ):
            dataset.query.matches(
                reference_combination,
                at_least=7,
            )

    def test_contains_exactly_returns_only_exact_matches(
        self,
        dataset,
        reference_combination,
    ) -> None:
        result = dataset.query.contains_exactly(
            reference_combination,
        ).dataset

        for draw in result:
            assert draw.matches(
                reference_combination,
            ).is_exact

    def test_queries_do_not_modify_original_dataset(
        self,
        dataset,
        reference_combination,
    ) -> None:
        original = tuple(dataset)

        filtered = dataset.query.matches(
            reference_combination,
            at_least=2,
        ).dataset

        assert filtered is not dataset
        assert len(filtered) <= len(dataset)
        assert tuple(dataset) == original

    def test_query_chain(
        self,
        dataset,
        reference_combination,
    ) -> None:
        result = (
            dataset.query.by_year(2024)
            .matches(
                reference_combination,
                at_least=2,
            )
            .dataset
        )

        for draw in result:
            assert draw.date.year == 2024

            assert (
                draw.matches(
                    reference_combination,
                ).count
                >= 2
            )

    def test_intersects_equals_matches_at_least_one(
        self,
        dataset,
        reference_combination,
    ) -> None:
        left = dataset.query.intersects(
            reference_combination,
        ).dataset

        right = dataset.query.matches(
            reference_combination,
            at_least=1,
        ).dataset

        assert tuple(left) == tuple(right)

    def test_matches_at_least_six_equals_contains_exactly(
        self,
        dataset,
        reference_combination,
    ) -> None:
        left = dataset.query.matches(
            reference_combination,
            at_least=6,
        ).dataset

        right = dataset.query.contains_exactly(
            reference_combination,
        ).dataset

        assert tuple(left) == tuple(right)

    def test_contains_and_by_number_are_equivalent(
        self,
        dataset,
    ) -> None:
        number = Number(42)

        left = dataset.query.contains(number).dataset

        right = dataset.query.by_number(number).dataset

        assert tuple(left) == tuple(right)

    def test_impossible_combination_returns_empty_dataset(
        self,
        dataset,
        impossible_combination,
    ) -> None:
        result = dataset.query.contains_exactly(
            impossible_combination,
        ).dataset

        assert result.is_empty

    def test_query_objects_are_independent(
        self,
        dataset,
    ) -> None:
        query = dataset.query

        by_2024 = query.by_year(2024)

        assert by_2024 is not query
        assert by_2024.dataset is not dataset
