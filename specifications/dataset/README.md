# Dataset Specifications

The Dataset Layer represents the immutable historical archive of
official SuperEnalotto draws.

The Dataset Layer belongs to the Kernel because it models domain
concepts and does not depend on infrastructure, persistence,
analytics or presentation.

The Dataset Layer provides immutable collections of Draw objects
together with a stable public API for future analytics modules.

---

## Components

- DrawCollection
- Dataset

---

## Design Goals

- Immutable
- Ordered
- Deterministic
- Infrastructure-independent
- Analytics-independent

---

## Non Goals

The Dataset Layer does not:

- read CSV files;
- parse external formats;
- connect to databases;
- perform statistical analysis;
- calculate frequencies or delays.

Those responsibilities belong to Infrastructure and Analytics.

---

## Dependency Graph

Dataset

↓

DrawCollection

↓

Draw

↓

Combination

↓

Number
