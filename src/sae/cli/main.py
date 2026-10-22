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
from sae.research import (
    ExecutionContext,
    Experiment,
    ExperimentConfiguration,
    HistoricalFrequencyNullModel,
    MonteCarloDrawSimulation,
    dataset_fingerprint,
    execute_research_module,
)
from sae.research_reporting import (
    CsvResearchReportRenderer,
    JsonResearchReportRenderer,
    TextResearchReportRenderer,
    build_research_report,
)


def _non_negative_int(value: str) -> int:
    """Parse a non-negative integer CLI argument."""
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
    return parsed


def _positive_int(value: str) -> int:
    """Parse a positive integer CLI argument."""
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def _existing_file(value: str) -> Path:
    """Return an existing regular file path or raise an argparse error."""
    path = Path(value)

    if not path.is_file():
        message = f"file does not exist or is not a file: {value!r}"
        raise argparse.ArgumentTypeError(message)

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

    research_parser = subparsers.add_parser(
        "research",
        help="Run reproducible research experiments.",
    )
    research_subparsers = research_parser.add_subparsers(dest="research_command")
    simulate_parser = research_subparsers.add_parser(
        "simulate",
        help="Run a seeded Monte Carlo simulation of independent draws.",
    )
    simulate_parser.add_argument(
        "--seed",
        type=_non_negative_int,
        required=True,
        help="Explicit non-negative random seed for reproducibility.",
    )
    simulate_parser.add_argument(
        "--draw-count",
        type=_positive_int,
        default=10_000,
        help="Number of simulated draws (default: 10000).",
    )
    historical_parser = research_subparsers.add_parser(
        "historical-test",
        help="Compare historical frequencies with the uniform six-of-90 null model.",
    )
    historical_parser.add_argument(
        "input",
        type=_existing_file,
        help="Path to the official SuperEnalotto CSV dataset.",
    )
    historical_parser.add_argument(
        "--seed",
        type=_non_negative_int,
        required=True,
        help="Explicit non-negative random seed for reproducibility.",
    )
    historical_parser.add_argument(
        "--replicate-count",
        type=_positive_int,
        required=True,
        help="Number of Monte Carlo null-model replicates; required explicitly.",
    )
    historical_parser.add_argument(
        "--format",
        choices=("text", "json", "csv"),
        default="text",
        help="Output format (default: text).",
    )

    simulate_parser.add_argument(
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


def _run_research_simulation(seed: int, draw_count: int, output_format: str) -> None:
    """Execute and render a reproducible Monte Carlo research experiment."""
    if seed < 0:
        raise ValueError("seed must be a non-negative integer.")
    if draw_count < 1:
        raise ValueError("draw-count must be a positive integer.")

    module = MonteCarloDrawSimulation()
    experiment = Experiment(
        experiment_id=f"monte-carlo-seed-{seed}-draws-{draw_count}",
        module_id=module.module_id,
        module_version=module.module_version,
        input_fingerprint="theoretical-independent-six-of-90-v1",
        configuration=ExperimentConfiguration({"draw_count": draw_count}),
        execution_context=ExecutionContext(random_seed=seed),
    )
    result = execute_research_module(module, None, experiment)
    report = build_research_report(result)

    renderer: (
        TextResearchReportRenderer
        | JsonResearchReportRenderer
        | CsvResearchReportRenderer
    )
    if output_format == "text":
        renderer = TextResearchReportRenderer()
    elif output_format == "json":
        renderer = JsonResearchReportRenderer()
    else:
        renderer = CsvResearchReportRenderer()

    print(renderer.render(report), end="")


def _run_historical_test(
    input_path: Path,
    seed: int,
    replicate_count: int,
    output_format: str,
) -> None:
    """Run the historical frequency null-model test and render its report."""
    dataset = CSVImporter.import_dataset(input_path)
    module = HistoricalFrequencyNullModel()
    fingerprint = dataset_fingerprint(dataset)
    experiment = Experiment(
        experiment_id=(
            f"historical-frequency-null-seed-{seed}-"
            f"replicates-{replicate_count}-{fingerprint[:12]}"
        ),
        module_id=module.module_id,
        module_version=module.module_version,
        input_fingerprint=fingerprint,
        configuration=ExperimentConfiguration(
            {"replicate_count": replicate_count}
        ),
        execution_context=ExecutionContext(random_seed=seed),
    )
    result = execute_research_module(module, dataset, experiment)
    report = build_research_report(result)

    renderer: (
        TextResearchReportRenderer
        | JsonResearchReportRenderer
        | CsvResearchReportRenderer
    )
    if output_format == "text":
        renderer = TextResearchReportRenderer()
    elif output_format == "json":
        renderer = JsonResearchReportRenderer()
    else:
        renderer = CsvResearchReportRenderer()

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
    elif args.command == "research" and args.research_command == "simulate":
        _run_research_simulation(args.seed, args.draw_count, args.format)
    elif args.command == "research" and args.research_command == "historical-test":
        _run_historical_test(
            args.input, args.seed, args.replicate_count, args.format
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
