# Analytics Specification

Version: 1.0

Status: Proposed

---

## Purpose

The Analytics layer provides deterministic, read-only calculations over a
supplied `Dataset`. It consumes the Kernel's domain objects and does not
modify the Dataset or introduce persistence, import, or prediction
responsibilities.

This specification defines the current contracts for:

- Frequency Engine;
- Delay Engine;
- Probability Engine;
- their result objects and empty-dataset behaviour.

---

## Domain and Input

Each engine accepts a `Dataset` and returns its corresponding immutable
result object. The analyzed draw count is exposed as `draw_count`.

The valid SuperEnalotto number domain is inclusive:

```text
MIN_NUMBER <= number <= MAX_NUMBER
```

The engines initialize results for every valid number, including numbers
that do not occur in the analyzed Dataset. The bounds must be obtained from
the Kernel constants `MIN_NUMBER` and `MAX_NUMBER`, not duplicated as
numeric literals in the Analytics engines.

Analytics operations are deterministic for a given Dataset and do not mutate
it. Result mappings are exposed as read-only mappings.

---

## A1 — Frequency Engine

`FrequencyEngine.analyze(dataset)` returns a `FrequencyResult`.

For every valid number (n), its frequency is the number of draws in the
Dataset whose combination contains (n):

```text
frequency(n) = count of analyzed draws containing n
```

Because a draw's combination contains distinct numbers, each draw contributes
at most one occurrence to the frequency of a given number.

### Result contract

- `draw_count`: number of draws analyzed.
- `frequencies`: read-only mapping from `Number` to integer count.
- `frequency(number)`: returns the count; returns zero if the key is absent.

### Empty Dataset

For an empty Dataset, `draw_count` is zero and every valid number has
frequency zero.

---

## A2 — Delay Engine

`DelayEngine.analyze(dataset)` returns a `DelayResult`.

The Dataset is chronologically ordered. Delay is measured in draw positions
backward from the most recent draw, not in days or calendar time.

For a number (n):

- `0`: the number occurs in the latest draw;
- `1`: the number's latest occurrence is one draw before the latest draw;
- `k`: the number's latest occurrence is (k) draws before the latest draw;
- `None`: the number does not occur in any draw in the analyzed Dataset.

Only the most recent occurrence is used. Earlier occurrences do not replace
a smaller delay.

### Result contract

- `draw_count`: number of draws analyzed.
- `delays`: read-only mapping from `Number` to a non-negative integer or
  `None`.
- `delay(number)`: returns the delay; returns `None` if the key is absent
  or its stored value indicates no occurrence in the analyzed Dataset.

The meaning of `None` is deliberately scoped to the input Dataset. It does
not assert that a number has never appeared in the complete history of the
game.

### Empty Dataset

For an empty Dataset, `draw_count` is zero and every valid number has delay
`None`.

---

## A3 — Probability Engine

`ProbabilityEngine.analyze(dataset)` returns a `ProbabilityResult`.

The engine calculates the empirical marginal inclusion rate for each number:
the fraction of analyzed draws that contain that number.

For a non-empty Dataset:

```text
probability(n) =
    number of analyzed draws containing n
    / total number of analyzed draws
```

The denominator is the number of draws, not the total count of all six
numbers across all draws. This is an empirical statistic derived from the
provided Dataset.

These values are not a prediction of the next draw, a guarantee of future
outcomes, or a betting recommendation. They are not the theoretical
probability supplied solely by the rules of the game.

### Result contract

- `draw_count`: number of draws analyzed.
- `probabilities`: read-only mapping from `Number` to a float.
- `probability(number)`: returns the empirical rate; returns zero if the
  key is absent.

### Empty Dataset

For an empty Dataset, `draw_count` is zero and every valid number has
probability value `0.0`. No division is performed for an empty Dataset.

---

## Result Objects and Immutability

The three result types are frozen data classes. Each copies its supplied
mapping into read-only mapping storage during initialization.

The result values describe the Dataset as analyzed. Neither an engine nor a
result object changes the Dataset.

The public package APIs are:

- `sae.analytics.frequency`: `FrequencyEngine`, `FrequencyResult`;
- `sae.analytics.delay`: `DelayEngine`, `DelayResult`;
- `sae.analytics.probability`: `ProbabilityEngine`, `ProbabilityResult`.

Each package declares its public exports through `__all__`.

---

## Non-Goals

The Analytics layer does not:

- predict or guarantee future draw outcomes;
- provide betting recommendations;
- mutate or own the historical Dataset;
- import or parse CSV files;
- persist or serialize results;
- implement Dataset querying or filtering;
- change the Kernel's domain model.

---

## Verification Expectations

Tests should cover, as applicable:

- single-draw and multi-draw datasets;
- repeated occurrences across different draws;
- numbers absent from the Dataset;
- the minimum and maximum valid numbers;
- empty Dataset behaviour;
- immutability and non-mutation of the Dataset;
- deterministic results;
- the public exports of each Analytics package;
- the precise delay meanings of zero, positive integers, and `None`.

Changes to the calculations or public result contracts require review of this
specification, the corresponding tests, and the project documentation.
