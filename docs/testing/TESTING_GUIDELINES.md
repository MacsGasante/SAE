# SAE Testing Guidelines

Version: 1.0 (Freeze)

---

# Purpose

This document defines the official testing conventions adopted by the SAE project.

The objective is to guarantee:

- consistency;
- readability;
- maintainability;
- deterministic behaviour;
- long-term evolution.

All Kernel tests MUST follow these conventions.

---

# General Principles

Tests verify the public behaviour of the Domain Model.

Tests never verify implementation details.

Tests should remain stable even if the internal implementation changes.

---

# Public API Only

Tests MUST interact only with the public API.

Never test:

- private methods;
- private attributes;
- implementation details.

Good:

```python
dataset.first
```

Bad:

```python
dataset._draws
dataset._validate()
```

---

# One Responsibility Per Test

Each test verifies exactly one behaviour.

Good:

```python
test_duplicate_draw_id_raises()
```

Bad:

```python
test_duplicate_draw_id_and_sorting()
```

---

# Arrange / Act / Assert

Whenever possible tests follow the classic structure.

```text
Arrange

Act

Assert
```

The sections are not explicitly commented unless clarity requires it.

---

# Factory Fixtures

Objects are created through pytest factory fixtures.

Example:

```python
def test_example(
    make_draw: DrawFactory,
) -> None:
```

Factories are defined in:

```text
tests/kernel/conftest.py
```

---

# Type Aliases

All fixture signatures use shared type aliases.

Location:

```text
tests/kernel/types.py
```

Example:

```python
from tests.kernel.types import DrawFactory
```

Never write long Callable[...] signatures inside test files.

---

# Aggregate Test Layout

Each Aggregate Root owns one directory.

Example:

```text
tests/kernel/dataset/
```

Recommended structure:

```text
test_<aggregate>_construction.py

test_<aggregate>_validation.py

test_<aggregate>_collection_protocol.py

test_<aggregate>_properties.py
```

---

# Construction Tests

Construction tests verify:

- valid creation;
- ordering;
- default state.

---

# Validation Tests

Validation tests verify:

- domain invariants;
- exception types;
- invalid inputs.

Validation tests verify exception classes, not exception messages.

---

# Collection Protocol Tests

Collection tests verify Python protocol behaviour.

Typical examples:

- len()
- bool()
- iteration
- reversed()
- contains
- getitem

---

# Property Tests

Property tests verify read-only API.

Typical examples:

- first
- last
- draws
- size
- count
- is_empty

---

# Assertions

Prefer explicit assertions.

Example:

```python
assert dataset.size == 1
assert dataset.count == 1
assert len(dataset) == 1
```

Instead of checking only one equivalent property.

---

# Immutability

Whenever an object is expected to be immutable, tests should verify observable immutability through the public API.

Implementation details are irrelevant.

---

# Equality

Equality tests verify semantic equality.

Hash consistency should be verified whenever equality is implemented.

---

# Ordering

Whenever a collection guarantees ordering, ordering must be explicitly verified.

Never assume insertion order unless it is part of the contract.

---

# Documentation

Every test module starts with a module docstring.

Every test function has a short descriptive docstring.

---

# Naming

Tests follow the pattern:

```text
test_<expected_behaviour>()
```

Examples:

```text
test_duplicate_draw_id_raises()

test_dataset_is_sorted_by_date()

test_first_returns_oldest_draw()
```

---

# Freeze

These conventions are frozen starting from Kernel Milestone M1.5.

Future Kernel tests should follow this document unless superseded by a newer version.
