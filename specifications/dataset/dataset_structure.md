# Dataset Internal Structure Specification

Status

Approved

---

## Purpose

This document specifies the internal organization of the Dataset Aggregate Root.

It defines the invariants governing the historical archive of SuperEnalotto draws independently from its concrete implementation.

This specification is implementation-independent.

---

## Aggregate

Dataset

---

## Internal Storage

The Dataset stores an immutable ordered collection of Draw objects.

Internal representation:

```python
tuple[Draw, ...]
```

The storage is immutable.

No mutable collection shall ever be exposed by the public API.

---

## Ordering

Draws are always stored in chronological order.

Ordering is defined by the ordering rules of the Draw Value Object.

The constructor shall automatically normalize the ordering.

Users are not required to provide sorted input.

---

## Invariants

### DS-001

Every element must be a Draw.

---

### DS-002

Draw identifiers must be unique.

No two Draw instances may share the same DrawId.

Violation raises:

InvalidDatasetError

---

### DS-003

Draw dates must be unique.

No two Draw instances may share the same DrawDate.

Violation raises:

InvalidDatasetError

---

### DS-004

The internal storage is immutable.

The Dataset never exposes mutable collections.

---

## Public API

The Dataset exposes:

- draws
- size
- first
- last

and the standard collection protocol:

- len(dataset)
- iter(dataset)
- draw in dataset

---

## Excluded Features

This specification intentionally excludes:

- searching
- filtering
- indexing
- statistics
- analytics
- persistence

These capabilities belong to later milestones.

---

## Design Principles

The Dataset shall be:

- immutable;
- deterministic;
- infrastructure-independent;
- analytics-independent;
- fully reproducible.

The Dataset is the Aggregate Root of the Dataset Layer.

No intermediate DrawCollection object exists.

The internal tuple of Draw objects belongs directly to the Dataset Aggregate.

---

## Notes

The Dataset Layer replaces the previously proposed DrawCollection abstraction.

The invariants defined in this document remain valid.

Only the architectural ownership has changed:

Before:

Dataset
↓
DrawCollection
↓
tuple[Draw]

Current design:

Dataset
↓
tuple[Draw]

This simplification removes an unnecessary abstraction while preserving all domain invariants.
