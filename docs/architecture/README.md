# Architecture Documentation

## Purpose

This section documents the software architecture of the SAE project.

Architecture documents describe how the system is organized, how the various layers interact, and which architectural rules must always be respected.

Unlike the project specifications, these documents focus on implementation architecture rather than business requirements.

## Current Architecture

SAE is organized into the following principal areas:

- **Kernel** — domain foundations, collections, builders, domain objects, and Dataset.
- **Analytics** — analytical engines operating on the Dataset, including Frequency, Delay, and Probability.
- **CLI** — application-facing command layer, currently providing C1 Basic Commands.
- **Infrastructure / Research** — future areas that must remain separated from the Kernel and analytical domain logic.

The current implemented analytical components are:

- A1 — Frequency Engine
- A2 — Delay Engine
- A3 — Probability Engine

The current implemented CLI components are:

- C1 — Basic Commands

The CLI provides the application-facing entry point for SAE and currently exposes basic informational commands.

Analytics consume domain data through explicit APIs and must not introduce dependencies from the Kernel back into Analytics.

## Architectural Rules

The architecture is governed by the following principles:

- Kernel independence from Analytics and infrastructure.
- Dataset integrity is enforced by the Dataset Aggregate Root.
- Analytics operate on immutable domain data.
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
