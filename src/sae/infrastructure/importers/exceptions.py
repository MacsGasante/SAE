"""
CSV importer exceptions.

Defines the public exception hierarchy for CSV import failures.
"""

from __future__ import annotations

__all__ = [
    "CSVImportError",
    "CSVFileAccessError",
    "CSVEncodingError",
    "CSVHeaderError",
    "CSVMalformedError",
    "CSVStreamPositionError",
    "CSVEmptyError",
    "CSVFieldError",
    "CSVContestNumberError",
    "CSVDateError",
    "CSVMainNumberError",
    "CSVRepeatedMainNumberError",
    "CSVDuplicateDrawIdError",
    "CSVDuplicateDrawDateError",
    "CSVDatasetValidationError",
]


class CSVImportError(Exception):
    """
    Base class for all CSV importer errors.
    """


class CSVFileAccessError(CSVImportError):
    """
    Raised when the CSV source cannot be accessed.
    """


class CSVEncodingError(CSVImportError):
    """
    Raised when the CSV source cannot be decoded as UTF-8.
    """


class CSVHeaderError(CSVImportError):
    """
    Raised when the CSV header is invalid.
    """


class CSVMalformedError(CSVImportError):
    """
    Raised when the CSV structure is malformed.
    """


class CSVStreamPositionError(CSVImportError):
    """
    Raised when an already-open stream is not positioned at the beginning.
    """


class CSVEmptyError(CSVImportError):
    """
    Raised when the CSV contains no importable data rows.
    """


class CSVFieldError(CSVImportError):
    """
    Base class for invalid CSV field values.
    """


class CSVContestNumberError(CSVFieldError):
    """
    Raised when the contest number is invalid.
    """


class CSVDateError(CSVFieldError):
    """
    Raised when the draw date is invalid.
    """


class CSVMainNumberError(CSVFieldError):
    """
    Raised when a main draw number is invalid.
    """


class CSVRepeatedMainNumberError(CSVFieldError):
    """
    Raised when a main draw number is repeated within a draw.
    """


class CSVDuplicateDrawIdError(CSVImportError):
    """
    Raised when duplicate official draw identity is detected.
    """


class CSVDuplicateDrawDateError(CSVImportError):
    """
    Raised when duplicate draw dates are detected.
    """


class CSVDatasetValidationError(CSVImportError):
    """
    Raised when the final Dataset cannot be constructed.
    """
