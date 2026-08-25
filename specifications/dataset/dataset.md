# Dataset Specification

## Purpose

`Dataset` is the Aggregate Root representing the complete immutable
historical archive of official SuperEnalotto draws.

The Dataset directly owns the immutable collection of `Draw` objects.

---

## Responsibilities

The Dataset is responsible for:

* owning the immutable collection of `Draw` objects;
* preserving chronological ordering;
* enforcing Dataset invariants;
* exposing a stable read-only collection API;
* providing standard Python collection semantics;
* exposing the Dataset Query facade;
* providing the backward-compatible `filter()` facade.

The Dataset is not responsible for:

* statistics;
* probability calculations;
* analytics;
* persistence;
* CSV parsing;
* serialization;
* repository behaviour;
* external services;
* presentation logic.

---

## Aggregate Root

```text
Dataset
│
└── tuple[Draw, ...]
    │
    └── Draw
```

The Dataset directly owns the immutable collection of `Draw` objects.

No intermediate `DrawCollection` abstraction exists.

The internal collection is normalized during construction and stored as
an immutable `tuple[Draw, ...]`.

---

## Public API

### Properties

* `draws`
* `size`
* `count`
* `is_empty`
* `first`
* `last`
* `query`

### `draws`

Returns the immutable tuple containing the Dataset draws.

```text
draws -> tuple[Draw, ...]
```

The returned tuple is the Dataset's immutable storage representation.

---

### `size`

Returns the number of draws contained in the Dataset.

```text
size -> int
```

---

### `count`

Returns the number of draws contained in the Dataset.

```text
count -> int
```

`count` is an alias of `size`.

---

### `is_empty`

Returns `True` when the Dataset contains no draws.

```text
is_empty -> bool
```

---

### `first`

Returns the chronologically oldest `Draw`.

```text
first -> Draw
```

Accessing `first` on an empty Dataset raises:

```text
InvalidDatasetError
```

---

### `last`

Returns the chronologically newest `Draw`.

```text
last -> Draw
```

Accessing `last` on an empty Dataset raises:

```text
InvalidDatasetError
```

---

### `query`

Returns the Dataset Query facade.

```text
query -> DatasetQuery
```

The returned `DatasetQuery` operates on the Dataset without modifying
the underlying aggregate.

---

## Python Collection Protocol

The Dataset implements the standard Python collection protocol.

Supported operations include:

```text
len(dataset)
bool(dataset)
iter(dataset)
reversed(dataset)
draw in dataset
dataset[index]
```

The corresponding protocol methods are:

* `__len__()`
* `__bool__()`
* `__iter__()`
* `__reversed__()`
* `__contains__()`
* `__getitem__()`

The Dataset behaves as an immutable ordered collection of `Draw`
objects.

Iteration, reverse iteration, containment, and index access operate on
the normalized chronological collection.

---

## Construction

The Dataset constructor accepts any `Iterable[Draw]`.

Examples:

```text
Dataset(draws)

Dataset(list_of_draws)

Dataset(tuple_of_draws)

Dataset(generator)
```

Construction performs the following operations:

1. materializes the input iterable;
2. validates that every element is a `Draw`;
3. sorts the draws chronologically by `Draw.date`;
4. validates `DrawId` uniqueness;
5. validates `DrawDate` uniqueness;
6. stores the normalized collection as an immutable tuple.

Input ordering is irrelevant.

For example, an input containing:

```text
Draw(date=2024-03-01)
Draw(date=2024-01-01)
Draw(date=2024-02-01)
```

is exposed by the Dataset as:

```text
Draw(date=2024-01-01)
Draw(date=2024-02-01)
Draw(date=2024-03-01)
```

The constructor therefore guarantees that `first` refers to the oldest
draw and `last` refers to the newest draw.

---

## Invariants

### DS-001 — Draw Type

Every Dataset element must be a `Draw`.

Invalid elements raise:

```text
InvalidDatasetError
```

The Dataset does not accept arbitrary objects or other collection
element types.

---

### DS-002 — Unique DrawId

Draw identifiers must be unique.

Duplicate `DrawId` values are forbidden within the same Dataset.

Violation raises:

```text
InvalidDatasetError
```

---

### DS-003 — Unique DrawDate

Draw dates must be unique.

Duplicate `DrawDate` values are forbidden within the same Dataset.

