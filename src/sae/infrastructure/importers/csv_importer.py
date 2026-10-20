"""
CSV importer for the official SuperEnalotto historical dataset.
"""

from __future__ import annotations

import csv
import re
from datetime import date, datetime
from pathlib import Path
from typing import TextIO

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
    CSVJollyError,
    CSVMainNumberError,
    CSVMalformedError,
    CSVRepeatedMainNumberError,
    CSVStreamPositionError,
    CSVSuperstarError,
)
from sae.kernel import Combination, Draw, DrawDate, DrawId, InvalidNumberError, Number
from sae.kernel.foundation.constants import MAX_NUMBER, MIN_NUMBER
from sae.kernel.dataset import Dataset, InvalidDatasetError
from sae.kernel.domain.exceptions import (
    InvalidDrawDateError,
    InvalidDrawError,
    InvalidDrawIdError,
)

EXPECTED_HEADER = (
    "Concorso",
    "Data",
    "N1",
    "N2",
    "N3",
    "N4",
    "N5",
    "N6",
    "Jolly",
    "Superstar",
)

FIELD_NAMES = (
    "Concorso",
    "Data",
    "N1",
    "N2",
    "N3",
    "N4",
    "N5",
    "N6",
    "Jolly",
    "Superstar",
)

INTEGER_PATTERN = re.compile(r"[0-9]+")
DATE_PATTERN = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{4}")
SUPERSTAR_INTRODUCTION_DATE = date(2006, 3, 28)
MAX_CONTEST_NUMBER = 999


