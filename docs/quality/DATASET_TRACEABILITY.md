# Dataset Traceability

## Purpose

This document provides traceability between the Dataset specification,
its kernel implementation, and the automated test suite.

The objective is to ensure that every Dataset invariant defined by the
architecture is:

* explicitly specified;
* implemented in the kernel;
* covered by automated tests;
* independently verifiable.

This document does not introduce new Dataset behaviour.

---

## Traceability Matrix

| Invariant | Specification                                                          | Implementation                                                                     | Tests                                                                                                                                                                   | Status      |
| --------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| DS-001    | `specifications/dataset/dataset.md` — Every element must be a `Draw`   | `src/sae/kernel/dataset/validators.py` — `validate_draw_type()`                    | `tests/kernel/dataset/test_dataset_validation.py` — `test_invalid_type_raises()`                                                                                        | **Covered** |
| DS-002    | `specifications/dataset/dataset.md` — Draw identifiers must be unique  | `src/sae/kernel/dataset/validators.py` — `validate_draw_id()`                      | `tests/kernel/dataset/test_dataset_validation.py` — `test_duplicate_draw_id_raises()`                                                                                   | **Covered** |
| DS-003    | `specifications/dataset/dataset.md` — Draw dates must be unique        | `src/sae/kernel/dataset/validators.py` — `validate_draw_date()`                    | `tests/kernel/dataset/test_dataset_validation.py` — `test_duplicate_draw_date_raises()`                                                                                 | **Covered** |
| DS-004    | `specifications/dataset/dataset.md` — Draws are stored chronologically | `src/sae/kernel/dataset/validators.py` — `normalize_draws()`                       | `tests/kernel/dataset/test_dataset_construction.py` — `test_dataset_is_sorted_by_date()`, `test_dataset_sorts_multiple_draws()`, `test_create_dataset_from_generator()` | **Covered** |
| DS-005    | `specifications/dataset/dataset.md` — Dataset storage is immutable     | `Dataset` exposes tuple-backed storage through `draws` and the collection protocol | `tests/kernel/dataset/test_dataset_properties.py` — `test_draws_returns_tuple()`, `test_draws_cannot_be_modified()`                                                     | **Covered** |

---

## DS-001 — Draw Type Integrity

### Requirement

Every element supplied to a Dataset must be a `Draw`.

### Implementation

The Dataset construction path materializes the input iterable and
validates every element through:

`normalize_draws()` → `validate_draw_type()`.

Invalid elements raise `InvalidDatasetError`.

### Verification

The test:

`test_invalid_type_raises()`

constructs a Dataset containing an object that is not a `Draw` and
verifies that `InvalidDatasetError` is raised.

### Status

**Covered**

---

## DS-002 — DrawId Uniqueness

### Requirement

Every Draw identifier within a Dataset must be unique.

### Implementation

`validate_dataset()` maintains a set of encountered `DrawId` values.

`validate_draw_id()` rejects an identifier already present in the set
and raises `InvalidDatasetError`.

### Verification

The test:

`test_duplicate_draw_id_raises()`

creates two Draw objects with the same `DrawId` and verifies that
Dataset construction fails with `InvalidDatasetError`.

### Status

**Covered**

---

## DS-003 — DrawDate Uniqueness

### Requirement

Every Draw date within a Dataset must be unique.

### Implementation

`validate_dataset()` maintains a set of encountered `DrawDate` values.

`validate_draw_date()` rejects a date already present in the set and
raises `InvalidDatasetError`.

### Verification

The test:

`test_duplicate_draw_date_raises()`

creates two Draw objects with the same `DrawDate` and verifies that
Dataset construction fails with `InvalidDatasetError`.

### Status

**Covered**

---

## DS-004 — Chronological Ordering

### Requirement

Draws must be stored in chronological order independently of the input
ordering.

### Implementation

`normalize_draws()` materializes the input iterable and sorts the
validated Draw objects by their `date` property.

The normalized result is returned as an immutable tuple.

### Verification

