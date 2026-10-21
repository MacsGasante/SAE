# Research Experiment Context

Version: 0.1

Status: Implemented (R1.1)

R1.1 introduces the immutable context objects needed to identify a research
execution before the Research Module and Research Result contracts are
implemented.

- Experiment identifies the experiment, module and version, input fingerprint,
  immutable configuration, and execution context.
- ExperimentConfiguration accepts JSON-compatible values, defensively copies
  them, exposes nested read-only mappings and tuples, and provides deterministic
  JSON serialization.
- ExecutionContext explicitly records an optional non-negative integer random
  seed. Randomized modules are responsible for requiring a seed when executing.

The experiment stores an input fingerprint rather than a Dataset instance. This
keeps the experiment identity independent of the input adapter and leaves the
Dataset itself unchanged.

## Scope

This milestone does not execute modules, calculate input fingerprints, define
ResearchResult, persist experiments, or add CLI/reporting/ML dependencies.
