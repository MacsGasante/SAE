"""End-to-end tests for the dataset-to-reporting pipeline."""

import csv
import io
import json
from pathlib import Path

import pytest

from sae.cli.main import main


def _write_dataset(path: Path) -> None:
    """Write a minimal valid historical dataset for pipeline tests."""
    path.write_text(
        "Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar\n"
        "1,01/01/2005,1,2,3,4,5,6,90,-\n",
        encoding="utf-8",
    )


@pytest.mark.parametrize(
    ("analysis", "expected_title", "expected_value"),
    [
        ("frequency", "Frequency Report", "1"),
        ("delay", "Delay Report", "0"),
        ("probability", "Probability Report", "1.000000"),
    ],
)
@pytest.mark.parametrize("output_format", ["text", "json", "csv"])
def test_report_pipeline_from_csv_to_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    analysis: str,
    expected_title: str,
    expected_value: str,
    output_format: str,
) -> None:
    """Exercise CSV import, analytics, report building, rendering, and CLI."""
    source = tmp_path / "historical-dataset.csv"
    _write_dataset(source)

    assert main(["report", analysis, str(source), "--format", output_format]) == 0

    output = capsys.readouterr().out

    if output_format == "text":
        assert output.startswith(f"{expected_title}\nDraws: 1\n")
        assert f"Number 1: {expected_value}" in output
    elif output_format == "json":
        payload = json.loads(output)
        assert payload["title"] == expected_title
        assert payload["draw_count"] == 1
        assert {"label": "Number 1", "value": expected_value} in payload["rows"]
        assert output.endswith("\n")
    else:
        records = list(csv.DictReader(io.StringIO(output)))
        assert records[0]["title"] == expected_title
        assert records[0]["draw_count"] == "1"
        number_one = next(row for row in records if row["label"] == "Number 1")
        assert number_one["value"] == expected_value

    assert source.read_text(encoding="utf-8").endswith(
        "1,01/01/2005,1,2,3,4,5,6,90,-\n"
    )
