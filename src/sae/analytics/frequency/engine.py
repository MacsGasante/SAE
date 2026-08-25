from sae.analytics.frequency.result import FrequencyResult
from sae.kernel.dataset import Dataset
from sae.kernel.foundation import Number


class FrequencyEngine:
    @staticmethod
    def analyze(dataset: Dataset) -> FrequencyResult:
        frequencies = {Number(value): 0 for value in range(1, 91)}

        for draw in dataset:
            for number in draw.numbers:
                frequencies[number] += 1

        return FrequencyResult(
            draw_count=dataset.size,
            frequencies=frequencies,
        )
