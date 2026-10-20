# C2 — CSV Import Specification

## Status

* Version: 1.0
* Status: Proposed
* Milestone: C2 — Import Tools
* Scope: Import of the official SuperEnalotto historical CSV archive

---

## 1. Purpose

C2 introduces the import capability required to construct a SAE `Dataset` from the official SuperEnalotto CSV representation.

The importer belongs to the infrastructure layer. It translates external data into existing Kernel domain objects without introducing CSV-related responsibilities into the Kernel.

The result of a successful import is one complete, validated, immutable `Dataset`.

An unsuccessful import must not return a partial Dataset.

## 2. Scope

### 2.1 In scope

The CSV importer is responsible for:

* reading CSV input from a supported source;
* validating the CSV header and row structure;
* validating the input encoding when opening a file path;
* parsing the official contest number and draw date;
* validating the six main numbers through the existing domain contracts;
* constructing the corresponding domain objects;
* creating a Dataset from all imported draws;
* reporting import failures with useful diagnostic information;
* managing file resources according to the ownership rules defined in this specification.

### 2.2 Out of scope

C2 does not introduce:

* CSV parsing or file access into the Kernel;
* changes to the `Draw`, `DrawId`, `DrawDate`, `Number`, `Combination`, or `Dataset` contracts;
* persistence or database integration;
* CSV export;
* statistical analysis or probability calculations;
* Jolly or Superstar domain properties;
* automatic correction of invalid input;
* partial-import or error-recovery modes;
* changes to the existing C1 informational CLI commands.

## 3. Architectural Placement

The importer belongs to the infrastructure layer, outside `src/sae/kernel/`.

Package location:

`src/sae/infrastructure/importers/`

Specification location:

`specifications/importers/csv_import.md`

The CSV-specific implementation must remain isolated from the domain model.

The importer may depend on existing Kernel APIs, but the Kernel must never depend on the importer, CSV libraries, file formats, or infrastructure exceptions.

The importer must use the existing domain constructors and APIs as the authoritative source of domain validation.

## 4. Public Interface and Resource Ownership

### 4.1 Supported input sources

The public import operation must accept both:

* a filesystem path represented by `str` or `Path`;
* an already-open, readable text stream.

Both input modes must produce the same domain result for equivalent valid CSV content.

The public operation must have one consistent import contract regardless of the supported input source.

### 4.2 Filesystem paths

When given a filesystem path, the importer is responsible for opening and closing the file.

The file must be decoded as UTF-8, accepting an optional UTF-8 byte-order mark (BOM).

The importer must close the file after processing, including when import fails.

File access and decoding failures must be reported through the infrastructure import exception contract.

### 4.3 Already-open text streams

When given an already-open text stream:

* the stream must be readable;
* the stream must be positioned at the beginning of the input;
* the importer must not silently seek or rewind the stream;
* if the stream is not positioned at the beginning, the import must fail;
* the importer must not close the caller-owned stream;
* text decoding is the responsibility of the caller because the input is already decoded.

The importer must not assume that it owns resources supplied by the caller.

### 4.4 Stream position validation

The importer must establish whether the stream is positioned at the beginning before consuming its content.

If the initial position cannot be established reliably, the importer must fail rather than silently repositioning the stream.

The failure must be reported through the infrastructure import exception contract.

## 5. Input Contract

### 5.1 Supported format

The importer accepts a comma-separated CSV file representing official SuperEnalotto draws.

The required header is exactly:

`Concorso,Data,N1,N2,N3,N4,N5,N6,Jolly,Superstar`

The ten columns must appear in the specified order.

The header is case-sensitive. Renamed, missing, additional, or reordered columns are invalid.

The optional UTF-8 BOM must be accepted when reading a filesystem path.

### 5.2 Encoding and delimiter

* Encoding for filesystem paths: UTF-8, with an optional BOM.
* Input type for already-open streams: decoded text.
* Delimiter: comma.
* The first CSV record is the header.
* The importer must use CSV-aware parsing rather than splitting lines manually.
* Filesystem input that cannot be decoded using the supported encoding must fail.

### 5.3 Column definitions

