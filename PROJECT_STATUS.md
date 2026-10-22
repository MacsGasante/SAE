# SAE Project Status

**Repository:** SAE — SuperEnalotto Analytics Engine

Current Version:

> v0.1.0-alpha1

---

# Overall Status

| Area       | Status |
| ---------- | ------ |
| Repository | 🟡 Engineering |
| Kernel     | 🟢 Frozen |
| Analytics  | 🟢 Implemented |
| CLI        | 🟢 Implemented |
| Research   | 🟡 R4.1 methodology in review |

---

# Functional Milestones

| Milestone          | Status |
| ------------------ | ------ |
| M0                 | ✅ Frozen |
| M1.1 — Number      | ✅ Frozen |
| M1.2 — Combination | ✅ Frozen |
| M1.3 — Builders    | ✅ Frozen |
| M1.4 — Domain      | ✅ Frozen |
| M1.5 — Dataset     | ✅ Verified |
| M1.6 — Analytics   | ✅ Implemented |

---

# Analytics Components

| Component          | Status |
| ------------------ | ------ |
| A1 — Frequency     | ✅ Implemented |
| A2 — Delay         | ✅ Implemented |
| A3 — Probability   | ✅ Implemented |

---

# CLI Milestones

| Milestone                     | Status |
| ----------------------------- | ------ |
| C1 — Basic Commands           | ✅ Implemented |
| C2 — Import Tools             | ✅ Implemented |
| C3.1 — Reporting core         | ✅ Complete |
| C3.2 — CLI reporting          | ✅ Complete |
| C3.3 — JSON and CSV formats   | ✅ Complete |
| C3.4 — End-to-end integration | ✅ Complete |

---

# Research Milestones

| Milestone | Status |
| --------- | ------ |
| R0 — Research architecture | ✅ Complete |
| R1.1 — Experiment and execution context | ✅ Complete |
| R1.2 — Research result and provenance | ✅ Complete |
| R1.3 — Module contract and controlled execution | ✅ Complete |
| R2 — First concrete research module | ✅ Implemented |
| R3.1 — Research reporting core | ✅ Complete |
| R3.2 — Research CLI integration | ✅ Complete |
| R3.3 — End-to-end integration and validation | ✅ Complete |
| R4.1 — Historical frequencies vs null model | 🟡 Methodology in review |

R2 provides `MonteCarloDrawSimulation`, a seeded simulation of independent six-number draws. It requires an explicit random seed, validates its draw-count configuration, and returns an immutable result with provenance. It does not consume historical Dataset data, predict official draws, or recommend bets.

R3.1 adds a dedicated Research reporting model and text, JSON, and CSV renderers. R3.2 exposes the simulation through `sae research simulate`, with an explicit seed, configurable draw count, and the same three output formats. Research reporting remains separate from the Analytics reporting API.

R3.3 is complete: the end-to-end CLI-to-module-to-result-to-report path is covered by integration tests for reproducibility, seed/configuration provenance, frequency invariants, and CSV title preservation. The PR and post-merge CI passed.

R4.1 defines a proposed omnibus comparison between historical marginal frequencies and a null model of independent uniform six-of-90 draws. Its methodology is documented for review before implementation; no historical hypothesis test is claimed as implemented.

---

# Engineering Milestones

| Milestone                       | Status |
| ------------------------------- | ------ |
| E1 — Repository Consolidation   | 🟡 In Progress |
| E2 — Development Infrastructure | 🟡 In Progress |

---

# Kernel Components

| Component   | Status |
| ----------- | ------ |
| Foundation  | ✅ Frozen |
| Collections | ✅ Frozen |
| Builders    | ✅ Frozen |
| Domain      | ✅ Frozen |
| Dataset     | ✅ Verified |

---

# Quality Gates

| Gate                   | Status |
| ----------------------- | ------ |
| Ruff                   | ✅     |
| MyPy                   | ✅     |
| Pytest                 | ✅     |
| Overall Coverage ≥ 97% | ✅     |
| Kernel Coverage = 100%  | ✅     |
| GitHub Actions         | ✅     |
| Documentation          | 🟡 R4.1 methodology proposal added; implementation pending |

---

# Current Focus

R4.1 is in methodology review. The immediate goal is to agree on a pre-specified omnibus statistic and a valid Monte Carlo null distribution before implementing the historical-data experiment. Kernel and Analytics contracts remain frozen; no implementation or statistical result is claimed yet.

The full quality pipeline is run through `make check`. Local checks are not claimed unless actually executed.

Last update:

C3 Reporting and Research R0–R3.3 are complete. R4.1 — Historical Frequencies vs Theoretical Null Model — is the active research design proposal; implementation, runtime benchmarking, and end-to-end validation remain pending.
