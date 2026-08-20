# Dataset Guidelines

Version

1.0

Status

Approved

---

# Purpose

The Dataset Aggregate Root represents the complete immutable historical archive of SuperEnalotto draws.

The Dataset is one of the fundamental Kernel components.

It defines the canonical representation of historical extraction data inside SAE.

The Dataset is intentionally minimal.

Its responsibility is to preserve the integrity of the historical archive.

---

# Dataset Philosophy

The Dataset follows the same design philosophy adopted throughout the Kernel.

The Dataset must always be:

- immutable
- deterministic
- reproducible
- infrastructure independent

Two identical historical archives shall always produce identical Dataset instances.

---

# Responsibilities

The Dataset is responsible for:

- storing Draw objects;
- preserving chronological ordering;
- guaranteeing all domain invariants;
- exposing immutable read-only access;
- exposing the Dataset Query facade.

The Dataset is NOT responsible for:

- statistics;
- probability calculations;
- searching;
- filtering;
- query implementation;
- indexing strategies;
- persistence;
- serialization;
- CSV parsing;
- repository behaviour.

Query behaviour belongs to the dedicated Query Layer.

---

# Aggregate Root

The Dataset is the Aggregate Root of the Dataset Layer.

The Aggregate owns directly the immutable collection of Draw objects.

Architecture:

Dataset
    ↓
tuple[Draw]

No intermediate DrawCollection abstraction exists.

---

# Internal Representation

The Dataset internally stores:

```
tuple[Draw, ...]
```

The internal representation is considered an implementation detail.

Only the public API is stable.

---

# Domain Invariants

The Dataset shall always guarantee the following invariants.

## DS-001

Every element is a Draw.

---

## DS-002

Draw identifiers are unique.

Duplicate DrawId values are forbidden.

Violation raises:

`InvalidDatasetError`

---

## DS-003

Draw dates are unique.

Duplicate DrawDate values are forbidden.

Violation raises:

`InvalidDatasetError`

---

## DS-004

Draws are stored in chronological order.

Input ordering is irrelevant.

The constructor shall normalize the archive automatically.

---

## DS-005

The Dataset storage is immutable.

No mutable collection shall ever be exposed.

---

# Public API

The following API is considered stable.

## Properties

- draws
- size
- count
- is_empty
- first
- last
- query

## Python Collection Protocol

- len(dataset)
- iter(dataset)
- draw in dataset
- dataset[index]

The Dataset itself remains the only public collection abstraction.

---

# Query Layer

Query behaviour is implemented outside the Dataset Aggregate.

The Dataset exposes the Query Layer through:

```
dataset.query
```

which returns a `DatasetQuery`.

The Query Layer is responsible for:

- generic filtering;
- date-based queries;
- Number queries;
- Combination queries;
- query composition.

Query operations must never mutate the Dataset.

---

# Construction

The Dataset constructor accepts any `Iterable[Draw]`.

Examples:

```
Dataset(draws)

Dataset(list_of_draws)

Dataset(tuple_of_draws)

Dataset(generator)
```

The constructor is responsible for:

- validating the archive;
- sorting draws chronologically;
- enforcing uniqueness;
- creating immutable storage.

Input ordering is irrelevant.

---

# Forbidden Responsibilities

The Dataset shall never implement:

- statistical algorithms;
- probability calculations;
- analytics;
- query algorithms;
- repository behaviour;
- persistence;
- CSV import/export;
- serialization.

These responsibilities belong to appropriate higher or adjacent layers
of the architecture.

---

# Future Evolution

Future versions of SAE may introduce:

`DatasetMetadata`

without modifying the fundamental Dataset Aggregate ownership model.

Possible future architecture:

Dataset
│
├── tuple[Draw]
└── DatasetMetadata

The Dataset Aggregate shall remain the owner of both components.

---

# Stability Contract

Any modification to the Dataset public API requires:

- Architecture Review;
- ADR update;
- Specification update;
- Test update;
- Documentation update.

No public API changes shall be introduced without following this process.

---

# Extension Policy

New behaviour may only be added when it belongs to one of the following categories:

- integrity validation;
- immutable navigation;
- archive consistency.

Query behaviour belongs to the dedicated Query Layer.

Features related to analytics or persistence belong to higher layers.

---

# Architecture Notes

The DrawCollection abstraction was intentionally removed during the
architectural review of the Dataset Layer.

The Aggregate Root owns the immutable collection directly.

Architecture evolution:

Previous proposal

Dataset
    ↓
DrawCollection
    ↓
tuple[Draw]

Current architecture

Dataset
    ↓
tuple[Draw]

This simplification removes an unnecessary abstraction while preserving
all domain invariants.

---

# References

- `docs/architecture/adr/ADR-0004-dataset-aggregate-root.md`
- `specifications/dataset/dataset.md`
- `specifications/dataset/dataset_structure.md`
- `specifications/dataset/dataset_queries.md`
- `docs/testing/TESTING_GUIDELINES.md`
