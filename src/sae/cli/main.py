"""SAE command-line interface."""

import argparse
from collections.abc import Sequence

from sae import __version__


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

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the SAE command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "info":
        print("SAE — SuperEnalotto Analytics Engine")
        print(f"Version: {__version__}")
        print("Status: Pre-Alpha")
        print("Analytics: Frequency, Delay, Probability")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
