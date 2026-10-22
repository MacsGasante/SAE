"""Monte Carlo goodness-of-fit test for historical marginal frequencies."""

from __future__ import annotations

import hashlib
import json
import math
import random
from collections.abc import Mapping

from sae.analytics.frequency.engine import FrequencyEngine
from sae.kernel.dataset import Dataset
from sae.kernel.foundation import Number
from sae.kernel.foundation.constants import MAX_NUMBER, MIN_NUMBER

from .experiment import Experiment
from .result import ResearchProvenance, ResearchResult


def dataset_fingerprint(dataset: Dataset) -> str:
    """Return the documented SHA-256 fingerprint of ordered Dataset content."""
    if not isinstance(dataset, Dataset):
        raise TypeError("dataset must be a Dataset.")

    canonical = [
        [
            draw.id.to_int(),
            draw.date.isoformat(),
            [number.value for number in draw.numbers],
        ]
        for draw in dataset
    ]
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class HistoricalFrequencyNullModel:
    """Compare historical frequencies with independent uniform six-of-90 draws.

    The primary statistic is the maximum absolute standardized deviation over
    all 90 marginal number frequencies. Its null distribution is estimated by
    simulating complete six-distinct-number draws. The result is evidence about
    the supplied historical Dataset only, not a prediction.
    """

    _MODULE_ID = "sae.research.historical-frequency-null-model"
    _MODULE_VERSION = "1.0.0"
    _NUMBER_DOMAIN = tuple(range(MIN_NUMBER, MAX_NUMBER + 1))
    _NUMBERS_PER_DRAW = 6
    _DEFAULT_REPLICATE_COUNT = 999

    @property
    def module_id(self) -> str:
        """Return this module's stable identifier."""
        return self._MODULE_ID

    @property
    def module_version(self) -> str:
        """Return this module's stable version."""
        return self._MODULE_VERSION

    def execute(self, input_data: object, experiment: Experiment) -> ResearchResult:
        """Run the pre-specified frequency-profile test on a historical Dataset."""
        if not isinstance(input_data, Dataset):
            raise TypeError("HistoricalFrequencyNullModel input_data must be a Dataset.")
        if input_data.is_empty:
            raise ValueError("HistoricalFrequencyNullModel requires a non-empty Dataset.")
        if not isinstance(experiment, Experiment):
            raise TypeError("experiment must be an Experiment.")
        if experiment.module_id != self.module_id:
            raise ValueError("Experiment module_id does not match this module.")
        if experiment.module_version != self.module_version:
            raise ValueError("Experiment module_version does not match this module.")

        fingerprint = dataset_fingerprint(input_data)
        if experiment.input_fingerprint != fingerprint:
            raise ValueError("Experiment input_fingerprint does not match the Dataset.")

        replicate_count = self._read_replicate_count(experiment.configuration.values)
        seed = experiment.execution_context.random_seed
        if seed is None:
            raise ValueError("Historical frequency test requires an explicit random_seed.")

        draw_count = input_data.size
        observed_result = FrequencyEngine.analyze(input_data)
        observed_frequencies = {
            number.value: observed_result.frequency(number)
            for number in (Number(value) for value in self._NUMBER_DOMAIN)
        }
        observed_statistic = self._statistic(observed_frequencies, draw_count)

        generator = random.Random(seed)
        exceedance_count = 0
        for _ in range(replicate_count):
            simulated_frequencies = dict.fromkeys(self._NUMBER_DOMAIN, 0)
            for _ in range(draw_count):
                for number in generator.sample(self._NUMBER_DOMAIN, self._NUMBERS_PER_DRAW):
                    simulated_frequencies[number] += 1
            simulated_statistic = self._statistic(simulated_frequencies, draw_count)
            if simulated_statistic >= observed_statistic:
                exceedance_count += 1

        p_value = (exceedance_count + 1) / (replicate_count + 1)
        expected_frequency = draw_count * self._NUMBERS_PER_DRAW / MAX_NUMBER
        standard_deviation = math.sqrt(
            draw_count
            * (self._NUMBERS_PER_DRAW / MAX_NUMBER)
            * (1 - self._NUMBERS_PER_DRAW / MAX_NUMBER)
        )
        payload = {
            "draw_count": draw_count,
            "number_domain_min": MIN_NUMBER,
            "number_domain_max": MAX_NUMBER,
            "numbers_per_draw": self._NUMBERS_PER_DRAW,
            "expected_frequency_per_number": expected_frequency,
            "frequency_standard_deviation": standard_deviation,
            "number_frequencies": {
                str(number): observed_frequencies[number]
                for number in self._NUMBER_DOMAIN
            },
            "observed_max_absolute_standardized_deviation": observed_statistic,
            "replicate_count": replicate_count,
            "exceedance_count": exceedance_count,
            "monte_carlo_p_value": p_value,
            "p_value_method": "(exceedance_count + 1) / (replicate_count + 1)",
            "interpretation": (
                "Monte Carlo estimate for the marginal frequency profile under "
                "the independent uniform six-of-90 null model; not a prediction."
            ),
        }
        return ResearchResult(
            provenance=ResearchProvenance.from_experiment(experiment),
            payload=payload,
            execution_metadata={
                "algorithm": "python.random.Random.sample",
                "random_seed": seed,
                "dataset_fingerprint": fingerprint,
                "statistic": "maximum absolute standardized marginal-frequency deviation",
                "null_model": "independent uniform draws of six distinct numbers from 1..90",
            },
        )

    @staticmethod
    def _statistic(frequencies: Mapping[int, int], draw_count: int) -> float:
        """Compute the pre-specified maximum absolute standardized deviation."""
        probability = 6 / MAX_NUMBER
        standard_deviation = math.sqrt(draw_count * probability * (1 - probability))
        expected = draw_count * probability
        return max(
            abs((frequencies[number] - expected) / standard_deviation)
            for number in range(MIN_NUMBER, MAX_NUMBER + 1)
        )

    @classmethod
    def _read_replicate_count(cls, configuration: Mapping[str, object]) -> int:
        """Validate the number of null-model Monte Carlo replicates."""
        value = configuration.get("replicate_count", cls._DEFAULT_REPLICATE_COUNT)
        if type(value) is not int or value < 1:
            raise ValueError("configuration replicate_count must be a positive integer.")
        return value
