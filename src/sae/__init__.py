"""
SAE - SuperEnalotto Analytics Engine.

Root package.

SAE provides a scientific framework for analysing historical
SuperEnalotto draws through a clean, testable and extensible
architecture.

The Kernel is intentionally designed to remain independent from
external libraries whenever possible.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sae")
except PackageNotFoundError:
    # Package not installed yet (development environment).
    __version__ = "0.0.0"
