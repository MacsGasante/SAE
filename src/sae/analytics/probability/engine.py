from sae.analytics.probability.result import ProbabilityResult
from sae.kernel.dataset import Dataset
from sae.kernel.foundation import Number


class ProbabilityEngine:
    @staticmethod
    def analyze(dataset: Dataset) -> ProbabilityResult:
        probabilities: dict[Number, float] = {
            Number(value): 0.0 for value in range(1, 91)
        }

        if dataset.is_empty:
            return ProbabilityResult(
                draw_count=0,
                probabilities=probabilities,
            )

        occurrences = {Number(value): 0 for value in range(1, 91)}

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
