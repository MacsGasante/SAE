"""Presentation-neutral report models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportRow:
    """One labelled value in a report."""

    label: str
    value: str


@dataclass(frozen=True)
class Report:
    """Immutable presentation-neutral report data."""

    title: str
    draw_count: int
    rows: tuple[ReportRow, ...]
