# Number Specification

**Identifier:** KERNEL-VO-0001

## Status

Approved

---

## Purpose

`Number` represents a valid SuperEnalotto number.

It is an immutable Value Object belonging to the Kernel Foundation.

A `Number` can assume only integer values in the inclusive range:

```text
1..90
```

No other values are allowed.

---

## Design Goals

`Number` is designed to be:

* immutable;
* hashable;
* comparable;
* lightweight;
* type-safe;
* independent of infrastructure concerns.

---

## Invariants

The following conditions must always hold:

* the underlying value is an integer;
* the value is greater than or equal to `1`;
* the value is less than or equal to `90`.

Therefore, every valid `Number` satisfies:

```text
1 <= number.value <= 90
```

Violation of any invariant raises:

```text
InvalidNumberError
```

---

## Construction

The public constructor is:

```text
Number(value: int)
```

The constructor validates:

1. the underlying value type;
2. the allowed numeric range.

Valid boundary values include:

```text
Number(1)
Number(25)
Number(90)
```

Values outside the valid range are rejected.

Examples:

```text
Number(0)
Number(-1)
Number(91)
Number(100)
```

Non-integer values are also rejected.

Examples:

```text
Number(7.5)
Number("7")
Number(None)
```

All invalid construction attempts raise `InvalidNumberError`.

---

## Equality

Two `Number` instances are equal if and only if their numeric values are equal.

For example:

```text
Number(17) == Number(17)
```

and:

```text
Number(17) != Number(18)
```

Equality is based on the underlying `value`.

---

## Ordering

`Number` instances are naturally ordered by their numeric value.

For example:

```text
Number(5) < Number(12)
```

and:

```text
Number(90) > Number(1)
```

The ordering is deterministic and corresponds directly to the underlying integer values.

---

## Hashability

`Number` is hashable.

The hash is determined by the value represented by the Value Object.

Equal `Number` instances have equal hash values.

For example:

```text
hash(Number(5)) == hash(Number(5))
```

`Number` instances may therefore be used as members of sets and as dictionary keys.

---

## Immutability

`Number` is immutable after construction.

The underlying `value` cannot be modified after the instance has been created.

The Value Object therefore remains stable as a hashable and comparable domain value.

---

## String Representation

The canonical string representation contains the underlying numeric value:

```text
str(Number(7))
```

returns:

```text
7
```

The canonical representation returned by `repr()` is:

```text
repr(Number(7))
```

which returns:

```text
Number(7)
```

The representation reflects the Value Object type and its underlying value.

---

## Public API

The current public `Number` API consists of:

### Constructor

```text
Number(value: int)
```

### Property

```text
value -> int
```

Returns the underlying integer value.

### Method

```text
to_int() -> int
```

Returns the underlying integer value.

For example:

```text
Number(42).value == 42
Number(42).to_int() == 42
```

### Standard Value Object behaviour

`Number` also supports:

```text
Number(5) == Number(5)
Number(5) < Number(12)
hash(Number(5))
str(Number(7))
repr(Number(7))
```

These behaviours are part of the current Value Object contract.

---

## Boundary Values

The valid numeric boundaries are inclusive.

The following values are valid:

```text
1
90
```

The following values are invalid:

```text
0
91
```

The complete valid domain is therefore:

```text
1 <= value <= 90
```

---

## Error Conditions

The constructor raises `InvalidNumberError` when:

### Invalid type

The supplied value is not an integer.

Examples include:

```text
7.5
"7"
None
[]
{}
object()
```

### Invalid range

The supplied integer is outside the inclusive range `1..90`.

Examples include:

```text
0
-1
91
100
```

The exception type is:

```text
InvalidNumberError
```

---

## Dependencies

`Number` belongs to the Kernel Foundation.

It depends only on internal Kernel abstractions, including:

```text
ValueObject
InvalidNumberError
MIN_NUMBER
MAX_NUMBER
NumberValue
```

It must not depend on:

* persistence;
* infrastructure;
* repositories;
* analytics;
* external services.

---

## Public API Stability

The following members constitute the current public `Number` API:

```text
Number(value: int)

value
to_int()

__eq__()
__lt__()
__le__()
__gt__()
__ge__()
__hash__()
__str__()
__repr__()
```

The comparison and hashing behaviour is part of the Value Object contract.

Private validation helpers such as:

```text
_validate_type()
_validate_range()
```

are implementation details and are not part of the public API.

---

## Design Principle

`Number` is a Kernel Value Object.

It owns the invariants necessary to guarantee that every instance represents exactly one valid SuperEnalotto number.

The object is:

* immutable;
* deterministic;
* hashable;
* comparable;
* type-safe;
* independent of infrastructure concerns.

The `Number` Value Object provides the foundational numeric abstraction used by higher-level Kernel components such as `Combination` and domain objects.
