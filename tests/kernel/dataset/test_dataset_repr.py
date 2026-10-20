"""Tests for Dataset's developer representation."""

from sae.kernel.dataset import Dataset


def test_empty_dataset_representation(empty_dataset: Dataset) -> None:
    """An empty Dataset has a concise representation."""
    assert repr(empty_dataset) == "Dataset(size=0)"


def test_non_empty_dataset_representation(dataset: Dataset) -> None:
    """A populated Dataset representation identifies its bounds."""
    assert repr(dataset) == (
        f"Dataset(size={dataset.size}, "
        f"first={dataset.first.id}, "
        f"last={dataset.last.id})"
    )
