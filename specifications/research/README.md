# Research Specifications

## Purpose

This section defines the functional contracts for SAE Research Modules.

Research specifications describe experimental behaviour, reproducibility, configuration, provenance, and research-specific results. They do not redefine the Kernel domain model or the existing Analytics contracts.

## Scope

Research is an application-level capability that consumes established SAE contracts to investigate hypotheses, simulations, statistical behaviour, and future experimental algorithms.

The initial research architecture is intentionally technology-neutral. External scientific or machine-learning libraries may be introduced later when a concrete module requires them.

## Specifications

- `experiment.md` — experiment identity, configuration, execution context, and reproducibility requirements.
- `research-module.md` — contract for an autonomous research module.
- `result.md` — contract for research-specific results and provenance.

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

These specifications define the R0 architectural foundation. They are intentionally implementation-neutral and will be refined through subsequent Research milestones.
