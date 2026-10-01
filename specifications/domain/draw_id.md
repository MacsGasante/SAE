# DrawId Specification

## Purpose

DrawId represents the logical identifier of a SuperEnalotto draw.

It uniquely identifies one draw inside the domain.

DrawId can also be deterministically derived from the official contest
identity represented by the pair:

```python
(year, contest_number)
```

The official contest identity remains the authoritative source identity.
DrawId is the internal global identifier used by the domain model.

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
- supporting hashing;
- deriving a deterministic identifier from an official contest identity.

---

## Invariants

A DrawId must satisfy all of the following:

- value is an integer;
- value is greater than zero.

No upper limit is defined for directly constructed DrawId values.

For identifiers derived from an official contest identity:

- year must be an integer;
- the resulting DrawId must satisfy the normal DrawId validity rules;
- contest number must be an integer;
- contest number must be between 1 and 999 inclusive.

The derived identifier is calculated as:

```text
DrawId = year * 1000 + contest_number
```

The derivation is deterministic.

The resulting DrawId preserves chronological ordering across years and
within the contests of the same year.

---
## Public API

### Constructor

```python
DrawId(value: int)
```

### Properties

```python
value
```

### Methods

```python
to_int()

__str__()

__repr__()
```

### Official Contest Identity

```python
DrawId.from_official(
    year: int,
    contest_number: int,
)
```

`from_official()` creates a DrawId from the official contest identity.

The method:

1. validates the types of `year` and `contest_number`;
2. validates that `contest_number` is in the inclusive range 1 through 999;
3. derives the global identifier using:

```text
DrawId = year * 1000 + contest_number
```

The method does not depend on any external representation such as CSV,
database records, or file formats.

External layers are responsible for extracting the official contest
identity from their source representation.

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

Identifiers derived from official contest identities preserve the
chronological ordering of those identities.

For example:

```text
(year=2026, contest_number=999)
<
(year=2027, contest_number=1)
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

`from_official()` raises:

```python
InvalidDrawIdError
```

when:

- year is not an integer;
- contest number is not an integer;
- contest number is less than 1;
- contest number is greater than 999.

---

## Dependencies

DrawId depends only on:

- ValueObject
- InvalidDrawIdError

No dependency on higher layers is allowed.

The official contest identity derivation does not introduce any dependency
on external data formats or infrastructure.

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
- integer conversion;
- derivation from a valid official contest identity;
- deterministic derivation from the same official contest identity;
- distinction between equal contest numbers in different years;
- chronological ordering across year boundaries;
- chronological ordering within the same year;
- invalid contest number below 1;
- invalid contest number above 999;
- invalid year type;
- invalid contest number type.

---

## Architectural Notes

DrawId is the first Domain Value Object.

It follows exactly the same implementation philosophy adopted for:

- Number
- Combination

to ensure architectural consistency across the Kernel.

The official contest identity `(year, contest_number)` is a domain-level
concept, while the extraction of that identity from external formats
belongs to the corresponding external or infrastructure layer.

DrawId must not depend on CSV parsing or other infrastructure concerns.
