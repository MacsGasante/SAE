from sae import __version__
from sae.cli.main import main


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
    source.write_text(
        "Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar\n"
        "1,01/01/2005,1,2,3,4,5,6,90,-\n",
        encoding="utf-8",
    )

    assert main(["report", "frequency", str(source)]) == 0

    output = capsys.readouterr().out

    assert output.startswith("Frequency Report\nDraws: 1\n")
    assert "Number 1: 1" in output
    assert "Number 7: 0" in output
    assert "Number 90: 0" in output


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


def test_main_unknown_command_exits_with_error() -> None:
    try:
        main(["unknown"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected unknown command to exit with error")
