from sae.analytics.probability import ProbabilityEngine, ProbabilityResult


def test_probability_package_exports_public_api() -> None:
    assert "ProbabilityEngine" in __import__(
        "sae.analytics.probability", fromlist=["__all__"]
    ).__all__
    assert "ProbabilityResult" in __import__(
        "sae.analytics.probability", fromlist=["__all__"]
    ).__all__
    assert ProbabilityEngine.__name__ == "ProbabilityEngine"
    assert ProbabilityResult.__name__ == "ProbabilityResult"