class CSVImporter:
    """
    Import the official SuperEnalotto CSV dataset.
    """

    @staticmethod
    def import_dataset(
        source: str | Path | TextIO,
    ) -> Dataset:
        """
        Import a Dataset from a filesystem path or an open text stream.

        Filesystem sources are opened and closed by the importer.
        Caller-owned streams are never closed by the importer.
        """
        if isinstance(source, (str, Path)):
            return CSVImporter._import_path(source)

        return CSVImporter._import_stream(source)

    @staticmethod
    def _import_path(
        source: str | Path,
    ) -> Dataset:
        """
        Open a filesystem source and delegate to stream import.
        """
        try:
            with Path(source).open(
                mode="r",
                encoding="utf-8-sig",
                newline="",
            ) as stream:
                return CSVImporter._import_stream(stream)
        except UnicodeDecodeError as exc:
            raise CSVEncodingError(
                f"CSV source is not valid UTF-8: {source!s}."
            ) from exc
        except OSError as exc:
            raise CSVFileAccessError(
                f"CSV source could not be accessed: {source!s}."
            ) from exc

    @staticmethod
    def _import_stream(
        stream: TextIO,
    ) -> Dataset:
        """
        Import a Dataset from a caller-owned text stream.

        The stream must be readable and positioned at the beginning.
        It is not rewound or closed by the importer.
        """
        readable = getattr(stream, "readable", None)

        if not callable(readable):
            raise CSVMalformedError("CSV source must be a readable text stream.")

        try:
            if not readable():
                raise CSVMalformedError("CSV source must be a readable text stream.")
        except OSError as exc:
            raise CSVFileAccessError(
                "CSV stream readability could not be determined."
            ) from exc

        try:
            position = stream.tell()
        except (OSError, ValueError, AttributeError) as exc:
            raise CSVStreamPositionError(
                "CSV stream position could not be determined."
            ) from exc

        if position != 0:
            raise CSVStreamPositionError(
                "CSV stream must be positioned at the beginning."
            )

        try:
            return CSVImporter._parse_stream(stream)
        except UnicodeDecodeError as exc:
            raise CSVEncodingError(
                "CSV stream contains data that cannot be decoded as UTF-8."
            ) from exc
        except csv.Error as exc:
            raise CSVMalformedError(f"Malformed CSV structure: {exc}") from exc
        except OSError as exc:
            raise CSVFileAccessError(
                "An I/O error occurred while reading the CSV stream."
            ) from exc

    @staticmethod
    def _parse_stream(
        stream: TextIO,
    ) -> Dataset:
        """
        Parse and validate the complete CSV before creating the Dataset.
        """
        reader = csv.reader(stream, strict=True)

        try:
            header = next(reader)
        except StopIteration as exc:
            raise CSVEmptyError("CSV input is empty.") from exc

        if header and header[0].startswith("\ufeff"):
            header[0] = header[0][1:]

        if tuple(header) != EXPECTED_HEADER:
            raise CSVHeaderError("CSV header does not match the expected format.")

        draws: list[Draw] = []
        seen_ids: set[DrawId] = set()
        seen_dates: set[DrawDate] = set()

        for record_number, row in enumerate(reader, start=2):
            if not row:
                continue

            if len(row) != len(EXPECTED_HEADER):
                raise CSVMalformedError(
                    f"CSV record {record_number} contains {len(row)} fields; "
                    f"expected {len(EXPECTED_HEADER)}."
                )

            for index, value in enumerate(row):
                if value != value.strip():
                    raise CSVFieldError(
                        f"Whitespace around a field value is not allowed "
                        f"at CSV record {record_number}, "
                        f"field '{FIELD_NAMES[index]}': {value!r}."
                    )

            contest_value = row[0]

            if INTEGER_PATTERN.fullmatch(contest_value) is None:
                raise CSVContestNumberError(
                    f"Invalid contest number at CSV record {record_number}, "
                    f"field 'Concorso': {contest_value!r}."
                )

            try:
                contest_number = int(contest_value)
            except ValueError as exc:
                raise CSVContestNumberError(
                    f"Invalid contest number at CSV record "
                    f"{record_number}, field 'Concorso': "
                    f"{contest_value!r}."
                ) from exc

            if not MIN_NUMBER <= contest_number <= MAX_CONTEST_NUMBER:
                raise CSVContestNumberError(
                    f"Contest number at CSV record {record_number}, "
                    f"field 'Concorso' must be between {MIN_NUMBER} and {MAX_CONTEST_NUMBER}; "
                    f"received {contest_value!r}."
                )

            date_value = row[1]

            if DATE_PATTERN.fullmatch(date_value) is None:
                raise CSVDateError(
                    f"Date at CSV record {record_number}, field 'Data' "
                    f"must use the exact DD/MM/YYYY format; "
                    f"received {date_value!r}."
                )

            try:
                parsed_date = datetime.strptime(
                    date_value,
                    "%d/%m/%Y",
                ).date()
            except ValueError as exc:
                raise CSVDateError(
                    f"Invalid draw date at CSV record {record_number}, "
                    f"field 'Data': {date_value!r}."
                ) from exc

            jolly_value = row[8]

            if INTEGER_PATTERN.fullmatch(jolly_value) is None:
                raise CSVJollyError(
                    f"Invalid Jolly at CSV record {record_number}, "
                    f"field 'Jolly': {jolly_value!r}."
                )

            try:
                jolly_number = int(jolly_value)
            except ValueError as exc:
                raise CSVJollyError(
                    f"Invalid Jolly at CSV record {record_number}, "
                    f"field 'Jolly': {jolly_value!r}."
                ) from exc

            if not MIN_NUMBER <= jolly_number <= MAX_NUMBER:
                raise CSVJollyError(
                    f"Jolly at CSV record {record_number}, "
                    f"field 'Jolly' must be between {MIN_NUMBER} and {MAX_NUMBER}; "
                    f"received {jolly_value!r}."
                )

            superstar_value = row[9]

            if parsed_date < SUPERSTAR_INTRODUCTION_DATE:
                if superstar_value != "-":
                    raise CSVSuperstarError(
                        f"Superstar at CSV record {record_number}, "
                        f"field 'Superstar' must be '-' before "
                        f"28/03/2006; received {superstar_value!r}."
                    )
            else:
                if INTEGER_PATTERN.fullmatch(superstar_value) is None:
                    raise CSVSuperstarError(
                        f"Invalid Superstar at CSV record {record_number}, "
                        f"field 'Superstar': {superstar_value!r}."
                    )

                try:
                    superstar_number = int(superstar_value)
                except ValueError as exc:
                    raise CSVSuperstarError(
                        f"Invalid Superstar at CSV record {record_number}, "
                        f"field 'Superstar': {superstar_value!r}."
                    ) from exc

                if not MIN_NUMBER <= superstar_number <= MAX_NUMBER:
                    raise CSVSuperstarError(
                        f"Superstar at CSV record {record_number}, "
                        f"field 'Superstar' must be between {MIN_NUMBER} and {MAX_NUMBER}; "
                        f"received {superstar_value!r}."
                    )

            try:
                draw_id = DrawId.from_official(
                    parsed_date.year,
                    contest_number,
                )
            except InvalidDrawIdError as exc:
                raise CSVContestNumberError(
                    f"Invalid official draw identity at CSV record "
                    f"{record_number}, field 'Concorso': {contest_value!r}."
                ) from exc

            try:
                draw_date = DrawDate.from_parts(
                    parsed_date.year,
                    parsed_date.month,
                    parsed_date.day,
                )
            except InvalidDrawDateError as exc:
                raise CSVDateError(
                    f"Invalid draw date at CSV record {record_number}, "
                    f"field 'Data': {date_value!r}."
                ) from exc

            if draw_id in seen_ids:
                raise CSVDuplicateDrawIdError(
                    f"Duplicate DrawId at CSV record {record_number}, "
                    f"field 'Concorso': {contest_value!r}."
                )

            if draw_date in seen_dates:
                raise CSVDuplicateDrawDateError(
                    f"Duplicate DrawDate at CSV record {record_number}, "
                    f"field 'Data': {date_value!r}."
                )

            parsed_numbers: list[Number] = []

            for index, value in enumerate(row[2:8], start=1):
                if INTEGER_PATTERN.fullmatch(value) is None:
                    raise CSVMainNumberError(
                        f"Invalid main number at CSV record {record_number}, "
                        f"field 'N{index}': {value!r}."
                    )

                try:
                    number_value = int(value)
                except ValueError as exc:
                    raise CSVMainNumberError(
                        f"Invalid main number at CSV record "
                        f"{record_number}, field 'N{index}': "
                        f"{value!r}."
                    ) from exc

                try:
                    parsed_numbers.append(Number(number_value))
                except InvalidNumberError as exc:
                    raise CSVMainNumberError(
                        f"Invalid main number at CSV record {record_number}, "
                        f"field 'N{index}': {value!r}."
                    ) from exc

            numbers = tuple(parsed_numbers)

            if len(set(numbers)) != len(numbers):
                raise CSVRepeatedMainNumberError(
                    f"Repeated main number at CSV record {record_number}, fields N1-N6."
                )

            try:
                combination = Combination(*numbers)
                draw = Draw(
                    id=draw_id,
                    date=draw_date,
                    combination=combination,
                )
            except InvalidDrawError as exc:
                raise CSVDatasetValidationError(
                    f"Domain validation failed at CSV record {record_number}."
                ) from exc

            seen_ids.add(draw_id)
            seen_dates.add(draw_date)
            draws.append(draw)

        if not draws:
            raise CSVEmptyError("CSV input contains no importable data rows.")

        try:
            return Dataset(draws)
        except InvalidDatasetError as exc:
            raise CSVDatasetValidationError(
                "The imported records violate Dataset invariants."
            ) from exc
