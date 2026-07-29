# DEV-002 — Testing Strategy

Status: Approved

---

# Purpose

This document defines the testing philosophy adopted by the SAE project.

Testing is considered an integral part of software engineering rather than a
verification activity performed after implementation.

Every component is expected to evolve together with its tests.

---

# Testing Principles

The project follows these principles:

- Behaviour over implementation.
- Regression prevention.
- Deterministic execution.
- Small independent tests.
- Fast feedback.

---

# Behaviour-Driven Testing

Tests describe observable behaviour.

GOOD

test_unsorted_input_is_sorted()

test_duplicate_numbers_are_rejected()

test_number_is_immutable()

BAD

test_sort()

test_set()

test_private_method()

Tests should explain what the software guarantees,
not how the implementation currently works.

---

# Unit Tests

Each Domain Object must have its own dedicated test module.

Example

tests/

    kernel/

        foundation/
            test_number.py

        collections/
            test_combination.py

---

# Coverage Policy

Kernel target:

100% statement coverage

The objective is to guarantee deterministic behaviour for all mathematical
components.

Infrastructure layers may adopt lower coverage targets when appropriate.

---

# Regression Tests

Every discovered bug must generate a regression test.

The regression test must fail before the fix and pass afterwards.

Bugs are not considered fixed until a regression test exists.

---

# Test Independence

Tests must never depend on execution order.

Tests must never share mutable state.

Each test must be executable independently.

---

# Fixtures

Use fixtures only when they improve readability.

Avoid complex fixture hierarchies.

Prefer explicit object construction.

---

# Property-Based Testing

Property-based tests may be introduced for mathematical components when they
provide additional confidence.

Examples include:

- ordering invariants

- uniqueness invariants

- combinatorial properties

---

# Performance Tests

Performance is not verified by unit tests.

Dedicated benchmark suites will be introduced separately.

---

# Naming Convention

Test names describe expected behaviour.

Recommended pattern:

test\_<behaviour>()

Examples

test_number_accepts_valid_value()

test_duplicate_numbers_are_rejected()

test_iteration_preserves_order()

---

# Repository Structure

Tests mirror the production code structure.

Example

src/

    sae/

        kernel/

            foundation/

            collections/

tests/

    kernel/

        foundation/

        collections/

This symmetry improves discoverability.

---

# Continuous Integration

Every Pull Request must execute:

- Ruff
- MyPy
- Pytest

No Pull Request may be merged if tests fail.

---

# Rule

A component is not considered complete until its tests are complete.
