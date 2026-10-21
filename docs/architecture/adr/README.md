# Architecture Decision Records (ADR)

## Purpose

This directory contains the official Architecture Decision Records (ADR) of the SAE project.

An ADR documents a significant architectural decision together with its rationale and consequences.

ADRs are immutable historical records.

Once accepted, an ADR is never rewritten.

If an architectural decision changes, a new ADR supersedes the previous one.

---

## Lifecycle

Every ADR follows the lifecycle:

Proposed

↓

Accepted

↓

Superseded (optional)

---

## Naming Convention

ADR-0001-short-title.md

Examples:

ADR-0001-kernel-boundary.md

ADR-0002-number-storage.md

ADR-0003-domain-layer.md

ADR-0004-dataset-aggregate-root.md
ADR-0005-csv-import-boundary-and-domain-mapping.md
ADR-0006-reporting-boundary-and-rendering.md
ADR-0007-research-module-boundary-and-experiment-reproducibility.md

---

## Current ADRs

| ADR | Status | Description |
|------|--------|-------------|
| ADR-0004 | Accepted | Dataset Aggregate Root |
| ADR-0005 | Accepted | CSV Import Boundary and Domain Mapping |
| ADR-0006 | Accepted | Reporting Boundary and Rendering |
| ADR-0007 | Proposed | Research Module Boundary and Experiment Reproducibility |

---

## Rules

An ADR must contain:

- Context
- Decision
- Consequences
- Alternatives
- Related Documents

An ADR must never contain implementation details.

Implementation belongs to the source code.

Domain behaviour belongs to the specifications.

Project rules belong to the Guidelines.

---

## References

- `KERNEL_GUIDELINES.md`
- Architecture Documentation
