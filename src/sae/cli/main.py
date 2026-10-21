"""SAE command-line interface."""

import argparse
from collections.abc import Sequence
from pathlib import Path

from sae import __version__
from sae.analytics.delay.engine import DelayEngine
from sae.analytics.frequency.engine import FrequencyEngine
from sae.analytics.probability.engine import ProbabilityEngine
from sae.infrastructure.importers.csv_importer import CSVImporter
from sae.reporting import (
    CsvReportRenderer,
    JsonReportRenderer,
    TextReportRenderer,
    build_delay_report,
    build_frequency_report,
    build_probability_report,
)


def _existing_file(value: str) -> Path:
    """Return an existing regular file path or raise an argparse error."""
    path = Path(value)

    if not path.is_file():
        raise argparse.ArgumentTypeError(f"file does not exist or is not a file: {value!r}")

    return path


def build_parser() -> argparse.ArgumentParser:
    """Build the SAE command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="sae",
        description="SuperEnalotto Analytics Engine.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "info",
        help="Show basic information about SAE.",
    )

    report_parser = subparsers.add_parser(
        "report",
        help="Generate an analytics report from a CSV dataset.",
    )
    report_parser.add_argument(
        "analysis",
        choices=("frequency", "delay", "probability"),
        help="Analytics result to report.",
    )
    report_parser.add_argument(
        "input",
        type=_existing_file,
        help="Path to the official SuperEnalotto CSV dataset.",
    )
    report_parser.add_argument(
        "--format",
        choices=("text", "json", "csv"),
        default="text",
        help="Output format (default: text).",
    )

    return parser


def _run_report(analysis: str, input_path: Path, output_format: str) -> None:
    """Import a dataset, run the selected analysis, and render its report."""
    dataset = CSVImporter.import_dataset(input_path)

    if analysis == "frequency":
        report = build_frequency_report(FrequencyEngine.analyze(dataset))
    elif analysis == "delay":
        report = build_delay_report(DelayEngine.analyze(dataset))
    else:
        report = build_probability_report(ProbabilityEngine.analyze(dataset))

    renderer: TextReportRenderer | JsonReportRenderer | CsvReportRenderer
    if output_format == "text":
        renderer = TextReportRenderer()
    elif output_format == "json":
        renderer = JsonReportRenderer()
    else:
        renderer = CsvReportRenderer()

    print(renderer.render(report), end="")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the SAE command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "info":
        print("SAE — SuperEnalotto Analytics Engine")
        print(f"Version: {__version__}")
        print("Status: Pre-Alpha")
        print("Analytics: Frequency, Delay, Probability")
    elif args.command == "report":
        _run_report(args.analysis, args.input, args.format)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
