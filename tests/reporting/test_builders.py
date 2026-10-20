from sae.analytics.delay.result import DelayResult
from sae.analytics.frequency.result import FrequencyResult
from sae.analytics.probability.result import ProbabilityResult
from sae.kernel.foundation import Number
from sae.reporting.builders import (
    build_delay_report,
    build_frequency_report,
    build_probability_report,
)


def test_build_frequency_report_orders_numbers() -> None:
    result = FrequencyResult(
        draw_count=3,
        frequencies={Number(2): 5, Number(1): 7},
    )

    report = build_frequency_report(result)

    assert report.title == "Frequency Report"
    assert report.draw_count == 3
    assert report.rows[0].label == "Number 1"
    assert report.rows[0].value == "7"
    assert report.rows[1].label == "Number 2"
    assert report.rows[1].value == "5"


def test_build_delay_report_renders_missing_numbers_as_never() -> None:
    result = DelayResult(
        draw_count=3,
        delays={Number(2): 1, Number(1): None},
    )

    report = build_delay_report(result)

    assert report.title == "Delay Report"
    assert report.rows[0].value == "Never"
    assert report.rows[1].value == "1"


def test_build_probability_report_formats_rates() -> None:
    result = ProbabilityResult(
        draw_count=4,
        probabilities={Number(2): 0.25, Number(1): 0.125},
    )

    report = build_probability_report(result)

    assert report.title == "Probability Report"
    assert report.rows[0].value == "0.125000"
    assert report.rows[1].value == "0.250000"
