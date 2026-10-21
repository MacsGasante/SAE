"""Seeded Monte Carlo simulation of independent SuperEnalotto-style draws."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Mapping

from .experiment import Experiment
from .result import ResearchProvenance, ResearchResult


class MonteCarloDrawSimulation:
    """Simulate independent draws of six distinct numbers from 1 through 90.

    This module is a methodological research tool. Its output describes the
    simulated sample only; it is not a prediction of future official draws.
    The input_data argument must be None because the simulation is self-contained.
    """

    _MODULE_ID = "sae.research.monte-carlo-draw-simulation"
    _MODULE_VERSION = "1.0.0"
    _NUMBER_DOMAIN_MAX = 90
    _NUMBERS_PER_DRAW = 6
    _DEFAULT_DRAW_COUNT = 10_000

    @property
    def module_id(self) -> str:
        """Return this module's stable identifier."""
        return self._MODULE_ID

    @property
    def module_version(self) -> str:
        """Return this module's stable version."""
        return self._MODULE_VERSION

    def execute(self, input_data: object, experiment: Experiment) -> ResearchResult:
        """Run the simulation with explicit configuration and random seed."""
        if input_data is not None:
            raise TypeError("MonteCarloDrawSimulation input_data must be None.")
        if not isinstance(experiment, Experiment):
            raise TypeError("experiment must be an Experiment.")
        if experiment.module_id != self.module_id:
            raise ValueError("Experiment module_id does not match this module.")
        if experiment.module_version != self.module_version:
            raise ValueError("Experiment module_version does not match this module.")

        draw_count = self._read_draw_count(experiment.configuration.values)
        seed = experiment.execution_context.random_seed
        if seed is None:
            raise ValueError("Monte Carlo simulation requires an explicit random_seed.")

        generator = random.Random(seed)
        frequencies = [0] * self._NUMBER_DOMAIN_MAX
        for _ in range(draw_count):
            for number in generator.sample(
                range(1, self._NUMBER_DOMAIN_MAX + 1),
                self._NUMBERS_PER_DRAW,
            ):
                frequencies[number - 1] += 1

        distribution = Counter(frequencies)
        payload = {
            "draw_count": draw_count,
            "number_domain_max": self._NUMBER_DOMAIN_MAX,
            "numbers_per_draw": self._NUMBERS_PER_DRAW,
            "number_frequencies": {
                str(number): frequencies[number - 1]
                for number in range(1, self._NUMBER_DOMAIN_MAX + 1)
            },
            "frequency_distribution": {
                str(occurrences): distribution[occurrences]
                for occurrences in sorted(distribution)
            },
        }
        return ResearchResult(
            provenance=ResearchProvenance.from_experiment(experiment),
            payload=payload,
            execution_metadata={
                "algorithm": "python.random.Random.sample",
                "random_seed": seed,
            },
        )

    @classmethod
    def _read_draw_count(cls, configuration: Mapping[str, object]) -> int:
        """Validate the module-specific number of simulated draws."""
        value = configuration.get("draw_count", cls._DEFAULT_DRAW_COUNT)
        if type(value) is not int or value < 1:
            raise ValueError("configuration draw_count must be a positive integer.")
        return value