| Column      | Meaning                                          | Domain treatment             |
| ----------- | ------------------------------------------------ | ---------------------------- |
| `Concorso`  | Official contest number within the calendar year | Used to construct `DrawId`   |
| `Data`      | Official draw date                               | Used to construct `DrawDate` |
| `N1`        | First main winning number                        | Imported into `Combination`  |
| `N2`        | Second main winning number                       | Imported into `Combination`  |
| `N3`        | Third main winning number                        | Imported into `Combination`  |
| `N4`        | Fourth main winning number                       | Imported into `Combination`  |
| `N5`        | Fifth main winning number                        | Imported into `Combination`  |
| `N6`        | Sixth main winning number                        | Imported into `Combination`  |
| `Jolly`     | Additional official draw number                  | Recognized but discarded     |
| `Superstar` | Additional official draw number                  | Recognized but discarded     |

Jolly and Superstar are not represented in the current domain model. Their values must not be added to `Draw` or `Combination` and must not be retained in the resulting Dataset.

The columns must nevertheless be present in the header and in the expected position.

### 5.4 Date-dependent Superstar validation

The official historical CSV archive uses `-` for the Superstar field before
28 March 2006, when the Superstar feature had not yet been introduced. The
first draw date for which a numeric Superstar value is expected is
28/03/2006.

Validation must be based on the parsed value of the `Data` column:

* For draw dates before 28/03/2006, `Superstar` must be exactly `-`.
  Empty values, numeric values, and all other representations are invalid.
* For draw dates on or after 28/03/2006, `Superstar` must be an integer
  from 1 through 90 inclusive. A hyphen, an empty value, a non-integer
  representation, or a value outside this range is invalid.

The importer must validate this rule for every record independently of its
row position or contest number. As specified above, a valid Superstar value
is discarded after validation and is not retained in the domain model.

### 5.5 Header validation

The first CSV record must match the required header exactly.

A missing header, an empty input, or a header with missing, additional, renamed, differently capitalized, or reordered columns must cause the import to fail.

A header-only file is not a valid import because it contains no draw records.

## 6. Row Processing

### 6.1 Blank rows

Completely empty CSV rows must be ignored.

A row containing separators but no values is not considered a completely empty row. It must be validated and must fail when required fields are missing.

A row containing only whitespace must not be silently discarded as an empty row.

Whitespace-only fields must be treated as invalid input, not as missing values that can be automatically corrected.

### 6.2 Row structure

Every non-empty data row must contain exactly ten fields.

Rows with missing or additional fields must cause the import to fail.

The importer must use CSV-aware parsing so that record and field boundaries are interpreted according to CSV rules.

Malformed CSV structure must cause the import to fail.

### 6.3 Field whitespace and parsing

The importer must not silently normalize or repair input fields.

Leading or trailing whitespace in a non-empty field is invalid.

The importer must not use trimming to make an otherwise invalid field acceptable.

The importer must validate required fields rather than silently substituting defaults.

* `Concorso` must represent a valid integer without surrounding whitespace.
* `Data` must follow the format `DD/MM/YYYY`, without surrounding whitespace, and represent a real calendar date.
* `N1` through `N6` must represent valid integers without surrounding whitespace.
* `Jolly` and `Superstar` must be present in the expected columns; their values are discarded and are not stored in the domain.
* Invalid values must not be silently coerced, rounded, replaced, or skipped.

A failure involving a field must identify the relevant field whenever possible.

### 6.4 Contest number

The contest number must be an integer from 1 through 999 inclusive.

The calendar year must be derived from the parsed draw date.

The importer must construct the identifier using:

`DrawId.from_official(year, contest_number)`

The importer must not implement a second version of the DrawId formula and must not introduce `DrawId.from_csv()`.

### 6.5 Draw date

The date must follow the exact format `DD/MM/YYYY`.

The parsed date must represent a real calendar date.

The importer must use the existing `DrawDate` domain API to construct the domain value.

Invalid dates must cause the import to fail.

### 6.6 Main winning numbers

Each of the six main numbers must satisfy the existing `Number` domain constraints:

* integer value;
* minimum value: 1;
* maximum value: 90.

The six numbers must be distinct.

The importer must use the existing `Number` and `Combination` constructors to enforce domain validity. It must not duplicate their validation rules as an alternative source of truth.

The original order of the six CSV columns does not need to be preserved in the domain: `Combination` stores its numbers in ascending order.

## 7. Domain Construction

