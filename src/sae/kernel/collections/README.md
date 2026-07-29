# Kernel Collections

## Purpose

Collections represent immutable groups of Domain Objects.

A Collection expresses domain semantics that cannot be represented by a simple
Python container.

---

## Responsibilities

Collections are responsible for:

- Cardinality validation
- Ordering guarantees
- Duplicate detection
- Immutable storage
- Collection semantics

---

## Public API

Current public objects:

- Combination

---

## Dependencies

Collections may depend only on Foundation.

Collections never depend on:

- Builders
- Model
- Analytics
- Infrastructure

---

## Design Principles

- Immutable
- Ordered
- Deterministic
- Domain-oriented
- Explicit invariants

---

## Future Extensions

Examples include:

- DrawNumbers
- NumberSet
- WheelNumbers
- PredictionSet
