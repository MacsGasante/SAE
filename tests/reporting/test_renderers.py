import csv
import io
import json

from sae.reporting.model import Report, ReportRow
from sae.reporting.renderers import (
    CsvReportRenderer,
    JsonReportRenderer,
    TextReportRenderer,
)


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


def test_json_report_renderer_uses_stable_schema_and_newline() -> None:
    report = Report(
        title="Frequency Report",
        draw_count=2,
        rows=(
            ReportRow(label="Number 1", value="1"),
            ReportRow(label="Numero 2", value="0"),
        ),
    )

    rendered = JsonReportRenderer().render(report)

    assert json.loads(rendered) == {
        "title": "Frequency Report",
        "draw_count": 2,
        "rows": [
            {"label": "Number 1", "value": "1"},
            {"label": "Numero 2", "value": "0"},
        ],
    }
    assert rendered.endswith("\n")
    assert '"Numero 2"' in rendered


def test_json_report_renderer_handles_empty_rows() -> None:
    report = Report(title="Empty Report", draw_count=0, rows=())

    assert json.loads(JsonReportRenderer().render(report)) == {
        "title": "Empty Report",
        "draw_count": 0,
        "rows": [],
    }


def test_csv_report_renderer_uses_stable_columns_and_records() -> None:
    report = Report(
        title="Frequency Report",
        draw_count=2,
        rows=(
            ReportRow(label="Number 1", value="1"),
            ReportRow(label="Number 2", value="0"),
        ),
    )

    rendered = CsvReportRenderer().render(report)
    records = list(csv.reader(io.StringIO(rendered)))

    assert records == [
        ["title", "draw_count", "label", "value"],
        ["Frequency Report", "2", "Number 1", "1"],
        ["Frequency Report", "2", "Number 2", "0"],
    ]
    assert rendered.endswith("\n")


def test_csv_report_renderer_handles_empty_rows_and_metadata() -> None:
    report = Report(title="Empty Report", draw_count=0, rows=())

    records = list(csv.reader(io.StringIO(CsvReportRenderer().render(report))))

    assert records == [
        ["title", "draw_count", "label", "value"],
        ["Empty Report", "0", "", ""],
    ]
