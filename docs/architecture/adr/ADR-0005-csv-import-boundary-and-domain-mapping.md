# ADR-0005

## Title

CSV Import Boundary and Domain Mapping

## Status

Accepted

## Date

2026-10-16

---

# Context

SAE accepts historical draw data through an external CSV representation.
The CSV format contains source-specific fields and naming conventions that
must not become part of the Kernel domain model.

The import boundary also has to preserve the domain decisions already
established for DrawId, DrawDate, Combination, and Dataset integrity.

In particular, the official contest identity is represented externally by
the contest number together with the year derived from the draw date.
The CSV also contains Jolly and Superstar fields, which are part of the
source representation but are not represented by the current domain model.

---

# Decision

The CSV Dataset Importer is an Infrastructure boundary responsible for
translating the external CSV representation into the existing domain model.

The importer shall:

1. extract the official contest identity from the external representation;
2. use the canonical DrawId domain derivation from `(year,
   contest_number)` rather than reproducing the identifier encoding in the
   infrastructure layer;
3. construct DrawDate and Combination through their domain contracts;
4. recognize and validate the Jolly and Superstar source fields, while not
   retaining them in the current domain model;
5. construct the final Dataset through the existing Dataset Aggregate Root,
   leaving collection integrity and uniqueness rules under domain
   ownership;
6. fail atomically so that invalid source data cannot produce a partial
   Dataset result.

The importer owns CSV-specific parsing, source validation, and importer
error translation. The Kernel remains independent of CSV and other
external file formats.

---

# Consequences

## Positive

- CSV concerns remain outside the Kernel;
- the canonical DrawId derivation remains centralized in the domain;
- source-only fields do not leak into the domain model;
- Dataset integrity remains owned by the Dataset Aggregate Root;
- invalid imports cannot expose partially constructed Dataset results;
- future external representations can follow the same boundary without
  changing the domain model.

## Negative

- Infrastructure must translate and validate an external representation
  before domain objects can be created;
- source fields that are intentionally discarded remain relevant to input
  validation even though they are not retained in the domain model.

---

# Alternatives Considered

## Alternative A

Add CSV-specific fields such as Jolly and Superstar to the domain model.

Rejected.

Reason:

The current domain model does not represent these source-specific fields,
and retaining them would couple domain concepts to the current external
CSV representation without an established domain requirement.

## Alternative B

Reimplement the DrawId derivation inside the importer.

Rejected.

Reason:

The official contest identity and its deterministic DrawId derivation are
already defined by the DrawId domain contract. Duplicating that rule in
Infrastructure would create two sources of truth.

## Alternative C

Build the Dataset incrementally and expose a partially imported result
when a later record is invalid.

Rejected.

Reason:

Dataset integrity requires the imported collection to satisfy its domain
invariants as a whole. The import operation therefore has atomic semantics.

---

# Related Documents

- `specifications/domain/draw_id.md`
- `specifications/dataset/dataset.md`
- `specifications/dataset/dataset_structure.md`
- `DATASET_GUIDELINES.md`
- `docs/architecture/adr/ADR-0004-dataset-aggregate-root.md`
- `src/sae/infrastructure/importers/csv_importer.py`
