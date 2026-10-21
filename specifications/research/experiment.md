# Research Experiment Specification

Version: 0.1

Status: Proposed

---

## Purpose

An Experiment is the explicit unit of execution for a Research Module.

An experiment captures enough context to identify what was executed, with which inputs and configuration, and under which reproducibility conditions.

## Experiment Context

An experiment must identify:

- the Research Module being executed;
- the input Dataset or other declared research input;
- the experiment configuration;
- the execution context relevant to reproducibility;
- the resulting Research Result.

The experiment context must be explicit. A module must not rely on hidden mutable global state to define experimental behaviour.

## Configuration

Experiment configuration contains the parameters that determine the module's behaviour.

Configuration is immutable for the duration of an experiment.

A configuration must be serializable into a stable representation suitable for provenance. The exact serialization format is an implementation concern and must not alter the semantic contract.

## Randomness and Seed

A Research Module that uses randomness must accept an explicit random seed as part of the experiment execution context.

The seed must be recorded in the experiment provenance.

A randomized experiment with the same module version, input, configuration, and seed must produce semantically equivalent results, subject to the documented numerical and platform tolerances of that module.

An experiment that does not use randomness does not require a seed.

## Reproducibility

Reproducibility means that a recorded experiment contains sufficient information to rerun the same experimental procedure.

At minimum, reproducibility context must identify:

- module identity and version;
- input identity or content fingerprint;
- configuration;
- random seed when randomness is used;
- relevant schema or contract version.

The implementation may record additional environment metadata, such as runtime or dependency information, when useful for scientific traceability.

## Input Integrity

A Research Module must treat its supplied Dataset as read-only.

An experiment must not mutate the source Dataset as a side effect of execution.

## Lifecycle

The conceptual lifecycle is:

```text
Experiment Definition
        │
        ▼
Configuration + Input + Execution Context
        │
        ▼
Research Module Execution
        │
        ▼
Research Result + Provenance
```

The experiment contract does not prescribe persistence, scheduling, parallel execution, or a CLI interface.

## Non-Goals

The Experiment contract does not define:

- a database schema;
- a job queue;
- a notebook format;
- a machine-learning pipeline;
- a prediction API;
- a betting strategy;
- a specific scientific library.

## Verification Expectations

Implementations should verify:

- configuration immutability;
- explicit module and input identity;
- explicit seed handling for randomized modules;
- deterministic replay for a fixed randomized context;
- non-mutation of input data;
- preservation of experiment provenance.
