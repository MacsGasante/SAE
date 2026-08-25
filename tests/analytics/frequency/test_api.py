from sae.analytics.frequency import FrequencyEngine, FrequencyResult


def test_public_api_exports_frequency_components() -> None:
    assert FrequencyEngine is not None
    assert FrequencyResult is not None
