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
| Research   | 🟡 R4.1 implemented; historical-data benchmark pending |

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
| R4.1 — Historical frequencies vs null model | 🟡 Merged; CI green; benchmark pending |

R2 provides `MonteCarloDrawSimulation`, a seeded simulation of independent six-number draws. It requires an explicit random seed, validates its draw-count configuration, and returns an immutable result with provenance. It does not consume historical Dataset data, predict official draws, or recommend bets.

R3.1 adds a dedicated Research reporting model and text, JSON, and CSV renderers. R3.2 exposes the simulation through `sae research simulate`, with an explicit seed, configurable draw count, and the same three output formats. Research reporting remains separate from the Analytics reporting API.

R3.3 is complete: the end-to-end CLI-to-module-to-result-to-report path is covered by integration tests for reproducibility, seed/configuration provenance, frequency invariants, and CSV title preservation. The PR and post-merge CI passed.

R4.1 now includes `HistoricalFrequencyNullModel`, a seeded Monte Carlo test comparing historical marginal frequencies against independent uniform six-of-90 draws. It reports the maximum absolute standardized deviation, exceedance count, finite-simulation p-value, observed frequencies, canonical Dataset fingerprint, seed, replicate count, and provenance. The CLI supports text, JSON, and CSV. The replicate count is required explicitly; no default is set until a representative historical Dataset benchmark is completed. PR #31 is merged and the post-merge GitHub Actions workflow passed. A runtime benchmark on the user's representative historical Dataset remains pending because no historical CSV is committed in the repository.

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
| Documentation          | 🟡 R4.1 implementation documented; benchmark procedure pending |

---

# Current Focus

R4.1 implementation is merged into `main` and verified by green post-merge CI. The historical-data test uses a pre-specified omnibus statistic and a seeded Monte Carlo null distribution. Kernel and Analytics contracts remain unchanged. No conclusion about the official historical Dataset is claimed until the CLI is run on that Dataset and its result is reviewed.

The full quality pipeline is run through `make check`. Local checks are not claimed unless actually executed.

Last update:

C3 Reporting and Research R0–R3.3 are complete. R4.1 — Historical Frequencies vs Theoretical Null Model — has an initial implementation and CLI integration; Only the representative historical-data runtime benchmark remains pending.