For every valid non-empty data row, the importer must:

1. Parse the official draw date.
2. Parse the official contest number.
3. Derive the calendar year from the parsed date.
4. Construct `DrawId` using `DrawId.from_official()`.
5. Construct `DrawDate` from the parsed calendar date.
6. Construct six `Number` instances.
7. Construct one `Combination` from those numbers.
8. Construct one `Draw` using the identifier, date, and combination.

After all data rows have been processed successfully, the importer must construct one `Dataset` containing all resulting draws.

The importer must not bypass domain constructors or directly manipulate their internal state.

The importer must not create or retain additional domain properties for Jolly or Superstar.

## 8. Dataset Integrity

The resulting Dataset must satisfy all existing Dataset invariants.

In particular:

* every element must be a valid `Draw`;
* `DrawId` values must be unique;
* draw dates must be unique;
* draws must be ordered chronologically;
* the resulting collection must remain immutable.

The importer must not depend on the input file already being chronologically ordered. The existing Dataset normalization is responsible for chronological ordering.

A duplicate official identity, which produces a duplicate `DrawId`, must cause the import to fail.

Two draws with the same date must also cause the import to fail.

The importer must not silently remove duplicates or choose one row over another.

## 9. Atomic Import Behaviour

Importation is an all-or-nothing operation.

### 9.1 Successful import

If the input source, header, all non-empty rows, all constructed domain objects, and the final Dataset are valid, the importer returns the complete Dataset.

The successful result must contain every valid draw record from the input, excluding only completely empty CSV rows.

### 9.2 Failed import

If any validation or construction step fails:

* the import operation fails;
* no partial Dataset is returned;
* invalid rows are not silently skipped;
* no invalid values are substituted;
* duplicate draws are not silently removed;
* no changes are made to the Kernel to accommodate malformed input.

The importer must not expose a partially populated Dataset as a successful result.

A failed import must not leave any persistent or external partial state because persistence and external side effects are outside the scope of C2.

## 10. Error Handling

### 10.1 Exception hierarchy

CSV import failures must be represented by an infrastructure-level exception hierarchy.

The public base exception is `CSVImportError`. It must derive from the project-wide `SAEError` base exception defined by the Kernel, whose documented contract is to provide the common base for SAE exceptions.

All importer-specific exceptions exposed by the public import operation must derive from `CSVImportError`.

This inheritance provides callers with a common exception boundary without moving CSV-specific exception types into the Kernel. The Kernel must not import or depend on the infrastructure importer or its exception classes.

### 10.2 Error categories

The exception hierarchy must distinguish, at minimum, the following categories:

* input file access failure;
* unsupported or invalid encoding;
* invalid or missing header;
* malformed CSV structure;
* invalid initial position or unverifiable position of an input stream;
* empty input or header-only input;
* missing or invalid required field;
* invalid contest number;
* invalid date;
* invalid main number;
* repeated main number within a combination;
* duplicate official draw identity;
* duplicate draw date;
* final Dataset validation failure.

The implementation may use dedicated subclasses for these categories or use a field-validation subclass with explicit, documented error categories for related field errors.

The exact public subclass names must be established during implementation and documented consistently. The base exception name `CSVImportError` is fixed by this specification.

### 10.3 Diagnostic information

When a failure can be associated with a particular data record, the diagnostic should include the CSV record or line number and the field involved, where available.

Diagnostics should provide enough context to identify the invalid input without requiring the caller to inspect internal implementation details.

The exception contract must not require retaining the entire input file or storing Jolly or Superstar values in the domain.

### 10.4 Exception chaining

When an underlying file, parsing, or domain validation exception is translated into an infrastructure import exception, the implementation must preserve the underlying exception as the cause where applicable.

The importer must not obscure the original cause with an unrelated exception.

## 11. Empty Input

The following inputs must fail:

* a file containing no CSV records;
* a file containing only the required header;
* a file containing only completely empty data rows after the header.

An input containing a valid header and at least one valid non-empty data record may succeed, subject to all other requirements.

The importer must never return an empty Dataset as the result of a successful CSV import.

## 12. Testing Requirements

The test suite must verify the public import contract and the integration with the existing Kernel domain model.

At minimum, tests must cover:

### 12.1 Input sources and resource ownership

