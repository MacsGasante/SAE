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

* persistence;
* infrastructure;
* analytics;
* repository implementations.

---

# Design Principles

Queries operate on an existing Dataset.

The original Dataset is never modified.

Every query operation produces a new `DatasetQuery` wrapping a new
Dataset containing the query result.

All returned Dataset instances remain valid Dataset Aggregate Roots.

Therefore:

* Dataset invariants remain enforced;
* chronological ordering is preserved;
* storage remains immutable;
* query operations are deterministic;
* query operations are composable.

---

# Query Facade

The Dataset exposes the Query Layer through:

```text
dataset.query
```

which returns:

```text
DatasetQuery
```

The public Query Layer entry point is:

```text
from sae.kernel.query import DatasetQuery
```

`DatasetQuery` is a fluent facade over Dataset query operations.

Each query operation returns a new `DatasetQuery` instance.

The resulting Dataset is accessible through:

```text
query.dataset
```

---

# Query Responsibilities

The Query Layer provides operations for:

* generic predicates;
* date-based selection;
* temporal selection;
* DrawId-based selection;
* Number-based selection;
* Combination-based matching;
* query composition.

The Query Layer does not:

* modify Dataset storage;
* perform persistence;
* load CSV files;
* implement repository behaviour;
* calculate statistics;
* perform probability calculations.

---

# Date Queries

## before

```text
dataset.query.before(date)
```

Returns a new `DatasetQuery` containing draws whose date is strictly
before the specified date.

---

## after

```text
dataset.query.after(date)
```

Returns a new `DatasetQuery` containing draws whose date is strictly
after the specified date.

---

## between

```text
dataset.query.between(
    start,
    end,
)
```

Returns a new `DatasetQuery` containing draws whose date satisfies:

```text
start <= draw.date <= end
```

The interval is closed at both boundaries.

---

# Temporal Queries

## by_year

```text
dataset.query.by_year(year)
```

Returns a new `DatasetQuery` containing draws belonging to the specified
calendar year.

---

## by_month

```text
dataset.query.by_month(month)
```

Returns a new `DatasetQuery` containing draws whose date belongs to the
specified month.

---

## by_day

```text
dataset.query.by_day(day)
```

Returns a new `DatasetQuery` containing draws whose date has the
specified day of the month.

---

# DrawId Queries

## by_draw_id

```text
dataset.query.by_draw_id(identifier)
```

Returns a new `DatasetQuery` containing the Draw identified by the
specified `DrawId`.

If no Draw has the specified identifier, the result is an empty
Dataset.

---

# Number Queries

The Query Layer provides Number-oriented queries over Draw objects.

All Number query operations return a new `DatasetQuery`.

## by_number

```text
dataset.query.by_number(number)
```

Returns draws containing the specified `Number`.

---

## contains

```text
dataset.query.contains(number)
```

Returns draws containing the specified `Number`.

`contains(number)` is semantically equivalent to `by_number(number)`.

---

## contains_any

```text
dataset.query.contains_any(
    number1,
    number2,
    ...
)
```

Returns draws containing at least one of the supplied Numbers.

When no Numbers are supplied, the result is an empty Dataset.

---

## contains_all

```text
dataset.query.contains_all(
    number1,
    number2,
    ...
)
```

Returns draws containing all of the supplied Numbers.

When no Numbers are supplied, the result contains all Draws from the
source Dataset.

---

# Combination Queries

The Query Layer provides Combination-oriented queries.

All Combination query operations return a new `DatasetQuery`.

## contains_exactly

```text
dataset.query.contains_exactly(combination)
```

Returns draws whose matching Numbers correspond exactly to the supplied
Combination.

---

## intersects

```text
dataset.query.intersects(combination)
```

Returns draws sharing at least one Number with the supplied
Combination.

---

## matches

```text
dataset.query.matches(
    combination,
    at_least=3,
)
```

Returns draws containing at least the requested number of matching
Numbers with the supplied Combination.

The `at_least` parameter must be between 1 and 6 inclusive.

Values outside this range raise `ValueError`.

The boundary conditions are therefore:

```text
at_least=1
```

is valid, and is equivalent to `intersects(combination)`.

```text
at_least=6
```

is valid, and is equivalent to `contains_exactly(combination)`.

---

# Generic Predicate Queries

## where

```text
dataset.query.where(predicate)
```

