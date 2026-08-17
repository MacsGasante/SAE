# Dataset Fluent API

Version: 1.0 (Draft)

---

# Purpose

The Dataset Aggregate exposes an immutable fluent API.

Every operation:

- never modifies the current Dataset;
- returns a new Dataset;
- preserves all Dataset invariants;
- preserves chronological ordering;
- is deterministic.

The Fluent API belongs to the Kernel Domain Model.

It is not part of:

- Analytics;
- Persistence;
- Infrastructure.

---

# Design Principles

The Dataset is an immutable Aggregate.

Every fluent operation returns another valid Dataset.

The original Dataset is never modified.

Operations must be composable.

Example:

```python
dataset \
    .after(date) \
    .take(20) \
    .skip(5)
```

---

# General Rules

Every fluent operation:

- returns Dataset;
- never returns list;
- never returns tuple;
- never returns Iterable.

The Dataset remains the only public collection abstraction.

---

# Fluent Operations

## take

```python
dataset.take(count)
```

Returns a Dataset containing the first *count* draws.

Rules:

- count <= 0 returns an empty Dataset.
- count >= dataset size returns the current Dataset.

Complexity:

O(n)

---

## skip

```python
dataset.skip(count)
```

Returns a Dataset after discarding the first *count* draws.

Rules:

- count <= 0 returns the current Dataset.
- count >= dataset size returns an empty Dataset.

Complexity:

O(n)

---

## before

```python
dataset.before(date)
```

Returns every draw strictly before the specified date.

Complexity:

O(n)

---

## after

```python
dataset.after(date)
```

Returns every draw strictly after the specified date.

Complexity:

O(n)

---

## between

```python
dataset.between(
    start,
    end,
)
```

Returns every draw whose date satisfies

```
start <= draw.date <= end
```

Complexity:

O(n)

---

# Ordering

Every returned Dataset preserves chronological ordering.

Sorting is never executed during fluent operations.

The Dataset invariant already guarantees ordering.

---

# Immutability

The original Dataset is never modified.

Example:

```python
filtered = dataset.take(10)

assert filtered is not dataset
```

---

# Composability

Every fluent operation returns another Dataset.

Therefore operations may be chained.

Example:

```python
dataset \
    .after(date) \
    .take(50)
```

---

# Future Extensions

The following operations are considered candidates for future versions.

## containing

```python
dataset.containing(number)
```

Returns every draw containing the specified Number.

---

## excluding

```python
dataset.excluding(number)
```

Returns every draw not containing the specified Number.

---

## matching

```python
dataset.matching(combination)
```

Returns every draw matching a Combination predicate.

---

## filter

```python
dataset.filter(predicate)
```

Generic immutable filtering.

---

# Freeze

The following operations are frozen for Dataset Fluent API v1:

- take
- skip
- before
- after
- between
