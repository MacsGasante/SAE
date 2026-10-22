# R3.2 — Research CLI Integration

Version: 0.1

Status: Implemented (R3.2)

---

## Purpose

Expose the existing seeded Monte Carlo Research Module through the SAE command-line interface without changing Analytics commands or Research contracts.

## Command

`sae research simulate --seed <integer> [--draw-count <integer>] [--format <text|json|csv>]`

- `--seed` is required and must be a non-negative integer.
- `--draw-count` is optional, defaults to 10000, and must be a positive integer.
- `--format` accepts `text`, `json`, or `csv`; text is the default.
- The command uses the theoretical independent six-of-90 model and does not import a historical Dataset.
- The selected Research report renderer preserves provenance, configuration, execution metadata, and the simulation payload.

## Reproducibility

The command supplies the explicit seed through `ExecutionContext`, configures the module with the requested draw count, and delegates execution to `execute_research_module`. The experiment identifier is derived deterministically from the seed and draw count.

## Boundaries

This command reports a simulated sample. It does not predict official future draws or recommend bets. It does not change the existing `sae report` Analytics command, add persistence, or introduce statistical interpretation.

## Verification

CLI tests cover all three output formats, preservation of seed and draw-count metadata, required seed handling, and invalid numeric arguments.
