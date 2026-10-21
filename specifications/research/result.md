# Research Result Specification

Version: 0.1

Status: Implemented (R1.2)

---

## Purpose

A Research Result represents the output of a Research Module execution.

It is distinct from the deterministic result objects returned by the Analytics layer because a research result describes an experimental procedure as well as its observations.

## Result Content

A Research Result contains:

- experiment identity;
- Research Module identity and version;
- the research payload produced by the module;
- provenance describing the input and configuration;
- reproducibility context, including the random seed when applicable;
- a schema/contract version;
- optional execution metadata needed to interpret the result.

The core contract does not execute a module or assign scientific meaning to the payload.

## Provenance

ResearchProvenance identifies the context required to understand how the result was produced.

At minimum it includes:

- experiment identifier;
- module identifier and version;
- input content fingerprint;
- immutable experiment configuration;
- execution context, including the random seed when applicable;
- result schema version (research-result/v1 by default).

ResearchProvenance.from_experiment(experiment) captures the identity and reproducibility context from the declared Experiment without recomputing or mutating it.

Execution metadata is separate from provenance: it may contain optional descriptive details such as runtime or environment information. The core does not require timestamps or environment discovery.

## Immutability and Payload Boundary

ResearchResult and ResearchProvenance are frozen value objects.

Payload and execution metadata accept JSON-compatible scalars, mappings, and sequences. Input structures are defensively copied; nested mappings become read-only and sequences become tuples. Non-string mapping keys, unsupported object types, and non-finite floats are rejected.

This intentionally technology-neutral representation supports structured observations without introducing serialization or scientific-library dependencies.

## Analytics Separation

A Research Result is not an Analytics result.

Analytics results answer deterministic questions about a supplied Dataset, such as frequency, delay, or empirical probability. Research Results describe the outcome of an explicitly defined experimental procedure and include its provenance.

A Research Module may use Analytics results as an input, but it must preserve the distinction between the consumed analytical evidence and the resulting experiment.

## Interpretation Boundary

A Research Result records observations produced by an experiment. It does not by itself establish causality, future outcomes, guarantees, or betting recommendations.

Any statistical significance, model quality, confidence interval, or other interpretation must be explicitly defined by the corresponding Research Module specification.

## Serialization

The core result contract does not require a specific serialization format. Serialization and presentation remain application concerns for a later Research Reporting milestone.

## Verification Expectations

Tests verify:

- immutable result and provenance objects;
- deep immutability and defensive copying of payload and execution metadata;
- preservation of experiment identity, configuration, input fingerprint, module version, and random seed;
- rejection of invalid identity fields and unsupported payload values;
- distinction from Analytics result types;
- absence of execution, persistence, reporting, or statistical logic in the core result contract.
