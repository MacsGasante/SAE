# R3.3 — Research End-to-End Integration Validation

Version: 0.1

Status: In progress

---

## Purpose

Validate the integration of the first Research Module through the application boundary:

`MonteCarloDrawSimulation → execute_research_module → ResearchResult → ResearchReport → renderer → CLI`.

This milestone does not introduce a new research algorithm or statistical interpretation.

## Validation Requirements

- The CLI requires an explicit non-negative random seed and accepts a positive draw count.
- The experiment configuration and random seed remain available in report provenance and execution metadata.
- Repeating the same module version, seed, and configuration produces identical structured output.
- The number-frequency payload contains exactly the number domain 1 through 90, and the frequency total equals six times the draw count.
- Text, JSON, and CSV are supported without changing the existing Analytics `sae report` command or reporting package.
- Each format retains the report title, provenance, payload, and execution metadata; nested CSV values use compact JSON where appropriate.
- README, project status, roadmap, and Research specifications describe the implemented functionality and milestone status consistently.

## Boundaries

The Monte Carlo module consumes no historical Dataset. It describes a simulated theoretical sample, not official future draws. Research remains separate from the Kernel and Analytics layers and does not provide betting recommendations.

## Verification

Automated tests exercise the CLI-to-module-to-result-to-report path, reproducibility, seed/configuration provenance, frequency invariants, and CSV title preservation. The milestone is complete only after the GitHub CI quality workflow passes on the pull request and the merge commit.
