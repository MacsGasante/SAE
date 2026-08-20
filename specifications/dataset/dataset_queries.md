# Dataset Query Specification

Version: 1.0

Status: Approved

---

# Purpose

The Dataset Query Layer provides read-oriented query operations over a
Dataset.

Queries never modify the Dataset Aggregate.

The Query Layer is responsible for expressing search and filtering
behaviour while preserving Dataset immutability and invariants.

The Query Layer belongs to the Kernel.

It is not part of:

- persistence;
- infrastructure;
- analytics;
- repository implementations.

---

# Design Principles

Queries operate on an existing Dataset.

The original Dataset is never modified.

Every query operation produces a new Dataset or a query result according
to its public contract.

All returned Dataset instances remain valid Dataset Aggregate Roots.

Therefore:

- Dataset invariants remain enforced;
- chronological ordering is preserved;
- storage remains immutable;
- query operations are deterministic.

---

# Query Facade

The Dataset exposes the Query Layer through:

```
dataset.query
```

which returns:

```
DatasetQuery
```

The public Query Layer entry point is:

```
from sae.kernel.query import DatasetQuery
```

---

# Query Responsibilities

The Query Layer provides operations for:

- generic predicates;
- date-based selection;
- Number-based selection;
- Combination-based matching;
- query composition.

The Query Layer does not:

- modify Dataset storage;
- perform persistence;
- load CSV files;
- implement repository behaviour;
- calculate statistics;
- perform probability calculations.

---

# Query Operations

## filter

```
dataset.query.filter(predicate)
```

Returns a query result containing the draws satisfying the supplied
predicate.

The predicate operates on `Draw` objects.

---

## before

```
dataset.query.before(date)
```

Returns draws whose date is strictly before the specified date.

---

## after

```
dataset.query.after(date)
```

Returns draws whose date is strictly after the specified date.

---

## between

```
dataset.query.between(
    start,
    end,
)
```

Returns draws whose date satisfies:

```
start <= draw.date <= end
```

---

# Number Queries

The Query Layer provides Number-oriented queries over Draw objects.

Examples include:

```
dataset.query.containing(number)
```

and:

```
dataset.query.excluding(number)
```

These operations return a Dataset containing the matching draws.

---

# Combination Queries

The Query Layer provides Combination-oriented queries.

Examples include:

```
dataset.query.contains_exactly(combination)
```

```
dataset.query.intersects(combination)
```

```
dataset.query.matches(
    combination,
    at_least=3,
)
```

The query semantics are based on the Number matches between the Draw
and the supplied Combination.

---

# Query Composition

Query operations are composable.

A query may be refined through successive operations without modifying
the original Dataset.

Example:

```
result = (
    dataset.query
    .after(start_date)
    .before(end_date)
    .containing(number)
)
```

Each intermediate query remains deterministic.

---

# Ordering

Dataset results preserve chronological ordering.

The Query Layer must not introduce a different ordering unless such
ordering is explicitly part of a future public query contract.

Dataset construction already guarantees chronological storage.

---

# Immutability

Query operations never mutate the original Dataset.

Example:

```
result = dataset.query.filter(predicate)

assert result.dataset is not dataset
```

The original Dataset remains unchanged.

---

# Invariants

Every Dataset returned by the Query Layer must satisfy all Dataset
invariants:

- every element is a Draw;
- DrawId values are unique;
- DrawDate values are unique;
- draws are chronologically ordered;
- storage is immutable.

---

# Complexity

Unless otherwise specified, query operations are linear in the number
of draws:

```
O(n)
```

The Query Layer does not require an indexing strategy.

Indexing is an infrastructure or future optimization concern and must
not alter the Dataset Aggregate contract.

---

# Public API Stability

Only the public Query Layer types and methods are considered stable.

Private implementation modules such as:

```
_combination.py
_helpers.py
_number.py
_predicates.py
```

are implementation details.

They must not be imported by external layers as public API.

---

# Future Extensions

Possible future query capabilities may include:

- additional Number predicates;
- additional Combination predicates;
- optimized query execution;
- metadata-aware queries.

Any new public query operation requires:

- specification update;
- tests;
- documentation update;
- architecture review when the change affects Kernel boundaries.

---

# Freeze

The Dataset Query Layer contract is frozen at Version 1.0.

Future changes must preserve Dataset immutability and Aggregate
invariants unless explicitly superseded by an Architecture Decision
Record.
