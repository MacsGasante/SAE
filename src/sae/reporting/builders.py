"""Build presentation-neutral reports from analytics results."""

from sae.analytics.delay.result import DelayResult
from sae.analytics.frequency.result import FrequencyResult
from sae.analytics.probability.result import ProbabilityResult
from sae.kernel.foundation import Number
from sae.reporting.model import Report, ReportRow


def build_frequency_report(result: FrequencyResult) -> Report:
    """Build a report from a frequency analysis result."""
    rows = tuple(
        ReportRow(label=f"Number {number.value}", value=str(result.frequency(number)))
        for number in _valid_numbers(result.frequencies)
    )
    return Report(title="Frequency Report", draw_count=result.draw_count, rows=rows)


def build_delay_report(result: DelayResult) -> Report:
    """Build a report from a delay analysis result."""
    rows = tuple(
        ReportRow(
            label=f"Number {number.value}",
            value="Never" if result.delay(number) is None else str(result.delay(number)),
        )
        for number in _valid_numbers(result.delays)
    )
    return Report(title="Delay Report", draw_count=result.draw_count, rows=rows)


def build_probability_report(result: ProbabilityResult) -> Report:
    """Build a report from a probability analysis result."""
    rows = tuple(
        ReportRow(
            label=f"Number {number.value}",
            value=f"{result.probability(number):.6f}",
        )
        for number in _valid_numbers(result.probabilities)
    )
    return Report(title="Probability Report", draw_count=result.draw_count, rows=rows)


def _valid_numbers(mapping: object) -> tuple[Number, ...]:
    """Return the valid number keys in numeric order."""
    if not hasattr(mapping, "keys"):
        raise TypeError("Analytics result must expose a number mapping.")

    return tuple(sorted(mapping.keys(), key=lambda number: number.value))  # type: ignore[union-attr]
