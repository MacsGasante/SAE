"""
Tests for the CSV importer.
"""

import io
from io import StringIO
from pathlib import Path

import pytest

from sae.infrastructure.importers.exceptions import (
    CSVJollyError,
    CSVStreamPositionError,
    CSVSuperstarError,
)
from sae.kernel import Number

VALID_HEADER = "Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar"


def test_import_dataset_from_valid_stream() -> None:
    stream = StringIO(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n")

    from sae.infrastructure.importers.csv_importer import CSVImporter

    dataset = CSVImporter.import_dataset(stream)

    assert dataset.size == 1

    draw = dataset.first

    assert draw.id.to_int() == 1998001
    assert draw.date.isoformat() == "1998-01-03"
    assert tuple(number.to_int() for number in draw.numbers) == (
        1,
        2,
        3,
        4,
        5,
        6,
    )


def test_import_dataset_does_not_retain_jolly_or_superstar() -> None:
    stream = StringIO(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n")

    from sae.infrastructure.importers.csv_importer import CSVImporter

    dataset = CSVImporter.import_dataset(stream)

    draw = dataset.first

    assert tuple(number.to_int() for number in draw.numbers) == (
        1,
        2,
        3,
        4,
        5,
        6,
    )
    assert draw.contains(Number(7)) is False
    assert draw.contains(Number(8)) is False


@pytest.mark.parametrize(
    "jolly_value",
    ["1", "90"],
)
def test_import_dataset_accepts_jolly_boundaries(
    jolly_value: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter

    stream = StringIO(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,{jolly_value},-\n")

    dataset = CSVImporter.import_dataset(stream)

    assert dataset.size == 1


@pytest.mark.parametrize(
    "jolly_value",
    ["", "abc", "1.5", "0", "91", "-1", "９"],
)
def test_import_dataset_rejects_invalid_jolly(
    jolly_value: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVJollyError

    stream = StringIO(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,{jolly_value},-\n")

    with pytest.raises(CSVJollyError):
        CSVImporter.import_dataset(stream)


@pytest.mark.parametrize(
    ("date_value", "superstar_value"),
    [
        ("27/03/2006", "-"),
        ("28/03/2006", "1"),
        ("28/03/2006", "90"),
    ],
)
def test_import_dataset_accepts_superstar_for_draw_date(
    date_value: str,
    superstar_value: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter

    stream = StringIO(
        f"{VALID_HEADER}\n1,{date_value},1,2,3,4,5,6,7,{superstar_value}\n"
    )

    dataset = CSVImporter.import_dataset(stream)

    assert dataset.size == 1


@pytest.mark.parametrize(
    ("date_value", "superstar_value"),
    [
        ("27/03/2006", "1"),
        ("27/03/2006", ""),
        ("28/03/2006", "-"),
        ("28/03/2006", ""),
        ("28/03/2006", "abc"),
        ("28/03/2006", "1.5"),
        ("28/03/2006", "0"),
        ("28/03/2006", "91"),
        ("28/03/2006", "９"),
    ],
)
def test_import_dataset_rejects_invalid_superstar_for_draw_date(
    date_value: str,
    superstar_value: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVSuperstarError

    stream = StringIO(
        f"{VALID_HEADER}\n1,{date_value},1,2,3,4,5,6,7,{superstar_value}\n"
    )

    with pytest.raises(CSVSuperstarError):
        CSVImporter.import_dataset(stream)


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("Jolly", "9" * 5000),
        ("Superstar", "9" * 5000),
    ],
)
def test_import_dataset_rejects_excessively_long_discarded_numbers(
    field_name: str,
    field_value: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import (
        CSVJollyError,
        CSVSuperstarError,
    )

    jolly_value = field_value if field_name == "Jolly" else "7"
    superstar_value = field_value if field_name == "Superstar" else "8"
    date_value = "01/01/2024"

    if field_name == "Jolly":
        expected_exception = CSVJollyError
    else:
        expected_exception = CSVSuperstarError

    stream = StringIO(
        f"{VALID_HEADER}\n1,{date_value},1,2,3,4,5,6,{jolly_value},{superstar_value}\n"
    )

    with pytest.raises(expected_exception):
        CSVImporter.import_dataset(stream)


def test_import_dataset_from_path(tmp_path: Path) -> None:
    csv_file = tmp_path / "draws.csv"
    csv_file.write_text(
        f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n",
        encoding="utf-8",
    )

    from sae.infrastructure.importers.csv_importer import CSVImporter

    dataset = CSVImporter.import_dataset(csv_file)

    assert dataset.size == 1
    assert dataset.first.id.to_int() == 1998001


def test_import_dataset_from_string_path(tmp_path: Path) -> None:
    csv_file = tmp_path / "draws.csv"
    csv_file.write_text(
        f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n",
        encoding="utf-8",
    )

    from sae.infrastructure.importers.csv_importer import CSVImporter

    dataset = CSVImporter.import_dataset(str(csv_file))

    assert dataset.size == 1
    assert dataset.first.id.to_int() == 1998001


def test_import_dataset_rejects_stream_not_at_beginning() -> None:
    stream = StringIO(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n")
    stream.read(5)

    from sae.infrastructure.importers.csv_importer import CSVImporter

    with pytest.raises(CSVStreamPositionError):
        CSVImporter.import_dataset(stream)

    assert not stream.closed


def test_import_dataset_does_not_close_caller_stream() -> None:
    stream = StringIO(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n")

    from sae.infrastructure.importers.csv_importer import CSVImporter

    dataset = CSVImporter.import_dataset(stream)

    assert dataset.size == 1
    assert not stream.closed


@pytest.mark.parametrize(
    "contest_number",
    ["abc", "0", "1000", "-1", "1.5", ""],
)
def test_import_dataset_rejects_invalid_contest_number(
    contest_number: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVContestNumberError

    stream = StringIO(f"{VALID_HEADER}\n{contest_number},03/01/1998,1,2,3,4,5,6,7,-\n")

    with pytest.raises(CSVContestNumberError):
        CSVImporter.import_dataset(stream)


def test_import_dataset_rejects_excessively_long_contest_number():
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVContestNumberError

    csv_content = (
        "Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar\n"
        f"{'9' * 5000},01/01/2024,1,2,3,4,5,6,7,8\n"
    )

    with pytest.raises(CSVContestNumberError):
        CSVImporter().import_dataset(io.StringIO(csv_content))


def test_import_dataset_rejects_excessively_long_main_number():
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVMainNumberError

    csv_content = (
        "Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar\n"
        f"1,01/01/2024,{'9' * 5000},2,3,4,5,6,7,8\n"
    )

    with pytest.raises(CSVMainNumberError):
        CSVImporter().import_dataset(io.StringIO(csv_content))


def test_import_dataset_accepts_contest_number_boundaries() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter

    stream = StringIO(
        f"{VALID_HEADER}\n"
        "1,03/01/1998,1,2,3,4,5,6,7,-\n"
        "999,04/01/1998,11,12,13,14,15,16,7,-\n"
    )

    dataset = CSVImporter.import_dataset(stream)

    assert dataset.size == 2
    assert dataset.draws[0].id.to_int() == 1998001
    assert dataset.draws[1].id.to_int() == 1998999


@pytest.mark.parametrize(
    ("date_value", "expects_cause"),
    [
        ("31/02/1998", True),
        ("00/01/1998", True),
        ("01/13/1998", True),
        ("abc", False),
        ("", False),
        ("1998-01-03", False),
    ],
)
def test_import_dataset_rejects_invalid_dates(
    date_value: str,
    expects_cause: bool,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVDateError

    csv_content = f"{VALID_HEADER}\n1,{date_value},1,2,3,4,5,6,7,8\n"

    with pytest.raises(CSVDateError) as exc_info:
        CSVImporter.import_dataset(StringIO(csv_content))

    if expects_cause:
        assert exc_info.value.__cause__ is not None
    else:
        assert exc_info.value.__cause__ is None


@pytest.mark.parametrize(
    "number_value",
    [
        "abc",
        "0",
        "91",
        "-1",
        "1.5",
        "",
    ],
)
def test_import_dataset_rejects_invalid_main_numbers(
    number_value: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVMainNumberError

    csv_content = f"{VALID_HEADER}\n1,03/01/1998,{number_value},2,3,4,5,6,7,-\n"

    with pytest.raises(CSVMainNumberError):
        CSVImporter.import_dataset(StringIO(csv_content))


@pytest.mark.parametrize(
    "main_numbers",
    [
        "1,1,3,4,5,6",
        "1,2,3,4,5,5",
        "7,2,3,4,7,6",
    ],
)
def test_import_dataset_rejects_repeated_main_numbers(
    main_numbers: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import (
        CSVRepeatedMainNumberError,
    )

    csv_content = f"{VALID_HEADER}\n1,03/01/1998,{main_numbers},7,-\n"

    with pytest.raises(CSVRepeatedMainNumberError):
        CSVImporter.import_dataset(StringIO(csv_content))


@pytest.mark.parametrize(
    "header",
    [
        "concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar",
        "Concorso,Data,N1,N2,N3,N4,N5,N6,Superstar,Jolly",
        "Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly",
        "Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar,Extra",
    ],
)
def test_import_dataset_rejects_invalid_headers(header: str) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVHeaderError

    stream = StringIO(f"{header}\n1,03/01/1998,1,2,3,4,5,6,7,-\n")

    with pytest.raises(CSVHeaderError):
        CSVImporter.import_dataset(stream)


def test_import_dataset_accepts_utf8_bom_in_stream() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter

    stream = StringIO(f"\ufeff{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n")

    dataset = CSVImporter.import_dataset(stream)

    assert dataset.size == 1


def test_import_dataset_ignores_fully_empty_rows() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter

    stream = StringIO(f"{VALID_HEADER}\n\n1,03/01/1998,1,2,3,4,5,6,7,-\n\n")

    dataset = CSVImporter.import_dataset(stream)

    assert dataset.size == 1


def test_import_dataset_rejects_separator_only_row() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVFieldError

    stream = StringIO(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n,,,,,,,,,\n")

    with pytest.raises(CSVFieldError):
        CSVImporter.import_dataset(stream)


@pytest.mark.parametrize(
    ("field_index", "field_name", "exception_type"),
    [
        (8, "Jolly", CSVJollyError),
        (9, "Superstar", CSVSuperstarError),
    ],
)
def test_import_dataset_rejects_empty_required_discarded_fields(
    field_index: int,
    field_name: str,
    exception_type: type[Exception],
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter

    fields = ["1", "03/01/1998", "1", "2", "3", "4", "5", "6", "7", "-"]
    fields[field_index] = ""

    stream = StringIO(f"{VALID_HEADER}\n{','.join(fields)}\n")
    with pytest.raises(exception_type, match=field_name):
        CSVImporter.import_dataset(stream)


@pytest.mark.parametrize(
    "row",
    [
        "1,03/01/1998,1,2,3,4,5,6,7",
        "1,03/01/1998,1,2,3,4,5,6,7,8,9",
    ],
)
def test_import_dataset_rejects_rows_with_wrong_field_count(row: str) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVMalformedError

    stream = StringIO(f"{VALID_HEADER}\n{row}\n")

    with pytest.raises(CSVMalformedError):
        CSVImporter.import_dataset(stream)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("Concorso", " 1"),
        ("Concorso", "1 "),
        ("Data", " 03/01/1998"),
        ("Data", "03/01/1998 "),
        ("N1", " 1"),
        ("N1", "1 "),
        ("Jolly", " 7"),
        ("Superstar", "8 "),
    ],
)
def test_import_dataset_rejects_surrounding_whitespace(
    field: str,
    value: str,
) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVFieldError

    values = {
        "Concorso": "1",
        "Data": "03/01/1998",
        "N1": "1",
        "N2": "2",
        "N3": "3",
        "N4": "4",
        "N5": "5",
        "N6": "6",
        "Jolly": "7",
        "Superstar": "-",
    }
    values[field] = value
    row = ",".join(
        values[name]
        for name in (
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
    )

    with pytest.raises(CSVFieldError):
        CSVImporter.import_dataset(StringIO(f"{VALID_HEADER}\n{row}\n"))


def test_import_dataset_rejects_duplicate_draw_id() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import (
        CSVDuplicateDrawIdError,
    )

    stream = StringIO(
        f"{VALID_HEADER}\n"
        "1,03/01/1998,1,2,3,4,5,6,7,-\n"
        "1,04/01/1998,11,12,13,14,15,16,17,-\n"
    )

    with pytest.raises(CSVDuplicateDrawIdError):
        CSVImporter.import_dataset(stream)


def test_import_dataset_rejects_duplicate_draw_date() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import (
        CSVDuplicateDrawDateError,
    )

    stream = StringIO(
        f"{VALID_HEADER}\n"
        "1,03/01/1998,1,2,3,4,5,6,7,-\n"
        "2,03/01/1998,11,12,13,14,15,16,17,-\n"
    )

    with pytest.raises(CSVDuplicateDrawDateError):
        CSVImporter.import_dataset(stream)


def test_import_dataset_sorts_draws_chronologically() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter

    stream = StringIO(
        f"{VALID_HEADER}\n"
        "3,05/01/1998,21,22,23,24,25,26,27,-\n"
        "1,03/01/1998,1,2,3,4,5,6,7,-\n"
        "2,04/01/1998,11,12,13,14,15,16,17,-\n"
    )

    dataset = CSVImporter.import_dataset(stream)

    assert [draw.date.isoformat() for draw in dataset.draws] == [
        "1998-01-03",
        "1998-01-04",
        "1998-01-05",
    ]


def test_import_dataset_rejects_header_only_input() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVEmptyError

    with pytest.raises(CSVEmptyError):
        CSVImporter.import_dataset(StringIO(f"{VALID_HEADER}\n"))


def test_import_dataset_rejects_empty_input() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVEmptyError

    with pytest.raises(CSVEmptyError):
        CSVImporter.import_dataset(StringIO(""))


def test_import_dataset_rejects_missing_path(tmp_path: Path) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVFileAccessError

    missing_file = tmp_path / "missing.csv"

    with pytest.raises(CSVFileAccessError) as exc_info:
        CSVImporter.import_dataset(missing_file)

    assert exc_info.value.__cause__ is not None


def test_import_dataset_rejects_invalid_utf8_file(tmp_path: Path) -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVEncodingError

    csv_file = tmp_path / "invalid_utf8.csv"
    csv_file.write_bytes(
        VALID_HEADER.encode("utf-8") + b"\n" + b"1,03/01/1998,1,2,3,4,5,6,7,\xff\n"
    )

    with pytest.raises(CSVEncodingError) as exc_info:
        CSVImporter.import_dataset(csv_file)

    assert isinstance(exc_info.value.__cause__, UnicodeDecodeError)


def test_import_dataset_rejects_unclosed_csv_quote() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVMalformedError

    stream = StringIO(f'{VALID_HEADER}\n1,03/01/1998,"1,2,3,4,5,6,7,8\n')

    with pytest.raises(CSVMalformedError) as exc_info:
        CSVImporter.import_dataset(stream)

    assert exc_info.value.__cause__ is not None


def test_import_dataset_reports_record_and_field_for_invalid_value() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVMainNumberError

    stream = StringIO(
        f"{VALID_HEADER}\n"
        "1,03/01/1998,1,2,3,4,5,6,7,-\n"
        "2,04/01/1998,91,12,13,14,15,16,17,-\n"
    )

    with pytest.raises(CSVMainNumberError) as exc_info:
        CSVImporter.import_dataset(stream)

    message = str(exc_info.value)
    assert "record 3" in message
    assert "N1" in message


def test_import_dataset_rejects_non_readable_stream() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVMalformedError

    class NonReadableStream(StringIO):
        def readable(self) -> bool:
            return False

    stream = NonReadableStream(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n")

    with pytest.raises(CSVMalformedError):
        CSVImporter.import_dataset(stream)

    assert not stream.closed


def test_import_dataset_rejects_stream_without_determinable_position() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter

    class UnknownPositionStream(StringIO):
        def tell(self) -> int:
            raise OSError("position unavailable")

    stream = UnknownPositionStream(f"{VALID_HEADER}\n1,03/01/1998,1,2,3,4,5,6,7,-\n")

    with pytest.raises(CSVStreamPositionError):
        CSVImporter.import_dataset(stream)

    assert not stream.closed


def test_import_dataset_does_not_return_partial_dataset_on_late_error() -> None:
    from sae.infrastructure.importers.csv_importer import CSVImporter
    from sae.infrastructure.importers.exceptions import CSVMainNumberError

    stream = StringIO(
        f"{VALID_HEADER}\n"
        "1,03/01/1998,1,2,3,4,5,6,7,-\n"
        "2,04/01/1998,11,12,91,14,15,16,17,-\n"
    )

    with pytest.raises(CSVMainNumberError):
        CSVImporter.import_dataset(stream)

    assert not stream.closed