Returns a new `DatasetQuery` containing draws satisfying the supplied
predicate.

The predicate operates on `Draw` objects.

---

## filter

```text
dataset.query.filter(predicate)
```

`filter` is an alias of `where`.

It provides equivalent query semantics:

```text
dataset.query.filter(predicate)
```

and:

```text
dataset.query.where(predicate)
```

produce equivalent results.

---

# Query Composition

Query operations are composable.

A query may be refined through successive operations without modifying
the original Dataset.

Example:

```text
result = (
    dataset.query
    .after(start_date)
    .before(end_date)
    .contains(number)
)
```

Each intermediate operation returns a new `DatasetQuery`.

The original Dataset remains unchanged.

Query operations can therefore be chained across different query
categories, including:

* date queries;
* temporal queries;
* DrawId queries;
* Number queries;
* Combination queries;
* generic predicates.

---

# Query Independence

Query objects are independent.

Starting from the same DatasetQuery, separate operations produce
independent query results.

For example:

```text
query = dataset.query

by_2024 = query.by_year(2024)
by_2025 = query.by_year(2025)
```

`by_2024` and `by_2025` are distinct `DatasetQuery` instances wrapping
distinct result Datasets.

Executing one query does not alter the state or result of another query.

---

# Ordering

Dataset results preserve chronological ordering.

The Query Layer must not introduce a different ordering unless such
ordering is explicitly part of a future public query contract.

Dataset construction already guarantees chronological storage.

Every Dataset produced by a query therefore retains the ordering
guarantee of the Dataset Aggregate.

---

# Immutability

Query operations never mutate the original Dataset.

Example:

```text
result = dataset.query.filter(predicate)

assert result.dataset is not dataset
```

The original Dataset remains unchanged.

The original Dataset storage is not replaced, reordered, or otherwise
modified by query execution.

All query results are new Dataset Aggregate Roots with their own
validated immutable storage.

---

# Dataset Invariants

Every Dataset returned by the Query Layer must satisfy all Dataset
invariants:

* every element is a Draw;
* DrawId values are unique;
* DrawDate values are unique;
* draws are chronologically ordered;
* storage is immutable.

The Query Layer therefore cannot bypass Dataset construction or
validation when producing query results.

---

# Query Result Contract

A query result is represented by a `DatasetQuery`.

The resulting Dataset is available through:

```text
query.dataset
```

An empty query result is represented by a valid empty Dataset.

For example:

```text
result = dataset.query.by_year(1999)

assert result.dataset.is_empty
```

An empty result remains a valid Dataset Aggregate Root and continues to
satisfy all Dataset invariants.

---

# Complexity

Unless otherwise specified, query operations are linear in the number
of draws:

```text
O(n)
```

The Query Layer does not require an indexing strategy.

Indexing is an infrastructure or future optimization concern and must
not alter the Dataset Aggregate contract.

---

# Public API Stability

The following `DatasetQuery` methods constitute the public Query Layer
API:

```text
before()
after()
between()

by_year()
by_month()
by_day()
by_draw_id()

by_number()
contains()
contains_any()
contains_all()

matches()
intersects()
contains_exactly()

where()
filter()
```

Only the public Query Layer types and methods are considered stable.

Private implementation modules such as:

```text
_combination.py
_helpers.py
_number.py
_predicates.py
```

are implementation details.

They must not be imported by external layers as public API.

---

# API Equivalence

The following API equivalences are part of the current Query Layer
contract:

```text
contains(number)
```

is equivalent to:

```text
by_number(number)
```

and:

```text
matches(combination, at_least=1)
```

is equivalent to:

```text
intersects(combination)
```

while:

```text
matches(combination, at_least=6)
```

is equivalent to:

```text
contains_exactly(combination)
```

These equivalences are verified by the automated test suite.

---

# Future Extensions

Possible future query capabilities may include:

* additional Number predicates;
* additional Combination predicates;
* optimized query execution;
* metadata-aware queries.

Any new public query operation requires:

* specification update;
* tests;
* documentation update;
* architecture review when the change affects Kernel boundaries.

A new query operation must not be introduced solely through an
implementation change.

---

# Freeze

The Dataset Query Layer contract is frozen at Version 1.0.

Future changes must preserve Dataset immutability and Aggregate
invariants unless explicitly superseded by an Architecture Decision
Record.
