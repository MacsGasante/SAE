# R4.1 — Historical Frequencies vs Theoretical Null Model

Version: 0.1

Status: Implemented in the Research layer; validation pending CI review

---

## Research question

Are the marginal number frequencies in a specified historical SuperEnalotto Dataset compatible with a model in which each draw independently selects six distinct numbers uniformly from 1 through 90?

This is an omnibus goodness-of-fit study of the frequency profile. It is not a test of whether any selected number is “due”, and it does not predict future draws.

## Hypotheses

- **Null hypothesis (H0):** every draw is an independent uniform selection of six distinct numbers from the domain 1..90.
- **Alternative (H1):** the historical frequency profile is inconsistent with that model in at least one number's marginal inclusion frequency.

The study is conditional on the supplied Dataset and its declared draw-selection policy. It does not establish the physical cause of any detected discrepancy.

## Primary statistic (pre-specified)

Let N be the number of included draws, and let f_i be the number of included draws containing number i. Under H0, each number has marginal inclusion probability p = 6/90 = 1/15, so its expected frequency is Np and its variance is Np(1-p).

For N > 0, define:

z_i = (f_i - Np) / sqrt(Np(1-p))

and the single primary omnibus statistic:

T = max over i in 1..90 of |z_i|.

This statistic is two-sided at the number level and examines the largest standardized marginal-frequency deviation across the entire number domain. The maximum is evaluated as one omnibus statistic; numbers must not be selected for testing after inspecting the data.

An empty Dataset is invalid for this experiment.

## Null distribution and Monte Carlo p-value

The null distribution of T will be estimated by seeded simulation. For each replicate, simulate exactly N independent draws, each consisting of six distinct numbers sampled uniformly from 1..90, then calculate T using the same formula.

Given B simulated replicates and R replicates with T_simulated >= T_observed, report the finite-simulation p-value:

p_hat = (R + 1) / (B + 1).

The +1 correction avoids a reported p-value of zero and treats the observed statistic consistently with the finite Monte Carlo reference sample. Equality counts as an exceedance. The result must report B, R, the seed, the observed statistic, and p_hat. It must describe p_hat as a Monte Carlo estimate, not an exact probability.

The random seed must be explicitly supplied and recorded. The simulation count B must be an explicit positive configuration value and is therefore required on the CLI; no default is supplied until a benchmark on a representative historical Dataset justifies one. The implementation must not silently change B, seed, or the analysis window.

## Dataset and provenance

- Input is a non-empty immutable Kernel Dataset.
- All six main numbers in each included draw contribute once to the corresponding marginal frequency.
- Jolly and Superstar are outside this research question and are excluded.
- The initial study uses all draws in the supplied Dataset; any future date-window selection must be explicit and separately recorded.
- The experiment input fingerprint must be SHA-256 over UTF-8 bytes of a canonical JSON array, in Dataset iteration order. Each draw is represented as `[draw.id.to_int(), draw.date.isoformat(), [n.value for n in draw.numbers]]`; JSON uses `ensure_ascii=False` and separators `(',', ':')`, with no trailing newline. This avoids dependence on Python object identity, repr output, or CSV formatting.
- Result provenance must preserve module identity/version, input fingerprint, configuration, and random seed through the existing Research contracts.

## Interpretation

The test addresses only the marginal frequency profile under the stated null model. It does not test every property of the draw process, such as serial dependence or dependence involving particular combinations.

A small p_hat is evidence of a frequency-profile discrepancy relative to this null model, not proof of fraud, a causal explanation, or evidence that any number is more likely in a future draw. A non-small p_hat is not proof that the null model is true.

The six numbers within each draw are sampled without replacement and therefore are not six independent number-level observations. The reference distribution must simulate complete six-number draws, not independent number picks or a naive multinomial model over 6N independent picks.

## Reproducibility and validation requirements

- Identical Dataset content, module version, configuration, and seed produce identical semantic results.
- Dataset fingerprint changes when any included draw identifier, date, or main number changes.
- Observed frequencies cover exactly 1..90 and sum to 6N.
- Every simulated replicate contains N valid six-distinct-number draws.
- The statistic is finite and non-negative for N > 0.
- R is an integer in [0, B] and p_hat equals (R + 1)/(B + 1).
- Invalid input types, empty Datasets, invalid B values, and missing/invalid seeds fail clearly; booleans are not accepted as integers.
- Tests use small controlled examples and deterministic seeds; the full CI must verify typing, lint, coverage, and regression safety.
- No default replicate count is currently defined. Runtime and memory must be benchmarked on a representative historical Dataset before considering one. If performance is insufficient, optimize the implementation without changing the declared null model or statistic.

## Architectural boundaries

This is a Research-layer experiment. It may consume Kernel Dataset APIs and the public Frequency Analytics API, but it must not modify Kernel or Analytics contracts. The existing theoretical Monte Carlo module remains self-contained and continues to require `None` input; this study must not change that module's input contract merely to reuse it.

The result is evidence about the supplied historical sample, not a prediction or betting recommendation.

## Implemented interface

The module is exposed as `sae.research.HistoricalFrequencyNullModel`; its stable module ID is `sae.research.historical-frequency-null-model` and version is `1.0.0`. The CLI entry point is:

```bash
sae research historical-test storico.csv --seed 1729 --replicate-count 999 --format json
```

`--seed` and `--replicate-count` are required. Output uses the existing Research reporting boundary and supports `text`, `json`, and `csv`. The observed Dataset fingerprint is verified against the experiment before execution. The existing `sae research simulate` module is unchanged.

## Acceptance criteria for implementation

1. Implemented: statistic and null simulation follow the pre-specified method.
2. Implemented: input/configuration/seed provenance and Dataset fingerprint are recorded.
3. Implemented: output uses the Research reporting boundary and supports text/JSON/CSV.
4. Implemented: focused unit and CLI tests cover determinism, invariants, validation, and report provenance.
5. Pending: benchmark runtime on a representative historical Dataset before considering a default replicate count.
6. Pending: verify the pull-request CI and review the complete change set.
