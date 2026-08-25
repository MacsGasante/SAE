# Draw Specification

## Classification

Aggregate Root

---

## Purpose

`Draw` represents one official SuperEnalotto draw.

A `Draw` aggregates the immutable domain objects describing a single
official extraction.

A `Draw` is responsible for the identity and core domain behaviour of
one draw. Statistical and analytical behaviour does not belong to `Draw`.

---

## Components

A `Draw` consists of:

* `DrawId`
* `DrawDate`
* `Combination`

---

## Identity

Identity is represented exclusively by `DrawId`.

Two `Draw` instances with the same `DrawId` represent the same domain
entity.

The `DrawDate` and `Combination` do not participate in equality.

For example, two `Draw` instances with the same `DrawId` are equal even
if their dates or combinations differ.

---

## Responsibilities

A `Draw` is responsible for:

* exposing its identifier;
* exposing the official draw date;
* exposing the winning combination;
* exposing the winning numbers;
* answering whether a `Number` belongs to the winning combination;
* computing the `MatchResult` produced by matching a `Combination`.

No statistical, analytical, persistence, or infrastructure behaviour
belongs to `Draw`.

---

## Public API

### Properties

#### `id`

Returns the `DrawId` identifying the draw.

```text
id -> DrawId
```

---

#### `date`

Returns the official `DrawDate` of the draw.

```text
date -> DrawDate
```

---

#### `combination`

Returns the winning `Combination`.

```text
combination -> Combination
```

---

#### `numbers`

Returns the numbers contained in the winning combination.

```text
numbers -> tuple[Number, ...]
```

The returned value is the immutable tuple exposed by the underlying
`Combination`.

---

## Methods

### `contains()`

Tests whether a `Number` belongs to the draw's winning combination.

```text
contains(number: Number) -> bool
```

Returns `True` when the supplied `Number` belongs to the
`Combination`; otherwise returns `False`.

For example:

```text
draw.contains(Number(4)) == True
draw.contains(Number(90)) == False
```

A value that is not a `Number` does not belong to the draw and returns
`False`.

---

### `matches()`

Computes the matching numbers between the draw's winning `Combination`
and a requested `Combination`.

```text
matches(combination: Combination) -> MatchResult
```

The returned `MatchResult` contains the numbers shared by the two
combinations.

The matching numbers preserve the order in which they occur in the
`Draw` combination.

For example, if the draw contains:

```text
Combination(10, 20, 30, 40, 50, 60)
```

and the requested combination contains:

```text
Combination(10, 30, 40, 70, 80, 90)
```

the resulting `MatchResult` contains:

```text
(10, 30, 40)
```

`matches()` performs domain matching only. It does not perform
statistical or analytical calculations.

---

## Equality

`Draw` equality is identity-based.

Two `Draw` instances are equal if and only if their `DrawId` values are
equal.

The following properties do not affect equality:

* `date`;
* `combination`;
* `numbers`.

For example:

```text
Draw(DrawId(10), date=A, combination=X)
==
Draw(DrawId(10), date=B, combination=Y)
```

provided both instances contain the same `DrawId`.

A `Draw` is not equal to an object of another type.

---

## Hashability

`Draw` is hashable.

The hash value depends exclusively on `DrawId`.

Equal `Draw` instances therefore have equal hash values.

`Draw` instances may be used as:

* dictionary keys;
* members of sets.

For example:

```text
hash(draw1) == hash(draw2)
```

when `draw1` and `draw2` have the same `DrawId`.

---

## Ordering

`Draw` does not define natural ordering.

Ordering must always be explicit.

Examples of valid external ordering criteria include:

* `DrawId`;
* `DrawDate`.

The `Draw` Aggregate Root does not implement comparison operators for
ordering between draws.

---

## Immutability

`Draw` is immutable after construction.

The following properties cannot be replaced:

* `id`;
* `date`;
* `combination`.

All contained domain objects are themselves immutable.

No mutable collection is exposed through the public API.

The `numbers` property exposes the immutable tuple provided by the
`Combination`.

---

## Validation

Construction validates all required aggregate components.

The following types are required:

```text
id          -> DrawId
date        -> DrawDate
combination -> Combination
```

Invalid construction raises:

```text
InvalidDrawError
```

The constructor rejects values that are not instances of the required
domain types.

Validation occurs before the aggregate state is established.

---

## String Representation

The canonical `repr()` representation identifies the aggregate and its
three primary components.

Format:

```text
Draw(id=<id>, date=<date>, combination=<combination>)
```

For example:

```text
Draw(id=DrawId(1), date=2026-01-07, combination=Combination(1, 2, 3, 4, 5, 6))
```

The representation includes:

* `id=`;
* `date=`;
* `combination=`.

The string representation is intended to provide a deterministic
debugging representation of the aggregate.

---

## Dependencies

`Draw` belongs to the Kernel Domain layer.

It depends on:

### Foundation

* `Number`

### Collections

* `Combination`

### Domain

* `DrawId`
* `DrawDate`
* `MatchResult`

`Draw` may use internal domain implementation helpers to perform its
matching behaviour.

These helpers are implementation details and are not part of the public
API.

`Draw` must not depend on:

* persistence;
* repositories;
* analytics;
* external services;
* infrastructure concerns.

---

## Public API Stability

The current public `Draw` API consists of:

```text
Draw(id, date, combination)

id
date
combination
numbers

contains(number)
matches(combination)

__eq__()
__hash__()
__repr__()
```

The following members are implementation details and are not part of
the public API:

```text
_validate()
```

Private attributes such as:

```text
_id
_date
_combination
```

are also implementation details.

---

## Domain Boundaries

`Draw` owns the core domain behaviour of a single official extraction.

The following concerns remain outside the aggregate:

* dataset-level querying;
* filtering;
* statistics;
* analytics;
* persistence;
* repository access;
* infrastructure.

`matches()` is a domain-level matching operation and returns a
`MatchResult`. It does not introduce statistical or analytical
responsibilities into the aggregate.

---

## Design Principle

`Draw` is a Kernel Domain Aggregate Root.

It owns the identity of one official SuperEnalotto draw and aggregates
the immutable objects required to describe it.

The aggregate is:

* identity-based;
* immutable;
* hashable;
* deterministic;
* infrastructure-independent;
* free of statistical responsibilities.

All invariants required by the aggregate are validated during
construction and remain valid throughout the lifetime of the `Draw`.