Violation raises:

```text
InvalidDatasetError
```

---

### DS-004 — Chronological Ordering

Draws are stored in chronological order.

Ordering is determined by:

```text
Draw.date
```

The constructor normalizes the input independently of its original
ordering.

---

### DS-005 — Immutable Storage

Dataset storage is immutable.

The internal collection is:

```text
tuple[Draw, ...]
```

No mutable collection is exposed through the public API.

The contained `Draw` objects are themselves immutable.

---

## Empty Dataset Behaviour

An empty Dataset is valid.

For an empty Dataset:

```text
dataset.draws == ()
dataset.size == 0
dataset.count == 0
dataset.is_empty == True
len(dataset) == 0
bool(dataset) == False
```

The following properties require at least one draw:

```text
dataset.first
dataset.last
```

Accessing either property on an empty Dataset raises:

```text
InvalidDatasetError
```

---

## Filtering Facade

The Dataset provides:

```text
filter(predicate) -> Dataset
```

`filter()` is a backward-compatible facade that delegates the operation
to the Dataset Query Layer.

The original Dataset is not modified.

The operation returns a new Dataset containing the draws matching the
predicate.

The resulting Dataset therefore undergoes the same Dataset
normalization and invariant validation as any other Dataset instance.

---

## Query Layer

Query behaviour does not belong to the Dataset Aggregate itself.

Dataset queries are implemented by the dedicated Query Layer.

The Dataset exposes the query facade through:

```text
dataset.query
```

which returns:

```text
DatasetQuery
```

The Query Layer is responsible for read-oriented operations such as:

* generic filtering;
* date-based selection;
* Number queries;
* Combination queries;
* predicates;
* query composition.

Query operations do not modify the Dataset Aggregate.

The Dataset remains responsible for archive integrity and immutable
collection semantics.

---

## Validation Boundary

Dataset-specific invariant violations use:

```text
InvalidDatasetError
```

Validation includes:

* element type validation;
* `DrawId` uniqueness;
* `DrawDate` uniqueness.

Accessing `first` or `last` on an empty Dataset also raises
`InvalidDatasetError`.

The Dataset does not expose infrastructure exceptions as part of its
domain contract.

---

## Non Goals

Dataset never:

* loads CSV files;
* saves files;
* computes statistics;
* performs probability calculations;
* performs analytics;
* implements persistence;
* implements repository behaviour;
* accesses external services;
* provides presentation logic.

Infrastructure is responsible for creating Dataset instances from
external representations.

Analytics and other higher-level components consume Dataset instances.

---

## Dependency Boundary

The Dataset belongs to the Kernel and depends on domain concepts rather
than infrastructure.

Its aggregate structure is:

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

The Dataset must remain independent of:

* persistence;
* repositories;
* external data sources;
* analytics;
* infrastructure services.

---

## Query Separation

The Dataset Aggregate owns:

* immutable archive storage;
* Draw type integrity;
* DrawId uniqueness;
* DrawDate uniqueness;
* chronological ordering;
* collection semantics.

The Dataset Query Layer owns:

* read-oriented query behaviour;
* filtering;
* date selection;
* Number selection;
* Combination selection;
* query composition.

This separation prevents query behaviour from weakening the aggregate's
invariants or introducing mutation.

---

## Future Metadata

Future versions may introduce a dedicated `DatasetMetadata` Value Object.

Possible architecture:

```text
Dataset
├── tuple[Draw, ...]
└── DatasetMetadata
```

The introduction of metadata must not weaken the Dataset invariants or
its immutable public API.

---

## Architectural Stability

Any modification to the Dataset public API requires:

* Architecture Review;
* ADR update;
* Specification update;
* Test update;
* Documentation update.

No public API changes shall be introduced without following this
process.

---

## Design Principle

`Dataset` is the immutable historical archive Aggregate Root of the
Kernel.

Every valid Dataset is:

* composed exclusively of `Draw` objects;
* free of duplicate `DrawId` values;
* free of duplicate `DrawDate` values;
* chronologically ordered;
* immutable;
* deterministic;
* infrastructure-independent;
* analytics-independent.

The Dataset Query Layer operates on this stable aggregate without
modifying it.

The Dataset therefore provides a reliable domain foundation for
higher-level querying, evidence, statistics, and analytics components.
