# SAE Documentation

This document provides the entry point to the complete SAE documentation.

Documentation is organized by purpose rather than by directory.

---

# Project Documentation

Repository-level documentation.

* README.md
* DOCUMENTATION.md
* KERNEL_GUIDELINES.md
* DATASET_GUIDELINES.md
* PROJECT_STATUS.md
* ROADMAP.md
* CHANGELOG.md
* CONTRIBUTING.md

---

# Architecture

Architecture-related documentation is available under:

docs/architecture/

The architecture section includes the architectural overview and Architecture Decision Records (ADRs).

---

# Engineering

Development practices are documented here.

* DEV-001 — Coding Standards
* DEV-002 — Testing Strategy
* DEV-003 — Release Process

Location:

docs/development/

---

# Quality

Quality standards and engineering gates.

Location:

docs/quality/

---

# Architectural Decisions

All Architectural Decision Records (ADR) are indexed under:

docs/architecture/adr/

Accepted ADRs are immutable historical records.

---

# Glossary

Shared terminology used throughout the project.

Location:

docs/glossary/

---

# User Documentation

Documentation intended for end users.

Location:

docs/user-guide/

---

# Kernel Documentation

Package-level documentation is available inside:

* src/sae/kernel/foundation/
* src/sae/kernel/collections/
* src/sae/kernel/builders/
* src/sae/kernel/domain/
* src/sae/kernel/dataset/

---

# Analytics Documentation

Analytics components are implemented under:

* src/sae/analytics/frequency/
* src/sae/analytics/delay/
* src/sae/analytics/probability/

Analytics specifications and architecture rules remain separate from the Kernel.

---

# Specifications

Specifications are organized by architectural and functional scope.

Locations:

* specifications/kernel/
* specifications/domain/
* specifications/dataset/

Analytics currently follows the established architecture and implementation contracts documented by the corresponding source modules and tests.

---

# Documentation Principles

Documentation follows these principles:

* Single Responsibility
* Explicit ownership
* Version controlled
* Incremental evolution
* Repository is the single source of truth

Documentation is considered part of the software and evolves together with the code.
