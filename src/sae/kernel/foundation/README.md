# Kernel Foundation

## Purpose

The Foundation package provides the fundamental building blocks of the SAE
Kernel.

Every other Kernel package depends directly or indirectly on this package.

Foundation objects are immutable, deterministic and independent from any
external infrastructure.

---

## Responsibilities

The Foundation package is responsible for:

- Primitive immutable Value Objects
- Base abstractions
- Shared domain constants
- Common domain types
- Core validation rules

---

## Public API

Current public objects:

- ValueObject
- Number

Additional public objects will be introduced only when they represent reusable
domain concepts.

---

## Dependencies

Foundation is the lowest layer of the Kernel.

It must never depend on:

- Collections
- Builders
- Model
- Analytics
- Infrastructure

---

## Design Principles

- Immutable by default
- Deterministic behaviour
- Minimal public API
- Explicit validation
- Infrastructure independent

---

## Future Extensions

Examples of future Foundation objects:

- Probability
- Percentage
- Score
- Identifier
- Timestamp
