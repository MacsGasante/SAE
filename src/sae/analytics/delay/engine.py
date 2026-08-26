from sae.analytics.delay.result import DelayResult
from sae.kernel.dataset import Dataset
from sae.kernel.foundation import Number


class DelayEngine:
    @staticmethod
    def analyze(dataset: Dataset) -> DelayResult:
        delays: dict[Number, int | None] = {
            Number(value): None for value in range(1, 91)
        }

        for delay, draw in enumerate(reversed(dataset.draws)):
            for number in draw.numbers:
                if delays[number] is None:
                    delays[number] = delay

        return DelayResult(
            draw_count=dataset.size,
            delays=delays,
        )
