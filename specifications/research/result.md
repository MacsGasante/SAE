# Research Result Specification

Version: 0.1

Status: Proposed

---

## Purpose

A Research Result represents the output of a Research Module execution.

It is distinct from the deterministic result objects returned by the Analytics layer because a research result describes an experimental procedure as well as its observations.

## Result Content

A Research Result must contain:

- the experiment identity or execution identity;
- the Research Module identity and version;
- the research payload produced by the module;
- provenance describing the input and configuration;
- reproducibility context, including the random seed when applicable;
- execution metadata required to interpret the result.

The exact representation of the research payload is module-specific.

## Provenance

Provenance must identify the context required to understand how the result was produced.

At minimum it includes:

- input identity or content fingerprint;
- configuration;
- module identity and version;
- relevant schema or contract version;
- random seed when randomness was used.

Additional metadata may be recorded without changing the semantic result contract.

## Immutability

Once produced, a Research Result is treated as immutable experimental evidence.

Subsequent interpretation, comparison, rendering, or reporting must not alter the original result.

## Analytics Separation

A Research Result must not be confused with an Analytics result.

Analytics results answer deterministic questions about a supplied Dataset, such as frequency, delay, or empirical probability. Research Results describe the outcome of an explicitly defined experimental procedure and include its provenance.

A Research Module may use Analytics results as an input, but it must preserve the distinction between the consumed analytical evidence and the resulting experiment.

## Interpretation Boundary

A Research Result records observations produced by an experiment. It does not by itself establish causality, future outcomes, guarantees, or betting recommendations.

Any statistical significance, model quality, confidence interval, or other interpretation must be explicitly defined by the corresponding Research Module specification.

## Serialization

The core result contract does not require a specific serialization format.

Serialization and presentation are application concerns and may be introduced by a later Research Reporting milestone.

## Verification Expectations

Implementations should verify:

- result immutability;
- preservation of provenance;
- preservation of random seed when applicable;
- distinction from Analytics result types;
- non-mutation during reporting or interpretation.
