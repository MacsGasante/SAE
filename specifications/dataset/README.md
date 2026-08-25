# Dataset Specifications

The Dataset Layer represents the complete immutable historical archive of
official SuperEnalotto draws.

The Dataset Layer belongs to the Kernel because it models domain concepts
and does not depend on infrastructure, persistence, analytics, or
presentation.

The Dataset Layer provides the Dataset Aggregate Root and its dedicated
Query Layer.

---

## Components

* Dataset Aggregate Root
* Dataset Query Layer

The Dataset Aggregate Root directly owns the immutable collection of
`Draw` objects.

No intermediate `DrawCollection` abstraction exists.

The Dataset stores its draws as:

```text
tuple[Draw, ...]
```

The collection is normalized during construction and ordered
chronologically by `DrawDate`.

---

## Design Goals

The Dataset Layer is designed to be:

* immutable;
* chronologically ordered;
* deterministic;
* reproducible;
* infrastructure-independent;
* analytics-independent;
* type-safe.

---

## Dataset Aggregate Root

`Dataset` is the Aggregate Root representing the complete historical
archive of official draws.

The aggregate guarantees the following invariants:

* every element is a `Draw`;
* `DrawId` values are unique;
* `DrawDate` values are unique;
* draws are ordered chronologically;
* internal storage is immutable.

The Dataset accepts any iterable of `Draw` objects during construction.
The iterable is materialized into the internal immutable tuple.

Input order does not determine Dataset order.

Draws are automatically sorted by `DrawDate`.

---

## Public Dataset Surface

The Dataset exposes the following primary properties:

```text
draws -> tuple[Draw, ...]
size -> int
count -> int
is_empty -> bool
first -> Draw
last -> Draw
query -> DatasetQuery
```

### `draws`

Returns the immutable tuple containing the Dataset draws.

### `size`

Returns the number of draws.

### `count`

Returns the number of draws.

`count` is an alias of `size`.

### `is_empty`

Returns `True` when the Dataset contains no draws.

### `first`

Returns the chronologically oldest draw.

Accessing `first` on an empty Dataset raises:

```text
InvalidDatasetError
```

### `last`

Returns the chronologically newest draw.

Accessing `last` on an empty Dataset raises:

```text
InvalidDatasetError
```

### `query`

Returns the Dataset Query facade:

```text
DatasetQuery
```

The Query facade provides read-oriented operations without modifying
the Dataset Aggregate.

---

## Python Collection Behaviour

The Dataset implements the standard collection protocol.

Supported operations include:

```text
len(dataset)
bool(dataset)
iter(dataset)
reversed(dataset)
draw in dataset
dataset[index]
```

The Dataset therefore behaves as an immutable ordered collection of
`Draw` objects.

Iteration follows chronological order.

Index access follows the same order.

---

## Filtering Facade

The Dataset provides:

```text
filter(predicate) -> Dataset
```

`filter()` is a backward-compatible facade that delegates filtering to
the Dataset Query Layer.

Filtering does not mutate the original Dataset.

The result is a new Dataset containing the matching draws.

The Dataset Aggregate therefore remains immutable.

---

## Validation

Dataset construction validates all aggregate invariants.

The following conditions are rejected:

### Invalid element type

Every element must be a `Draw`.

Invalid elements raise:

```text
InvalidDatasetError
```

### Duplicate DrawId

Each `DrawId` must be unique within the Dataset.

Duplicate identifiers raise:

```text
InvalidDatasetError
```

### Duplicate DrawDate

Each `DrawDate` must be unique within the Dataset.

Duplicate dates raise:

```text
InvalidDatasetError
```

Validation occurs after materializing and type-validating the input and
before the normalized collection becomes the Dataset state.

---

## Immutability

The Dataset is immutable after construction.

Its internal collection is stored as:

```text
tuple[Draw, ...]
```

No mutable collection is exposed through the public API.

The returned `draws` tuple cannot be modified.

Contained `Draw` objects are themselves immutable domain objects.

The Dataset therefore provides immutable aggregate storage.

---

## Ordering

Dataset ordering is chronological.

The Dataset automatically sorts its draws by:

```text
Draw.date
```

The input order is irrelevant.

For example, if the input contains:

```text
Draw(date=2024-03-01)
Draw(date=2024-01-01)
Draw(date=2024-02-01)
```

the Dataset exposes:

```text
Draw(date=2024-01-01)
Draw(date=2024-02-01)
Draw(date=2024-03-01)
```

Consequently:

```text
first
```

always represents the oldest draw, while:

```text
last
```

always represents the newest draw.

---

## Non Goals

The Dataset Layer does not:

* read CSV files;
* parse external formats;
* connect to databases;
* perform statistical analysis;
* calculate frequencies or delays;
* implement persistence;
* implement repository behaviour;
* access external services;
* provide presentation logic.

Those responsibilities belong to Infrastructure, Analytics, or other
higher-level layers.

---

## Dependency Graph

The Dataset Aggregate depends on domain objects in the Kernel:

```text
Dataset
│
└── tuple[Draw, ...]
    │
    └── Draw
        │
        └── Combination
            │
            └── Number
```

The Dataset Query Layer operates on Dataset instances:

```text
Dataset
│
└── DatasetQuery
```

The Dataset does not depend on infrastructure or persistence concerns.

---

## Query Layer

The Dataset Query Layer provides read-oriented operations over Dataset
instances.

The Dataset exposes the query facade through:

```text
dataset.query
```

which returns:

```text
DatasetQuery
```

The Query Layer provides operations such as:

* generic filtering;
* date-based selection;
* Number queries;
* Combination queries;
* query composition.

Query operations never modify the Dataset Aggregate.

A query produces a new result rather than changing the underlying
Dataset.

---

## Architecture

Current Dataset architecture:

```text
Dataset
│
└── tuple[Draw, ...]
```

Current Query architecture:

```text
Dataset
│
└── DatasetQuery
```

The Dataset Aggregate is responsible for:

* aggregate integrity;
* immutable storage;
* Draw uniqueness;
* chronological ordering;
* collection semantics.

The Query Layer is responsible for:

* read-oriented query behaviour;
* filtering;
* query composition;
* query-specific selection logic.

These responsibilities remain separated.

---

## Error Boundary

Dataset construction and aggregate access use:

```text
InvalidDatasetError
```

for Dataset-specific invariant violations and invalid access to
`first` or `last` when the Dataset is empty.

The Dataset does not expose infrastructure exceptions as part of its
domain contract.

---

## Design Principle

The Dataset is the immutable historical archive Aggregate Root of the
Kernel.

It guarantees that every valid Dataset is:

* composed exclusively of `Draw` objects;
* free of duplicate `DrawId` values;
* free of duplicate `DrawDate` values;
* chronologically ordered;
* immutable;
* deterministic;
* independent of infrastructure;
* independent of analytics.

The Dataset Query Layer operates on this stable aggregate without
modifying it.

The Dataset therefore provides a reliable domain foundation for
higher-level query, evidence, statistics, and analytics components.
