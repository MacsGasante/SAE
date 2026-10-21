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

### R3 — Research Reporting and CLI

- R3.1 Research reporting model and text/JSON/CSV renderers ✅
- R3.2 Research CLI integration ⏳
- R3.3 End-to-end integration, validation, and documentation ⏳
- Present Research results and provenance through an explicit reporting boundary.
- Add CLI integration only after the result and module contracts are stable.

### R4 — Advanced Research

- Evaluate additional statistical, probabilistic, numerical, or machine-learning approaches only when justified by concrete research questions.
- Keep optional research dependencies behind the Research boundary.

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
