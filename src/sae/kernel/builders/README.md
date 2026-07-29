# Kernel Builders

## Purpose

Builders translate external representations into immutable Domain Objects.

They isolate parsing and construction logic from the Domain Model.

---

## Responsibilities

Builders are responsible for:

- Parsing external data
- Coordinating validation
- Constructing Domain Objects
- Converting primitive values

Business rules remain inside the Domain Model.

---

## Public API

No public builders are currently available.

The first implementation will be:

- CombinationBuilder

---

## Dependencies

Builders may depend on:

- Foundation
- Collections

Builders never introduce business logic.

Domain Objects never depend on Builders.

---

## Design Principles

- Explicit construction
- Safe conversions
- Separation of concerns
- Deterministic behaviour

---

## Future Extensions

Planned builders:

- CombinationBuilder
- DrawBuilder
- PredictionBuilder
- StatisticsBuilder
