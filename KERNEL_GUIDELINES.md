# 004 — Kernel Guidelines

## Purpose

This document defines the architectural principles governing the SAE Kernel.

The Kernel is the stable foundation of the project.

Every new component added to the Kernel shall comply with the rules described in this document.

These guidelines have higher priority than implementation convenience.

---

# 1. Core Principles

The Kernel follows these fundamental principles:

* Single Responsibility Principle
* Explicit Domain Modeling
* Immutability by Default
* Composition over Inheritance
* No Premature Abstraction
* Explicit Dependencies
* Testability
* Deterministic Behaviour

---

# 2. Value Objects

All domain primitives are implemented as immutable Value Objects.

Rules:

* immutable (`frozen=True`)
* slot-based (`slots=True`)
* equality by value
* hashable
* deterministic behaviour
* self-validating

Every invariant belongs inside the Value Object.

Validation must never be delegated elsewhere.

---

# 3. Marker Base Classes

The Kernel defines semantic marker classes:

* ValueObject
* Entity
* AggregateRoot

These classes communicate architectural intent.

They intentionally contain no business logic.

---

# 4. Builder Framework

Builders exist only to simplify object construction.

Builders:

* collect construction data;
* never contain domain rules;
* never duplicate validation;
* always delegate validation to the constructed object;
* are reusable after `reset()`.

Builders are convenience objects, not domain objects.

---

# 5. Collections

Collections represent immutable mathematical structures.

Collections:

* preserve domain invariants;
* expose read-only behaviour;
* never expose mutable internal state.

---

# 6. Validation Rules

Validation always belongs to the object owning the invariant.

Incorrect:

* Builder validation
* external validator classes
* duplicated checks

Correct:

* constructor validation
* `__post_init__()`
* dedicated private validation methods

---

# 7. Primitive Types

Domain concepts should not expose primitive values directly.

Instead, they should use dedicated Value Objects whenever appropriate.

Primitive aliases are allowed only when they improve readability without introducing additional domain behaviour.

---

# 8. Dependency Rules

Dependencies are one-directional.

Foundation

↓

Collections

↓

Builders

↓

Domain

Higher layers may depend on lower layers.

Lower layers shall never depend on higher layers.

---

# 9. Immutability

Objects created by the Kernel are immutable unless explicitly documented otherwise.

Mutability must always be considered an exception.

---

# 10. Documentation

Every public module shall include:

* module documentation;
* class documentation;
* public API documentation.

Documentation evolves together with the code.

---

# 11. Testing

Every public component shall have corresponding unit tests.

Tests must be:

* deterministic;
* isolated;
* readable;
* independent.

The adopted naming convention is:

```
test_<expected_behavior>()
```

---

# 12. Repository Rules

Every milestone follows the same workflow:

1. implementation;
2. review;
3. repository certification;
4. commit.

Commits are performed only after the repository reaches a certified green state.

---

# 13. Long-Term Stability

The Foundation layer is considered stable.

Changes affecting:

* Foundation
* Builder Framework
* architectural contracts

should be introduced only through an explicit Repository Patch after architectural review.

---

# 14. Guiding Principle

The Kernel prioritises correctness, clarity and long-term maintainability over short-term convenience.

Every new contribution should strengthen these principles rather than weaken them.
