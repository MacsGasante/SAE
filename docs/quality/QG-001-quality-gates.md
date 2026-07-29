# QG-001 — Quality Gates

Status: Approved

Owner: Repository

Applies to:

Entire Repository

---

# Purpose

This document defines the mandatory quality gates that every contribution must
satisfy before being accepted.

Quality gates protect repository stability and reduce technical debt.

---

# Mandatory Gates

The following commands must complete successfully.

make format

make lint

make typecheck

make test

make check

---

# Static Analysis

Static analysis must execute without errors.

Warnings should be treated as opportunities for improvement.

---

# Tests

All tests must pass.

No skipped tests are allowed without documented justification.

---

# Documentation

Public APIs require documentation.

Repository documentation must remain synchronized with implementation.

---

# Repository Integrity

A change is complete only when:

Specification

Implementation

Tests

Documentation

remain consistent.

---

# Rule

Quality gates are mandatory.

There are no exceptions.
