"""Compute empirical occurrence counts for each valid SuperEnalotto number."""

from sae.analytics.frequency.result import FrequencyResult
from sae.kernel.dataset import Dataset
from sae.kernel.foundation import MAX_NUMBER, MIN_NUMBER, Number


class FrequencyEngine:
    """Calculate how often each number occurs in a dataset."""

    @staticmethod
    def analyze(dataset: Dataset) -> FrequencyResult:
        """Return occurrence counts for every valid number in the dataset.

        Numbers absent from the dataset have a frequency of zero. The returned
        result includes the number of draws analyzed and an immutable mapping.
        """
        frequencies = {
            Number(value): 0 for value in range(MIN_NUMBER, MAX_NUMBER + 1)
        }

        for draw in dataset:
            for number in draw.numbers:
                frequencies[number] += 1

        return FrequencyResult(
            draw_count=dataset.size,
            frequencies=frequencies,
        )
