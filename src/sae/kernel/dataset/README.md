# Dataset Layer

## Purpose

The Dataset Layer contains the Aggregate Root representing the
complete immutable historical archive of SuperEnalotto draws.

The Dataset is responsible only for preserving archive integrity.

It is intentionally independent from:

- repositories
- analytics
- persistence
- statistics
- infrastructure

---

# Aggregate

The Dataset Aggregate owns directly an immutable collection of Draw objects.

Architecture:

Dataset
    ↓
tuple[Draw]

---

# Responsibilities

The Dataset guarantees:

- immutable storage
- chronological ordering
- unique Draw identifiers
- unique Draw dates
- deterministic construction

---

# Public API

The Dataset exposes:

Properties

- draws
- size
- first
- last

Python Collection Protocol

- len(dataset)
- iter(dataset)
- draw in dataset
- dataset[index]

---

# Invariants

The Dataset enforces:

- every element is a Draw
- DrawId uniqueness
- DrawDate uniqueness
- chronological ordering
- immutable storage

---

# Design Philosophy

The Dataset follows the same architectural principles adopted
throughout the Kernel:

- immutability
- deterministic behaviour
- reproducibility
- infrastructure independence

---

# References

DATASET_GUIDELINES.md

ADR-0004

Dataset Specification
