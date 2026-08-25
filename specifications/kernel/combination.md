# Combination Specification

Identifier: KERNEL-VO-0002

Status: Approved

---

## Purpose

`Combination` represents an immutable mathematical combination of distinct
SuperEnalotto `Number` objects.

A `Combination` models an unordered set of exactly six numbers.

Internally, numbers are always stored in ascending order to guarantee
deterministic behaviour.

---

## Cardinality

A valid `Combination` contains exactly six numbers.

The required cardinality is defined by the Kernel constant
`COMBINATION_SIZE`.

---

## Invariants

A `Combination` shall satisfy all of the following rules:

* exactly six numbers;
* every element is a `Number`;
* all numbers are distinct;
* numbers are stored internally in ascending order;
* internal storage is immutable;
* the value object is hashable.

Invalid construction raises:

```text
InvalidCombinationError
```

---

## Construction

The public constructor is:

```text
Combination(*numbers)
```

The constructor accepts exactly six `Number` objects.

Input order is not significant.

The constructor validates:

1. element types;
2. cardinality;
3. duplicate values.

After validation, the numbers are stored in ascending order.

---

## Equality

Equality is based on the mathematical combination of numbers.

The order in which the numbers are supplied during construction is
irrelevant.

For example:

```text
Combination(17, 3, 90, 45, 28, 62)
```

is equal to:

```text
Combination(3, 17, 28, 45, 62, 90)
```

Two `Combination` instances containing the same six `Number` values are
therefore equal regardless of construction order.

---

## Public API

### `numbers`

Returns the numbers in ascending order.

The returned value is an immutable tuple:

```text
tuple[Number, ...]
```

---

### `size`

Returns the number of values contained in the combination.

For every valid `Combination`:

```text
size == 6
```

---

### `minimum`

Returns the smallest `Number` in the combination.

---

### `maximum`

Returns the largest `Number` in the combination.

---

### `numbers_set`

Returns the numbers as an immutable set:

```text
frozenset[Number]
```

This property provides set semantics without exposing mutable storage.

---

## Collection Protocol

`Combination` implements the standard Python collection operations:

### Iteration

```text
for number in combination:
    ...
```

Iteration follows the internal ascending order.

---

### Length

```text
len(combination)
```

is equivalent to:

```text
combination.size
```

---

### Membership

```text
number in combination
```

tests whether the specified `Number` belongs to the combination.

---

## Immutability

`Combination` is immutable after construction.

The internal collection of numbers cannot be replaced or modified.

The `numbers` property exposes tuple-backed storage.

The `numbers_set` property exposes a `frozenset`.

No mutable collection is exposed through the public API.

---

## Hashability

`Combination` is hashable.

Equal `Combination` instances therefore have equal hash values and may be
used as dictionary keys or members of sets.

---

## Ordering of Stored Values

Although a `Combination` is mathematically unordered, its internal
representation is deterministic.

Numbers are always stored in ascending order.

For example:

```text
Combination(90, 3, 45, 17, 62, 28)
```

is internally represented as:

```text
(3, 17, 28, 45, 62, 90)
```

This ordering is an implementation invariant and does not change the
mathematical equality semantics.

---

## String Representation

The canonical representation is:

```text
Combination(3, 17, 28, 45, 62, 90)
```

The representation lists the stored numbers in ascending order.

---

## Error Handling

Invalid combinations raise `InvalidCombinationError`.

The following conditions are invalid:

### Wrong cardinality

Any number of values other than six is invalid.

### Invalid element type

Every element must be a `Number`.

### Duplicate values

The six numbers must be distinct.

---

## Dependencies

`Combination` belongs to the Kernel Collections layer.

It depends only on Kernel abstractions and does not depend on:

* persistence;
* infrastructure;
* repositories;
* analytics;
* external services.

---

## Public API Stability

The following members constitute the current public `Combination` API:

```text
Combination(*numbers)

numbers
size
minimum
maximum
numbers_set

__iter__()
__len__()
__contains__()
__repr__()
```

Private validation helpers are implementation details and are not part of
the public API.

---

## Design Principle

`Combination` is a Kernel Value Object.

It owns the invariants necessary to guarantee that every instance
represents exactly one valid six-number SuperEnalotto combination.

The object is immutable, deterministic, hashable, and independent of
infrastructure concerns.
