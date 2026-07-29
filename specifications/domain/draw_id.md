# DrawId Specification

## Purpose

DrawId represents the logical identifier of a SuperEnalotto draw.

It uniquely identifies one draw inside the domain.

---

## Classification

Value Object

---

## Responsibilities

DrawId is responsible for:

- representing a draw identifier;
- validating its own invariants;
- exposing the identifier value;
- supporting equality by value;
- supporting ordering;
- supporting hashing.

---

## Invariants

A DrawId must satisfy all of the following:

- value is an integer;
- value is greater than zero.

No upper limit is defined.

Future draws must remain valid without modifying the model.

---

## Public API

Constructor

```python
DrawId(value: int)
```

Properties

```python
value
```

Methods

```python
to_int()

__str__()

__repr__()
```

---

## Equality

Two DrawId objects are equal when their values are equal.

Example

```python
DrawId(10) == DrawId(10)
```

---

## Ordering

DrawId objects are naturally ordered.

Example

```python
DrawId(5) < DrawId(8)
```

---

## Hashability

DrawId is immutable and hashable.

It may safely be used as:

- dictionary key;
- set element.

---

## Exceptions

Construction raises:

```python
InvalidDrawIdError
```

when:

- value is not an integer;
- value is less than or equal to zero.

---

## Dependencies

DrawId depends only on:

- ValueObject
- InvalidDrawIdError

No dependency on higher layers is allowed.

---

## Testing Requirements

The following behaviours shall be verified:

- valid construction;
- invalid type;
- invalid range;
- equality;
- ordering;
- hashability;
- string representation;
- integer conversion.

---

## Architectural Notes

DrawId is the first Domain Value Object.

It follows exactly the same implementation philosophy adopted for:

- Number
- Combination

to ensure architectural consistency across the Kernel.
