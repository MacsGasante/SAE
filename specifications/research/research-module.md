# Research Module Specification

Version: 0.2

Status: Implemented (R1.3)

---

## Purpose

A Research Module is an autonomous experimental capability that executes a defined research procedure over declared input data and an explicit Experiment, returning a Research Result.

A module owns the experimental procedure, not the Kernel domain model or the existing Analytics contracts.

## Python Contract

The public `ResearchModule` protocol in `sae.research.module` defines:

```python
@property
def module_id(self) -> str: ...

@property
def module_version(self) -> str: ...

def execute(self, input_data: object, experiment: Experiment) -> ResearchResult: ...
```

Module identity and version must be stable, non-empty strings and must match the supplied Experiment. The concrete input type and its interpretation belong to each module's own specification. The core deliberately does not infer, fingerprint, or mutate input data.

## Controlled Execution

`execute_research_module(module, input_data, experiment)` is the public execution boundary. It validates the experiment and protocol, checks that module identity/version match the experiment, executes the module, and verifies that the returned value is a ResearchResult whose provenance exactly matches the supplied experiment.

Module exceptions are exposed as ResearchExecutionError with the original exception preserved as the cause. Contract violations are reported as ResearchExecutionError. Invalid top-level argument types and invalid module identity values are rejected before execution.

The executor does not retry, schedule, parallelize, persist, serialize, or instrument executions. It does not compute input fingerprints; the caller is responsible for ensuring that the Experiment fingerprint identifies the supplied input.

## Inputs

A module must document the input types it requires.

When a module consumes the SAE historical Dataset, it must consume the established Dataset contract and treat the Dataset as read-only. A module may consume Analytics results when they are part of the declared experiment input or procedure.

## Configuration and Execution Context

Module-specific parameters belong to the immutable Experiment configuration rather than hidden module state. Execution context contains reproducibility information, including an explicit random seed when required. A module must not silently generate or discard a seed when randomness affects the result.

## Result

Every successful module execution returns a ResearchResult with provenance matching the supplied Experiment. A Research Module must not return an existing Analytics result type as its primary research result when the execution represents an experiment.

## Determinism

A deterministic module should produce the same semantic result for the same declared input and experiment configuration. A randomized module should produce the same semantic result for the same declared input, configuration, module version, and seed, subject to its documented numerical tolerances.

## Isolation

Research Modules must not:

- mutate the Kernel Dataset;
- change Kernel domain behaviour;
- change Analytics calculations;
- persist hidden experiment state;
- depend on global mutable configuration;
- present experimental output as a guaranteed future outcome.

## Technology Boundary

The module contract is technology-neutral. Scientific computing, statistical, numerical, or machine-learning dependencies may be used by individual modules when justified by their research requirements. Such dependencies must remain behind the Research boundary and must not become implicit Kernel dependencies.

## Initial Module Direction

The first concrete Research Module is planned as a controlled simulation-oriented module, exercising explicit configuration, random seed handling, reproducibility, result provenance, and performance. It belongs to R2 and is not implemented by R1.3.

## Verification Expectations

Tests cover successful execution, module identity/version mismatch, invalid module contracts, invalid result types, provenance mismatch, and module execution failures. Input-specific validation, scientific correctness, and deterministic replay must be tested by each concrete module.
