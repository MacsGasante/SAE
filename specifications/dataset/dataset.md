# Dataset Specification

## Purpose

Dataset is the Aggregate Root representing the complete immutable
historical archive of SuperEnalotto draws.

---

## Responsibilities

The Dataset is responsible for:

- owning the immutable collection of Draw objects;
- preserving chronological ordering;
- enforcing Dataset invariants;
- exposing a stable read-only collection API.

The Dataset is not responsible for:

- statistics;
- probability calculations;
- analytics;
- persistence;
- CSV parsing;
- serialization;
- repository behaviour.

---

## Aggregate Root

Dataset

↓

tuple[Draw]

The Dataset directly owns the immutable collection of Draw objects.

No intermediate DrawCollection abstraction exists.

---

## Public API

### Properties

- draws
- size
- count
- is_empty
- first
- last
- query

### Python Collection Protocol

- `__len__()`
- `__iter__()`
- `__contains__()`
- `__getitem__()`

The Dataset remains the only public collection abstraction for the
historical archive.

---

## Construction

The Dataset constructor accepts any `Iterable[Draw]`.

Examples:

```
Dataset(draws)

Dataset(list_of_draws)

Dataset(tuple_of_draws)

Dataset(generator)
```

Construction is responsible for:

- validating Draw types;
- normalizing chronological ordering;
- enforcing DrawId uniqueness;
- enforcing DrawDate uniqueness;
- creating immutable storage.

Input ordering is irrelevant.

---

## Invariants

### DS-001

Every element must be a Draw.

---

### DS-002

Draw identifiers must be unique.

Duplicate DrawId values are forbidden.

Violation raises:

`InvalidDatasetError`

---

### DS-003

Draw dates must be unique.

Duplicate DrawDate values are forbidden.

Violation raises:

`InvalidDatasetError`

---

### DS-004

Draws are stored in chronological order.

The constructor normalizes the input independently of input ordering.

---

### DS-005

Dataset storage is immutable.

No mutable collection is exposed through the public API.

---

## Query Layer

Query behaviour does not belong to the Dataset Aggregate itself.

Dataset queries are implemented by the dedicated Query Layer.

The Dataset exposes the query facade through:

```
dataset.query
```

which returns:

```
DatasetQuery
```

The Query Layer is responsible for:

- filtering;
- searching;
- number predicates;
- combination predicates;
- date predicates;
- composable query operations.

The Dataset remains responsible only for archive integrity and
immutable collection semantics.

---

## Non Goals

Dataset never:

- loads CSV files;
- saves files;
- computes statistics;
- performs probability calculations;
- performs analytics;
- implements persistence;
- implements repository behaviour.

Infrastructure creates Dataset instances.

Analytics and other higher layers consume Dataset instances.

---

## Future Metadata

Future versions may introduce a dedicated `DatasetMetadata` Value Object.

Possible architecture:

Dataset

├── tuple[Draw]

└── DatasetMetadata

The introduction of metadata must not weaken the Dataset invariants or
its immutable public API.

---

## Architectural Stability

Any modification to the Dataset public API requires:

- Architecture Review;
- ADR update;
- Specification update;
- Test update;
- Documentation update.

No public API changes shall be introduced without following this process.
