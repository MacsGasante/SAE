# Architecture Documentation

## Purpose

This section documents the software architecture of the SAE project.

Architecture documents describe how the system is organized, how the various layers interact, and which architectural rules must always be respected.

Unlike the project specifications, these documents focus on implementation architecture rather than business requirements.

## Current Architecture

SAE is organized into the following principal areas:

- **Kernel** — domain foundations, collections, builders, domain objects, and Dataset.
- **Analytics** — analytical engines operating on the Dataset, including Frequency, Delay, and Probability.
- **CLI** — application-facing command layer, providing C1 Basic Commands and C3 Reporting commands.
- **Infrastructure** — external adapters, including the CSV Dataset Importer boundary.
- **Reporting** — application-facing report model, builders, and dedicated text, JSON, and CSV renderers.
- **Research** — future area that must remain separated from the Kernel and analytical domain logic.

The current implemented analytical components are:

- A1 — Frequency Engine
- A2 — Delay Engine
- A3 — Probability Engine

The current implemented CLI components are:

- C1 — Basic Commands
- C3 — Reporting: `sae report <frequency|delay|probability> <dataset.csv> [--format text|json|csv]` (text is the default)

The current implemented Infrastructure component is:

- C2 — CSV Dataset Importer

The CLI provides the application-facing entry point for SAE. Its reporting command imports a CSV Dataset, invokes the selected Analytics engine, builds a presentation-neutral report, and delegates output to a dedicated renderer.

The CSV Dataset Importer translates the official CSV representation into domain objects and Dataset instances while keeping CSV-specific concerns outside the Kernel.

Analytics consume domain data through explicit APIs and must not introduce dependencies from the Kernel back into Analytics.

## Architectural Rules

The architecture is governed by the following principles:

- Kernel independence from Analytics and infrastructure.
- Dataset integrity is enforced by the Dataset Aggregate Root.
- Analytics operate on immutable domain data.
- External representations are translated at infrastructure boundaries rather than introduced into the Kernel.
- Cross-layer dependencies must respect the established direction of the architecture.
- Architectural decisions are recorded in ADRs.
- Accepted ADRs are immutable historical records.

## Typical Contents

Examples include:

- Package layout
- Layering
- Dependency rules
- Module organization
- Repository structure
- Architectural conventions
- Architecture Decision Records

## Audience

- Core developers
- Contributors
- Maintainers

## Status

This section evolves together with the project architecture.

For the current implementation status, see `PROJECT_STATUS.md` and `ROADMAP.md`.
