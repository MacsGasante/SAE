# DEV-001 — Coding Standards

Status: Approved

---

# Purpose

This document defines the coding standards adopted by the SAE project.

The objective is consistency, readability, maintainability and long-term
stability.

These standards apply to every module of the repository.

---

# General Principles

The project follows these principles:

- Readability over cleverness.
- Explicit over implicit.
- Simplicity over premature optimization.
- Immutability by default.
- Deterministic behaviour.

---

# Python Version

Minimum supported version:

Python 3.12

---

# Formatting

Formatting is delegated to Ruff.

No manual formatting conventions should conflict with Ruff.

---

# Type Hints

All public APIs must be fully typed.

Avoid using Any.

Prefer explicit domain types.

Example:

GOOD

Number

Combination

Probability

instead of

int

tuple

float

whenever a dedicated domain object exists.

---

# Docstrings

Public modules

Public classes

Public methods

must include docstrings.

Private methods may omit documentation if they are self-explanatory.

---

# Exceptions

Never raise generic Exception.

Always define domain-specific exceptions.

GOOD

InvalidNumberError

InvalidCombinationError

BAD

ValueError

Exception

except for infrastructure adapters.

---

# Immutability

Domain Objects are immutable.

Collections are immutable.

Builders are mutable services only if required.

---

# Naming

Class names:

PascalCase

Functions:

snake_case

Variables:

snake_case

Constants:

UPPER_CASE

Private members:

\_leading_underscore

---

# Imports

Standard library

Third-party

Local imports

One blank line between groups.

---

# Public API

Every package explicitly exposes its public API through **init**.py.

Internal modules are not considered stable.

---

# Dependencies

Dependencies always point downward.

Higher layers may depend on lower layers.

Lower layers never depend on higher layers.

---

# Rule

If a rule is not explicitly defined here,

prefer the simplest solution.
