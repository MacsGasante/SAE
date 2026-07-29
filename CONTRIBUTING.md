# Contributing

Thank you for your interest in contributing to SAE.

---

# Development Principles

The project follows Domain-Driven Design principles.

Repository quality is considered as important as source code quality.

---

# Development Workflow

Every new component must follow:

1. Specification
2. Architecture Review
3. Implementation
4. Tests
5. Documentation
6. Freeze

---

# Quality Rules

Every contribution must:

- pass Ruff
- pass MyPy
- pass Pytest
- include documentation
- include tests

---

# Architecture

The Kernel is immutable by design.

Domain Objects never depend on infrastructure.

Builders convert external data into Domain Objects.

---

# Coding Style

- explicit is better than implicit
- immutable by default
- deterministic behaviour
- comprehensive documentation
- behaviour-driven tests
