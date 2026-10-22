# Research Specifications

## Purpose

This section defines the functional contracts for SAE Research Modules.

Research specifications describe experimental behaviour, reproducibility, configuration, provenance, and research-specific results. They do not redefine the Kernel domain model or the existing Analytics contracts.

## Scope

Research is an application-level capability that consumes established SAE contracts to investigate hypotheses, simulations, statistical behaviour, and future experimental algorithms.

The initial research architecture is intentionally technology-neutral. External scientific or machine-learning libraries may be introduced later when a concrete module requires them.

## Specifications

- `experiment.md` — experiment identity, configuration, execution context, and reproducibility requirements.
- `experiment-context.md` — implemented R1.1 contracts for immutable experiment identity, configuration, and execution context.
- `research-module.md` — implemented R1.3 protocol and controlled execution boundary.
- `result.md` — implemented R1.2 contract for immutable research results and provenance.
- `monte-carlo.md` — initial R2 module for seeded simulation of independent six-number draws.
- `reporting.md` — R3.1 Research reporting model and text, JSON, and CSV renderers.
- `cli.md` — R3.2 seeded Monte Carlo CLI command and output contract.\n- `integration-validation.md` — R3.3 end-to-end validation requirements, output invariants, and documentation alignment.

## Architectural Boundary

Research Modules may consume:

- Kernel domain and Dataset APIs;
- public Analytics APIs;
- research-specific configuration and execution context.

Research Modules must not:

- modify Kernel contracts;
- modify Analytics contracts;
- introduce dependencies from Kernel to Research;
- introduce dependencies from Analytics to Research;
- treat experimental results as predictions or betting recommendations.

## Status

R0 established the architectural foundation. R1.1 implemented experiment identity, immutable configuration, and execution context. R1.2 implemented immutable research results and explicit provenance. R1.3 implements the ResearchModule protocol and validates controlled execution and result provenance. R2 introduces the first concrete Research Module, a seeded Monte Carlo simulation that reports properties of its simulated sample only. R3.1 adds a separate presentation boundary that preserves Research provenance, payload, and execution metadata in text, JSON, and CSV without adding statistical interpretation. R3.2 exposes the seeded Monte Carlo module through `sae research simulate`, requiring an explicit seed and supporting text, JSON, and CSV output. R3.3 validates the complete CLI-to-report pipeline, reproducibility, frequency invariants, output consistency, and documentation alignment.
