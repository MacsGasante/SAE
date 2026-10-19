"""Estimate empirical number inclusion rates from historical draws."""

from sae.analytics.probability.result import ProbabilityResult
from sae.kernel.dataset import Dataset
from sae.kernel.foundation import MAX_NUMBER, MIN_NUMBER, Number


class ProbabilityEngine:
    """Calculate empirical marginal inclusion rates for valid numbers."""

    @staticmethod
    def analyze(dataset: Dataset) -> ProbabilityResult:
        """Return each number's observed frequency per draw in the dataset.

        For a non-empty dataset, the value is the number of draws containing a
        number divided by the total number of draws. An empty dataset produces
        zero for every valid number. These empirical rates describe the
        analyzed data; they are not predictions of future draws.
        """
        if dataset.is_empty:
            return ProbabilityResult(
                draw_count=0,
                probabilities={
                    Number(value): 0.0
                    for value in range(MIN_NUMBER, MAX_NUMBER + 1)
                },
            )

        occurrences = {
            Number(value): 0 for value in range(MIN_NUMBER, MAX_NUMBER + 1)
        }

        for draw in dataset:
            for number in draw.numbers:
                occurrences[number] += 1

        draw_count = dataset.size
        probabilities = {
            number: count / draw_count for number, count in occurrences.items()
        }

        return ProbabilityResult(
            draw_count=draw_count,
            probabilities=probabilities,
        )
