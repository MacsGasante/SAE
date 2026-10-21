# R3.1 — Research Reporting Core

Version: 0.1

Status: Implemented (R3.1)

---

## Purpose

Define a presentation boundary for `ResearchResult` values. Reporting preserves experiment provenance, payload, and execution metadata without adding statistical interpretation or modifying the existing Analytics reporting contracts.

## Model

`ResearchReport` is an immutable presentation model containing a title, `ResearchProvenance`, payload, and execution metadata. `build_research_report(result)` accepts a `ResearchResult` and carries its existing content into the report; it does not run a module or alter the result.

## Renderers

The Research reporting package provides deterministic text, JSON, and CSV renderers.

- Text output labels provenance, execution metadata, and payload as distinct sections.
- JSON output includes title, structured provenance, payload, and execution metadata.
- CSV output uses `section,key,value` records. Nested mappings and sequences are represented as compact JSON values instead of imposing a statistical schema on arbitrary Research payloads.

The report provenance includes experiment and module identity, module version, input fingerprint, result schema version, immutable configuration, and execution context including the random seed when present.

## Boundaries

Research reporting is separate from `sae.reporting`, which continues to present Analytics results. This milestone does not add CLI commands, persistence, new statistical logic, payload-specific visualizations, or dependencies.

## Verification

Tests cover preservation of provenance and payload and the three output formats, including the explicit seed and nested payload values.
