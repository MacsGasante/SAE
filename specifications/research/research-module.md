# Research Module Specification

Version: 0.1

Status: Proposed

---

## Purpose

A Research Module is an autonomous experimental capability that executes a defined research procedure over declared inputs and configuration and returns a Research Result.

A module owns the experimental procedure, not the Kernel domain model or the existing Analytics contracts.

## Module Contract

A Research Module must expose a conceptual operation equivalent to:

```text
execute(input, configuration, execution_context) -> ResearchResult
```

The concrete Python interface is an implementation decision for the R1 Research Core milestone.

## Inputs

A module must declare the input types it requires.

When a module consumes the SAE historical Dataset, it must consume the established Dataset contract and treat the Dataset as read-only.

A module may consume Analytics results when they are part of the declared experiment input or procedure.

## Configuration

Module-specific parameters belong to the experiment configuration rather than hidden module state.

Configuration must be immutable during execution.

## Execution Context

Execution context contains reproducibility information that is not itself part of the research hypothesis, including a random seed when required.

A module must not silently generate or discard a seed when randomness affects the result.

## Result

Every successful module execution returns a Research Result with sufficient provenance to identify the experiment that produced it.

A Research Module must not return an existing Analytics result type as its primary research result when the execution represents an experiment. Research results have a separate contract.

## Determinism

A deterministic module must produce the same semantic result for the same declared input and configuration.

A randomized module must produce the same semantic result for the same declared input, configuration, module version, and seed, subject to the module's documented numerical tolerances.

## Isolation

Research Modules must not:

- mutate the Kernel Dataset;
- change Kernel domain behaviour;
- change Analytics calculations;
- persist hidden experiment state;
- depend on global mutable configuration;
- present experimental output as a guaranteed future outcome.

## Technology Boundary

The module contract is technology-neutral.

Scientific computing, statistical, numerical, or machine-learning dependencies may be used by individual modules when justified by their research requirements. Such dependencies must remain behind the Research boundary and must not become implicit Kernel dependencies.

## Initial Module Direction

The first concrete Research Module should be a controlled simulation-oriented module because it exercises the core requirements of the Research architecture: explicit configuration, random seed handling, reproducibility, execution context, result provenance, and performance.

The concrete module contract is deferred to the R2 milestone and is not defined by this specification.
