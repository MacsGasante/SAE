# QG-003 — Code Coverage

Status: Approved

---

## Repository-wide coverage

The repository-wide coverage gate is 97%, configured through
`[tool.coverage.report].fail_under` in `pyproject.toml`.

## Kernel coverage

The Kernel has a separate, stricter coverage requirement:

**Target coverage: 100%.**

The `make check` target must enforce this requirement independently of the
repository-wide threshold. After the complete test suite has generated the
coverage data, the Kernel-only report is checked with:

```bash
coverage report --include="src/sae/kernel/*" --fail-under=100
```

A successful repository-wide coverage result does not replace the Kernel
coverage check. Both thresholds must pass.

## Infrastructure

Coverage targets may vary according to the component and its responsibilities.

---

## Principles

Coverage is an indicator. It is not the objective.

Meaningful tests are preferred over artificially increasing coverage.

Coverage gaps should be addressed with tests that verify meaningful behavior,
not trivial tests added only to raise a percentage.

---

## Rule

Coverage must never be improved through trivial tests.

Repository confidence is more important than percentage.
