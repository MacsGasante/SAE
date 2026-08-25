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

```text
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

```text
InvalidDatasetError
```

---

### DS-003

Draw dates must be unique.

No two Draw instances may share the same DrawDate.

Violation raises:

```text
InvalidDatasetError
```

---

### DS-004

Draws must be stored in chronological order.

The Dataset constructor shall normalize the input ordering so that the internal storage is always chronological.

The ordering is determined by the `date` property of each Draw.

---

### DS-005

The internal storage is immutable.

The Dataset never exposes mutable collections.

The public `draws` property exposes the immutable tuple-backed Dataset storage.

---

## Public API

The Dataset exposes:

* `draws`
* `size`
* `count`
* `is_empty`
* `first`
* `last`
* `query`

The standard collection protocol is also supported:

* `len(dataset)`
* `iter(dataset)`
* `draw in dataset`
* `dataset[index]`

The `query` property exposes the Dataset Query Layer through a `DatasetQuery` facade.

Query behaviour is specified separately in:

```text
specifications/dataset/dataset_queries.md
```

The Query Layer does not alter the Dataset Aggregate or its storage.

---

## Excluded Features

This specification intentionally excludes:

* statistics;
* analytics;
* persistence;
* repository implementations;
* infrastructure concerns.

Query and filtering behaviour are part of the Dataset Query Layer and are specified separately.

---

## Design Principles

The Dataset shall be:

* immutable;
* deterministic;
* infrastructure-independent;
* analytics-independent;
* fully reproducible.

The Dataset is the Aggregate Root of the Dataset Layer.

No intermediate DrawCollection object exists.

The internal tuple of Draw objects belongs directly to the Dataset Aggregate.

---

## Notes

The Dataset Layer replaces the previously proposed DrawCollection abstraction.

The invariants defined in this document remain valid.

Only the architectural ownership has changed:

Before:

```text
Dataset
    ↓
DrawCollection
    ↓
tuple[Draw]
```

Current design:

```text
Dataset
    ↓
tuple[Draw]
```

This simplification removes an unnecessary abstraction while preserving all Dataset invariants.

The Dataset Query Layer is exposed through the Dataset Aggregate but remains a separate concern with its own specification.

---

## Invariant Summary

The Dataset invariants are:

```text
DS-001  Every element is a Draw
DS-002  DrawId values are unique
DS-003  DrawDate values are unique
DS-004  Draws are chronologically ordered
DS-005  Dataset storage is immutable
```

These invariants are enforced during Dataset construction and remain valid for every Dataset produced by the Dataset Query Layer.
