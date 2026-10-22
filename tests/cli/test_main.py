import csv
import io
import json
from pathlib import Path

import pytest

from sae import __version__
from sae.cli.main import main


def _write_dataset(path: Path) -> None:
    path.write_text(
        "Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar\n"
        "1,01/01/2005,1,2,3,4,5,6,90,-\n",
        encoding="utf-8",
    )


def test_main_without_arguments_returns_zero() -> None:
    assert main([]) == 0


def test_main_version_returns_zero(capsys) -> None:
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("Expected --version to exit")

    captured = capsys.readouterr()

    assert captured.out == f"sae {__version__}\n"


def test_main_info_returns_zero(capsys) -> None:
    assert main(["info"]) == 0

    captured = capsys.readouterr()

    assert "SAE — SuperEnalotto Analytics Engine" in captured.out
    assert f"Version: {__version__}" in captured.out
    assert "Status: Pre-Alpha" in captured.out
    assert "Analytics: Frequency, Delay, Probability" in captured.out


def test_main_report_frequency_imports_analyzes_and_renders(tmp_path, capsys) -> None:
    source = tmp_path / "dataset.csv"
    _write_dataset(source)

    assert main(["report", "frequency", str(source)]) == 0

    output = capsys.readouterr().out

    assert output.startswith("Frequency Report\nDraws: 1\n")
    assert "Number 1: 1" in output
    assert "Number 7: 0" in output
    assert "Number 90: 0" in output


def test_main_report_delay_renders_selected_analysis(tmp_path, capsys) -> None:
    source = tmp_path / "dataset.csv"
    _write_dataset(source)

    assert main(["report", "delay", str(source)]) == 0

    output = capsys.readouterr().out

    assert output.startswith("Delay Report\nDraws: 1\n")
    assert "Number 1: 0" in output
    assert "Number 7: Never" in output


def test_main_report_probability_renders_selected_analysis(tmp_path, capsys) -> None:
    source = tmp_path / "dataset.csv"
    _write_dataset(source)

    assert main(["report", "probability", str(source)]) == 0

    output = capsys.readouterr().out

    assert output.startswith("Probability Report\nDraws: 1\n")
    assert "Number 1: 1.000000" in output
    assert "Number 7: 0.000000" in output


def test_main_report_rejects_missing_input_file(tmp_path, capsys) -> None:
    missing = tmp_path / "missing.csv"

    with pytest.raises(SystemExit) as exc_info:
        main(["report", "probability", str(missing)])

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert f"file does not exist or is not a file: '{missing}'" in captured.err
    assert "Traceback" not in captured.err


def test_main_report_rejects_directory_as_input(tmp_path, capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["report", "probability", str(tmp_path)])

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "file does not exist or is not a file" in captured.err
    assert "Traceback" not in captured.err


def test_main_report_json_renders_selected_format(tmp_path, capsys) -> None:
    source = tmp_path / "dataset.csv"
    _write_dataset(source)

    assert main(["report", "frequency", str(source), "--format", "json"]) == 0

    output = capsys.readouterr().out
    payload = json.loads(output)

    assert payload["title"] == "Frequency Report"
    assert payload["draw_count"] == 1
    assert payload["rows"][0] == {"label": "Number 1", "value": "1"}
    assert output.endswith("\n")


def test_main_report_csv_renders_selected_format(tmp_path, capsys) -> None:
    source = tmp_path / "dataset.csv"
    _write_dataset(source)

    assert main(["report", "delay", str(source), "--format", "csv"]) == 0

    records = list(csv.reader(io.StringIO(capsys.readouterr().out)))

    assert records[0] == ["title", "draw_count", "label", "value"]
    assert records[1] == ["Delay Report", "1", "Number 1", "0"]
    assert records[7] == ["Delay Report", "1", "Number 7", "Never"]


def test_main_help_returns_zero(capsys) -> None:
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("Expected --help to exit")

    captured = capsys.readouterr()

    assert "usage:" in captured.out
    assert "--version" in captured.out
    assert "info" in captured.out
    assert "report" in captured.out


def test_main_report_help_lists_supported_formats(capsys) -> None:
    try:
        main(["report", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("Expected report --help to exit")

    captured = capsys.readouterr()

    assert "--format" in captured.out
    assert "text" in captured.out
    assert "json" in captured.out
    assert "csv" in captured.out


def test_main_unknown_command_exits_with_error() -> None:
    try:
        main(["unknown"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected unknown command to exit with error")


@pytest.mark.parametrize("output_format", ["text", "json", "csv"])
def test_research_simulate_renders_all_supported_formats(
    output_format: str, capsys
) -> None:
    assert main(
        [
            "research",
            "simulate",
            "--seed",
            "17",
            "--draw-count",
            "25",
            "--format",
            output_format,
        ]
    ) == 0

    output = capsys.readouterr().out
    assert output

    if output_format == "json":
        data = json.loads(output)
        assert data["provenance"]["execution_context"]["random_seed"] == 17
        assert data["provenance"]["configuration"]["draw_count"] == 25
        assert data["payload"]["draw_count"] == 25
        assert data["execution_metadata"]["random_seed"] == 17
    elif output_format == "csv":
        records = list(csv.reader(io.StringIO(output)))
        assert records[0] == ["section", "key", "value"]
        assert [
            "provenance",
            "experiment_id",
            "monte-carlo-seed-17-draws-25",
        ] in records
        assert [
            "provenance",
            "execution_context",
            '{"random_seed":17}',
        ] in records
        assert ["payload", "draw_count", "25"] in records
        assert ["execution_metadata", "random_seed", "17"] in records
    else:
        assert output.startswith(
            "Research Report — sae.research.monte-carlo-draw-simulation"
        )
        assert "Provenance:" in output
        assert "Execution metadata:" in output
        assert "Payload:" in output
        assert '"random_seed": 17' in output


def test_research_simulate_requires_explicit_seed() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["research", "simulate", "--draw-count", "10"])

    assert exc_info.value.code == 2


@pytest.mark.parametrize(
    ("arguments", "expected_message"),
    [
        (["--seed", "-1"], "must be non-negative"),
        (["--seed", "1", "--draw-count", "0"], "must be positive"),
        (["--seed", "invalid"], "must be an integer"),
    ],
)
def test_research_simulate_rejects_invalid_numeric_arguments(
    arguments: list[str], expected_message: str, capsys
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["research", "simulate", *arguments])

    assert exc_info.value.code == 2
    assert expected_message in capsys.readouterr().err
