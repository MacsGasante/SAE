# Combination Specification

Identifier: KERNEL-VO-0002

Status: Approved

---

## Purpose

Combination represents an immutable mathematical combination of
distinct SuperEnalotto numbers.

A Combination models the concept of an unordered set of numbers.

Internally, however, numbers are always stored in ascending order
to guarantee deterministic behaviour.

---

## Cardinality

A valid Combination contains exactly six numbers.

---

## Invariants

A Combination shall satisfy all of the following rules.

- exactly six numbers
- all elements are Number
- all numbers are distinct
- internal representation is always sorted
- immutable
- hashable

---

## Equality

Order of construction is irrelevant.

Example

Combination(17,3,90,45,28,62)

equals

Combination(3,17,28,45,62,90)

---

## Public API

Constructor

Combination(\*numbers)

Properties

numbers

Methods

len()

contains()

iter()

to_tuple()

---

## String Representation

Combination(3,17,28,45,62,90)

---

## Dependencies

Kernel only.