The construction test suite verifies:

* two Draw objects supplied in reverse chronological order are
  normalized correctly;
* multiple Draw objects are sorted chronologically;
* a one-shot generator is accepted and normalized correctly.

Relevant tests:

* `test_dataset_is_sorted_by_date()`
* `test_dataset_sorts_multiple_draws()`
* `test_create_dataset_from_generator()`

### Status

**Covered**

---

## DS-005 — Immutable Dataset Storage

### Requirement

Dataset storage must be immutable and no mutable collection may be
exposed through the public API.

### Implementation

Dataset storage is represented by a tuple of Draw objects.

The public `draws` property exposes this tuple rather than a mutable
collection.

The Python collection protocol operates on the same immutable storage.

### Verification

The property tests verify:

* `dataset.draws` is a tuple;
* iteration produces the same collection content;
* repeated access returns the same tuple object;
* attempting item assignment through `dataset.draws` raises `TypeError`.

Relevant tests:

* `test_draws_returns_tuple()`
* `test_draws_cannot_be_modified()`

### Status

**Covered**

---

## Construction Traceability

Dataset construction follows the following invariant enforcement path:

```text
Iterable[Draw]
     │
     ▼
normalize_draws()
     │
     ├── materialize iterable
     │
     ├── validate_draw_type()
     │
     └── chronological sort
     │
     ▼
tuple[Draw, ...]
     │
     ▼
validate_dataset()
     │
     ├── validate_draw_id()
     │
     └── validate_draw_date()
     │
     ▼
immutable Dataset state
```

This establishes that validation and normalization are performed during
construction rather than delegated to callers.

---

## Collection API Traceability

The Dataset specification defines the following Python collection
protocol:

* `__len__()`
* `__iter__()`
* `__contains__()`
* `__getitem__()`

The collection protocol operates over the immutable tuple-backed
Dataset storage.

The dedicated collection protocol tests provide behavioural coverage
for these operations.

---

## Empty Dataset Traceability

An empty iterable is a valid Dataset construction input.

The construction tests verify:

* empty tuple storage;
* `size == 0`;
* `count == 0`;
* `len(dataset) == 0`;
* `is_empty is True`;
* `bool(dataset) is False`.

Accessing `first` or `last` on an empty Dataset raises
`InvalidDatasetError`, as verified by the Dataset validation tests.

---

## Query Boundary

The Dataset specification explicitly separates Dataset integrity from
query behaviour.

The Dataset exposes the query facade through:

```text
dataset.query
```

Query behaviour is implemented by the dedicated Query Layer and is not
included in the DS-001–DS-005 invariant traceability matrix.

This separation preserves the Aggregate Root boundary:

```text
Dataset
├── immutable Draw storage
├── Dataset invariants
└── query facade
       │
       ▼
   DatasetQuery
```

Dataset invariants therefore remain independent from filtering and
search algorithms.

---

## Quality Gate

At the time of this traceability review, the Dataset invariant changes
are supported by the following project-wide verification results:

* MyPy: no issues found in 31 source files;
* pytest: 201 tests passed;
* Ruff: all checks passed;
* Black: all files unchanged;
* isort: checks passed.

These checks confirm the current implementation and test suite are
consistent with the traced Dataset invariants.

---

## Maintenance Rule

Any future modification affecting DS-001–DS-005 must update all
applicable layers of this traceability chain:

1. Dataset specification;
2. kernel implementation;
3. automated tests;
4. this traceability document;
5. relevant architectural documentation or ADRs.

A requirement must not be considered implemented solely because code
exists for it. It is considered **Covered** only when specification,
implementation, and automated verification remain aligned.

---

## Current Traceability Status

All Dataset invariants currently defined by the Dataset Specification
are covered by the kernel implementation and automated tests.

**DS-001 — Covered**

**DS-002 — Covered**

**DS-003 — Covered**

**DS-004 — Covered**

**DS-005 — Covered**

No uncovered Dataset invariant is currently identified by this
traceability review.
