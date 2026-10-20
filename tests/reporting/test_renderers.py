from sae.reporting.model import Report, ReportRow
from sae.reporting.renderers import TextReportRenderer


def test_text_report_renderer_uses_stable_line_format() -> None:
    report = Report(
        title="Frequency Report",
        draw_count=42,
        rows=(
            ReportRow(label="Number 1", value="7"),
            ReportRow(label="Number 2", value="5"),
        ),
    )

    assert TextReportRenderer().render(report) == (
        "Frequency Report\nDraws: 42\nNumber 1: 7\nNumber 2: 5"
    )


def test_text_report_renderer_handles_empty_rows() -> None:
    report = Report(title="Empty Report", draw_count=0, rows=())

    assert TextReportRenderer().render(report) == "Empty Report\nDraws: 0"
