import sae.analytics.probability as probability
from sae.analytics.probability import ProbabilityEngine, ProbabilityResult


def test_probability_package_exports_public_api() -> None:
    assert probability.__all__ == [
        "ProbabilityEngine",
        "ProbabilityResult",
    ]
    assert probability.ProbabilityEngine is ProbabilityEngine
    assert probability.ProbabilityResult is ProbabilityResult
