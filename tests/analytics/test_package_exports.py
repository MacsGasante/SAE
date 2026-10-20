"""Tests for the public Analytics package APIs."""

from sae.analytics import delay, frequency, probability
from sae.analytics.delay.engine import DelayEngine
from sae.analytics.delay.result import DelayResult
from sae.analytics.frequency.engine import FrequencyEngine
from sae.analytics.frequency.result import FrequencyResult
from sae.analytics.probability.engine import ProbabilityEngine
from sae.analytics.probability.result import ProbabilityResult


def test_frequency_package_exports_public_api() -> None:
    assert frequency.__all__ == ["FrequencyEngine", "FrequencyResult"]
    assert frequency.FrequencyEngine is FrequencyEngine
    assert frequency.FrequencyResult is FrequencyResult


def test_delay_package_exports_public_api() -> None:
    assert delay.__all__ == ["DelayEngine", "DelayResult"]
    assert delay.DelayEngine is DelayEngine
    assert delay.DelayResult is DelayResult


def test_probability_package_exports_public_api() -> None:
    assert probability.__all__ == ["ProbabilityEngine", "ProbabilityResult"]
    assert probability.ProbabilityEngine is ProbabilityEngine
    assert probability.ProbabilityResult is ProbabilityResult