* import from a filesystem path;
* import from an already-open text stream;
* equivalent results for equivalent input content;
* acceptance of a stream positioned at the beginning;
* rejection of a stream positioned elsewhere, without automatically rewinding it;
* failure when the initial stream position cannot be established;
* closure of importer-owned files after success and failure;
* preservation of caller ownership of an already-open stream.

### 12.2 CSV format

* exact valid header;
* optional UTF-8 BOM for filesystem input;
* invalid encoding;
* missing, renamed, reordered, differently capitalized, or additional header columns;
* malformed CSV structure;
* missing and additional row fields;
* completely empty rows;
* separator-only rows;
* whitespace-only rows and fields;
* leading or trailing whitespace in field values.

### 12.3 Domain validation

* valid contest numbers at the lower and upper boundaries;
* contest number zero and values greater than 999;
* invalid contest number representations;
* valid dates and invalid calendar dates;
* invalid date formats;
* Superstar is `-` before 28/03/2006 and rejects numeric values before that date;
* Superstar accepts integers from 1 through 90 on and after 28/03/2006 and rejects `-`, empty, non-integer, and out-of-range values;
* main numbers at the valid boundaries 1 and 90;
* main numbers outside the valid range;
* non-integer main number representations;
* repeated main numbers within a row;
* derivation of the year from the draw date;
* construction through existing domain APIs.

### 12.4 Dataset integrity and atomicity

* successful import of multiple draws;
* chronological ordering independent of CSV row order;
* duplicate official draw identity;
* duplicate draw date;
* rejection of an empty file;
* rejection of a header-only file;
* rejection when all data rows are completely empty;
* no partial Dataset returned when a later row fails;
* no silent row skipping for invalid records;
* no retention of Jolly or Superstar in the domain result.

### 12.5 Error contract

* every importer-specific exception derives from `CSVImportError`;
* relevant error categories are distinguishable;
* row or field diagnostics are supplied where applicable;
* underlying causes are preserved when exceptions are translated.

Tests must use the existing test framework and repository conventions. The Kernel must not acquire a dependency on the test framework or on the importer.

## 13. Acceptance Criteria

C2 CSV Import is ready for certification when all of the following are satisfied:

* [ ] The importer resides in the infrastructure layer.
* [ ] The public import operation accepts `str` and `Path` inputs.
* [ ] The public import operation accepts an already-open readable text stream.
* [ ] The importer respects the ownership rules for both input modes.
* [ ] The importer rejects streams that are not positioned at the beginning and does not silently reposition them.
* [ ] The required CSV header is validated exactly.
* [ ] UTF-8 and an optional BOM are supported for filesystem input.
* [ ] CSV parsing uses a CSV-aware parser.
* [ ] Completely empty rows are ignored, while malformed or incomplete records are rejected.
* [ ] Surrounding whitespace in non-empty fields is rejected rather than normalized.
* [ ] Empty files and header-only files are rejected.
* [ ] Contest number, draw date, and main numbers are validated through the existing domain contracts.
* [ ] `DrawId.from_official()` is used without duplicating its formula or introducing `DrawId.from_csv()`.
* [ ] Jolly and Superstar are recognized but are not retained in the domain.
* [ ] Superstar validation follows the 28/03/2006 introduction-date boundary.
* [ ] The resulting Dataset satisfies all existing Dataset invariants.
* [ ] Duplicate identifiers and duplicate dates cause the import to fail.
* [ ] Importation is atomic and never returns a partial Dataset.
* [ ] All importer-specific public exceptions derive from `CSVImportError`.
* [ ] Useful diagnostics and exception chaining are provided.
* [ ] The required tests pass.
* [ ] The existing Kernel contracts remain unchanged.
* [ ] The repository's required quality checks pass.
* [ ] Documentation is consistent with the implemented public contract.

## 14. Related Documents

* `specifications/dataset/README.md`
* `specifications/dataset/dataset.md`
* `specifications/dataset/dataset_queries.md`
* `specifications/dataset/dataset_structure.md`
* `specifications/domain/draw.md`
* `specifications/domain/draw_date.md`
* `specifications/domain/draw_id.md`
* `specifications/kernel/combination.md`
* `specifications/kernel/number.md`
* `docs/architecture/README.md`
* `docs/architecture/adr/ADR-0004-dataset-aggregate-root.md`
