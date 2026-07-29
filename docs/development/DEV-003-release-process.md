# DEV-003 — Release Process

Status: Approved

---

# Purpose

This document defines the release lifecycle adopted by the SAE project.

The objective is to guarantee that every published version is reproducible,
verified and fully documented.

A release is an engineering milestone rather than a packaging operation.

---

# Release Lifecycle

Every component progresses through the following stages.

Draft

The specification is under discussion.

Approved

The specification has been accepted.

Implementation may begin.

Implemented

The implementation is complete.

Verified

The implementation passes all quality gates.

Documentation has been updated.

Frozen

The component becomes stable.

Future modifications require either:

- a documented bug fix
- a new architectural decision
- a new specification

---

# Quality Gates

Before a release, the following commands must succeed.

make format

make lint

make typecheck

make test

make check

No release may bypass a failed quality gate.

---

# Documentation Requirements

Every release must update, when applicable:

README.md

CHANGELOG.md

PROJECT_STATUS.md

ROADMAP.md

Relevant documentation under docs/

Architectural documentation

Specifications

---

# Versioning

The project follows Semantic Versioning.

MAJOR.MINOR.PATCH

Examples

0.1.0-alpha1

0.1.0-alpha2

0.1.0-beta1

0.1.0-rc1

0.1.0

0.2.0

1.0.0

---

# Pre-release Stages

Alpha

Core functionality under development.

Public API may change.

Beta

Features complete.

Testing and stabilization.

Release Candidate (RC)

No new features.

Only bug fixes.

Stable

Production-quality release.

---

# Release Checklist

Before publishing a release, verify:

- repository builds successfully
- all tests pass
- static analysis passes
- documentation is updated
- changelog is updated
- version number is updated
- release notes are prepared

---

# Git Workflow

Each release must be associated with:

- a dedicated Git tag
- a corresponding changelog entry
- a reproducible repository state

Tags follow the version number.

Examples

v0.1.0-alpha1

v0.1.0

v1.0.0

---

# Freeze Policy

Frozen components should not change.

Changes are allowed only for:

- verified defects
- security issues
- architectural evolution approved through an ADR

This policy minimizes technical debt and protects repository stability.

---

# Engineering Philosophy

Small, verified releases are preferred over large, infrequent releases.

Repository history should describe the evolution of the software clearly.

Every release should leave the repository in a better state than before.

---

# Rule

A release is complete only when:

Specification

Implementation

Tests

Documentation

all evolve together.
