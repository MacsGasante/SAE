# SAE Roadmap

This document describes the long-term evolution of the project.

---

# Functional Roadmap

## Kernel

- M1.1 Number ✅
- M1.2 Combination ✅
- M1.3 Builders ✅
- M1.4 Domain ✅
- M1.5 Dataset ✅
- M1.6 Analytics ✅

---

## Analytics

- A1 Frequency Engine ✅
- A2 Delay Engine ✅
- A3 Probability Engine ✅

---

## CLI

- C1 Basic Commands ✅
- C2 Import Tools ✅
- C3 Reporting
  - C3.1 Reporting core ✅
  - C3.2 CLI reporting ✅
  - C3.3 JSON and CSV output formats ✅
  - C3.4 End-to-end integration and validation ✅

---

## Research

### R0 — Research Architecture ✅

- Establish Research as an application-level consumer of Kernel/Dataset and Analytics.
- Define module boundaries, experiment reproducibility, and evidence interpretation.
- Keep Research results distinct from Analytics results.

### R1 — Research Core

- R1.1 Experiment identity, immutable configuration, and execution context ✅
- R1.2 Immutable ResearchResult and provenance ✅
- R1.3 ResearchModule protocol and controlled execution ✅

### R2 — First Concrete Research Module

- Seeded Monte Carlo simulation of independent six-number draws ✅
- Explicit configuration, seed handling, immutable result payload, and provenance ✅
- Reproducibility and input/configuration validation tests ✅

### R3 — Research Reporting and CLI ✅

- R3.1 Research reporting model and text/JSON/CSV renderers ✅
- R3.2 Research CLI integration ✅
- R3.3 End-to-end integration, validation, and documentation ✅
  - Verified reproducibility and provenance through the CLI-to-report pipeline.
  - Added end-to-end assertions for result invariants and seed/configuration provenance.
  - Preserved the report title in CSV and aligned project documentation.
- Research reporting remains separate from Analytics reporting.
- `sae research simulate` exposes the seeded Monte Carlo module with explicit seed, configurable draw count, and text/JSON/CSV output.

### R4 — Advanced Research (active)

- **R4.1 — Historical Frequencies vs Theoretical Null Model: implementation added; CI review pending.**
  - Compares historical marginal frequencies with independent uniform six-of-90 draws using the pre-specified maximum absolute standardized-deviation statistic.
  - Estimates the null distribution through seeded complete-draw simulations and reports the finite-simulation Monte Carlo p-value.
  - Records the canonical Dataset fingerprint, seed, replicate count, and Research provenance.
  - CLI: `sae research historical-test <csv> --seed <integer> --replicate-count <positive integer> [--format text|json|csv]`.
  - No default replicate count is set until a representative historical-data runtime benchmark is completed.
- Implementation must not modify Kernel or Analytics contracts.
- Research outputs must not be framed as predictions or betting recommendations.
---

# Engineering Roadmap

## E1

Repository Consolidation

## E2

Development Infrastructure

- GitHub Actions ✅
- Coverage ✅
- Pre-commit ✅
- Release Automation

## E3

Repository Automation

- Metadata generation
- Documentation generation
- Dashboard
- Badges
