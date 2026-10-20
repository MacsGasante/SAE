"""
Tests for CSV importer exceptions.
"""

from sae.infrastructure.importers.exceptions import (
    CSVContestNumberError,
    CSVDatasetValidationError,
    CSVDateError,
    CSVDuplicateDrawDateError,
    CSVDuplicateDrawIdError,
    CSVEmptyError,
    CSVEncodingError,
    CSVFieldError,
    CSVFileAccessError,
    CSVHeaderError,
    CSVImportError,
    CSVJollyError,
    CSVMainNumberError,
    CSVMalformedError,
    CSVRepeatedMainNumberError,
    CSVStreamPositionError,
    CSVSuperstarError,
)

from sae.kernel import SAEError


def test_csv_import_error_derives_from_sae_error() -> None:
    assert issubclass(CSVImportError, SAEError)


def test_all_importer_exceptions_derive_from_csv_import_error() -> None:
    exception_types = (
        CSVFileAccessError,
        CSVEncodingError,
        CSVHeaderError,
        CSVMalformedError,
        CSVStreamPositionError,
        CSVEmptyError,
        CSVFieldError,
        CSVDuplicateDrawIdError,
        CSVDuplicateDrawDateError,
        CSVDatasetValidationError,
    )

    for exception_type in exception_types:
        assert issubclass(exception_type, CSVImportError)


def test_field_exceptions_derive_from_csv_field_error() -> None:
    field_exception_types = (
        CSVContestNumberError,
        CSVDateError,
        CSVMainNumberError,
        CSVRepeatedMainNumberError,
        CSVJollyError,
        CSVSuperstarError,
    )

    for exception_type in field_exception_types:
        assert issubclass(exception_type, CSVFieldError)
        assert issubclass(exception_type, CSVImportError)


def test_csv_import_error_preserves_message() -> None:
    error = CSVImportError("test error")

    assert str(error) == "test error"


def test_specific_exception_can_preserve_cause() -> None:
    cause = ValueError("underlying error")

    try:
        raise cause
    except ValueError as exc:
        error = CSVDateError("invalid date")
        error.__cause__ = exc

    assert str(error) == "invalid date"
    assert error.__cause__ is cause
