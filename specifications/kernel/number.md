# Number Specification

**Identifier:** KERNEL-VO-0001

## Status

Approved

---

## Purpose

`Number` represents a valid SuperEnalotto number.

It is an immutable Value Object.

A `Number` can assume only values in the inclusive range:

1..90

No other values are allowed.

---

## Design Goals

- Immutable
- Hashable
- Comparable
- Lightweight
- Type-safe

---

## Invariants

The following conditions must always hold.

- value >= 1
- value <= 90

Violation of an invariant must raise a domain exception.

---

## Equality

Two Number instances are equal if and only if their numeric value is equal.

Example:

Number(17) == Number(17)

Number(17) != Number(18)

---

## Ordering

Numbers are naturally ordered.

Example:

Number(5) < Number(12)

---

## Hash

The hash value depends exclusively on the numeric value.

---

## String Representation

str(Number(7))

returns

7

repr(Number(7))

returns

Number(7)

---

## Public API

Constructor

Number(value: int)

Properties

value -> int

Methods

to_int() -> int

---

## Error Conditions

The constructor shall reject:

- values smaller than 1
- values greater than 90
- non-integer values

---

## Dependencies

None.

The implementation belongs to the Kernel and must not depend on external packages.
