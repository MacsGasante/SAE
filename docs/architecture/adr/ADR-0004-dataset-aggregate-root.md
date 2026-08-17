# ADR-0004

Title

Dataset Aggregate Root

Status

Accepted

Date

2026-08-01

---

# Context

During the design of the Dataset Layer an intermediate DrawCollection abstraction was proposed.

Architecture:

Dataset
    ↓
DrawCollection
    ↓
tuple[Draw]

A design review showed that DrawCollection introduced no additional domain behaviour.

Its responsibilities would have duplicated those of Dataset.

---

# Decision

The DrawCollection abstraction is removed.

The Dataset becomes the Aggregate Root.

Architecture:

Dataset
    ↓
tuple[Draw]

---

# Consequences

Positive

- fewer abstractions
- simpler API
- fewer forwarding methods
- clearer Aggregate ownership
- lower maintenance cost

Negative

- Dataset becomes responsible for collection invariants

This responsibility is considered appropriate for an Aggregate Root.

---

# Alternatives Considered

Alternative A

Dataset
    ↓
DrawCollection
    ↓
tuple[Draw]

Rejected.

Reason:

Unnecessary abstraction.

---

# Future Evolution

Metadata will be introduced through a dedicated DatasetMetadata Value Object.

Architecture:

Dataset
│
├── tuple[Draw]
└── DatasetMetadata

No DrawCollection layer shall be introduced.

---

# Related Documents

005_DATASET_GUIDELINES.md

Dataset Specification

004_KERNEL_GUIDELINES.md
