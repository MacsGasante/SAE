# Contributing

Thank you for your interest in contributing to SAE.

SAE is an open-source research and engineering project. Contributions are
welcome in software development, testing, documentation, architecture,
and statistical or probabilistic research.

The goal is to make every contribution useful, reproducible, and
consistent with the project's architecture and engineering principles.

---

# Ways to Contribute

There are several ways to contribute to SAE.

## Code

Contributions may include:

- Domain Model improvements
- Dataset functionality
- Query functionality
- Analytics components
- CLI functionality
- test improvements
- performance improvements
- development tooling

Production-code contributions must respect the SAE architecture and
quality gates.

## Documentation

Documentation contributions are equally valuable.

Examples include:

- improving existing documentation;
- correcting inconsistencies;
- adding usage examples;
- improving specifications;
- improving architecture documentation;
- improving the glossary;
- improving contributor documentation.

Documentation-only contributions do not require changes to production
code.

## Research

SAE is also a research project.

Research contributions may include:

- statistical analysis;
- probability models;
- combinatorial analysis;
- hypothesis formulation;
- hypothesis validation;
- experimental algorithms;
- research documentation.

Research contributions should clearly distinguish between established
results, hypotheses, experiments, and conclusions.

---

# Before You Start

Before starting work:

1. Read the `README.md`.
2. Review the relevant project documentation.
3. Check the existing GitHub Issues.
4. Check the `ROADMAP.md` when the contribution concerns planned work.
5. For architectural changes, review the relevant Architecture
   documentation and Architectural Decision Records.

For a first contribution, prefer issues labelled:

- `good first issue`

Issues labelled:

- `help wanted`

may require a deeper understanding of the project.

If you are unsure whether a proposed contribution fits the project,
open an issue before implementing it.

---

# Development Principles

The project follows Domain-Driven Design principles.

Repository quality is considered as important as source code quality.

SAE follows these core principles:

- specification before implementation;
- explicit architecture;
- immutable domain objects where appropriate;
- deterministic behaviour;
- reproducible research;
- test-first development;
- documentation as code;
- incremental and reviewable changes.

---

# Development Workflow

New components should normally follow:

1. Specification
2. Architecture Review
3. Implementation
4. Tests
5. Documentation
6. Freeze

Not every contribution requires all six stages independently.

For example, documentation-only contributions may require only
specification/documentation review.

When modifying an existing component, contributors should first inspect
the current implementation, tests, and documentation before making
changes.

---

# Choosing an Issue

When possible, start from an existing GitHub Issue.

Before beginning work, make sure you understand:

- the problem being addressed;
- the intended scope;
- the acceptance criteria;
- the affected components;
- any dependencies.

Do not expand the scope of an issue unnecessarily.

If additional problems are discovered during implementation, document
them and consider opening a separate issue.

This keeps contributions focused and easier to review.

---

# Good First Issues

Issues labelled `good first issue` are intended to provide a clear entry
point for contributors who are new to SAE.

A good first issue should normally:

- have a clearly defined scope;
- provide acceptance criteria;
- identify relevant files or areas;
- avoid unnecessary architectural decisions;
- be independently reviewable.

Good first issues may involve code, tests, or documentation.

You do not need to modify production code to make a meaningful first
contribution.

---

# Development Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

Install the project and development dependencies:

```bash
make bootstrap
```

---

# Development Commands

Run the test suite:

```bash
make test
```

Run linting:

```bash
make lint
```

Format the code:

```bash
make format
```

Run static type checking:

```bash
make typecheck
```

Run the complete quality check:

```bash
make check
```

A contribution that modifies Python source code should pass:

```bash
make check
```

before being submitted for review.

---

# Quality Rules

Every production-code contribution must:

- pass Ruff;
- pass MyPy;
- pass Pytest;
- include appropriate tests;
- include documentation when behaviour or public APIs change.

Tests should primarily verify observable behaviour and domain contracts
rather than implementation details.

Documentation and specification changes must remain consistent with the
current implementation.

---

# Architecture

The Kernel is immutable by design.

Domain Objects never depend on infrastructure.

Builders convert external data into Domain Objects.

The Dataset layer is responsible for maintaining the integrity of the
historical Draw collection.

Contributors making changes involving Dataset, Query, or Analytics should
review the relevant Architecture documentation and Architectural Decision
Records before implementation.

---

# Pull Requests

Pull Requests should be focused and reviewable.

A Pull Request should normally:

- address one issue or a clearly related group of changes;
- explain what was changed;
- explain why the change was necessary;
- include tests when behaviour changes;
- update documentation when required;
- avoid unrelated refactoring.

Before opening a Pull Request, run:

```bash
make check
```

The Pull Request description should reference the relevant GitHub Issue.

For example:

```bash
Closes #123
```

---

# Pull Request Review

Contributions are reviewed for:

- correctness;
- architectural consistency;
- test coverage;
- documentation consistency;
- maintainability;
- adherence to project conventions.

Passing automated checks is necessary but does not by itself guarantee
acceptance.

Architectural changes may require additional discussion before merging.

---

# Coding Style

- explicit is better than implicit;
- immutable by default;
- deterministic behaviour;
- comprehensive documentation;
- behaviour-driven tests;
- small and focused changes;
- clear public APIs.

Use the project's configured formatting and linting tools rather than
introducing personal formatting conventions.

---

# Documentation Changes

Documentation is part of the software.

When changing a public API, architectural decision, invariant, or
observable behaviour, review the corresponding documentation and
specifications.

Avoid duplicating the same source of truth across multiple documents.

When documentation conflicts with the current implementation, do not
silently choose one interpretation. Raise the inconsistency for review.

---

# Research Contributions

Research contributions should be reproducible whenever practical.

A research contribution should clearly identify:

- the research question;
- the hypothesis, if applicable;
- the data used;
- the methodology;
- the experiment;
- the results;
- the limitations.

SAE does not treat experimental or predictive techniques as guarantees
of future lottery outcomes.

Research results should distinguish between empirical observations,
interpretations, and hypotheses.

---

# Questions and Proposals

If you are unsure about an architectural, research, or implementation
decision, open a GitHub Issue before making a large change.

For substantial architectural changes, explain:

- the problem;
- the proposed solution;
- alternatives considered;
- expected impact.

Small, focused contributions are preferred over large unsolicited
refactors.

---

# Thank You

Every contribution helps improve SAE.

Whether you contribute code, tests, documentation, architecture,
research, or simply identify a problem, your contribution is valuable.

Thank you for helping make SAE a more rigorous, reproducible, and
maintainable open-source project.
