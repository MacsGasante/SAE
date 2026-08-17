"""
Dataset Layer.

The Dataset Layer provides the Aggregate Root representing
the complete immutable historical archive of SuperEnalotto draws.
"""

from .dataset import Dataset
from .exceptions import InvalidDatasetError

__all__ = [
    "Dataset",
    "InvalidDatasetError",
]
