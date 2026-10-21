# R2 — Monte Carlo Draw Simulation

Version: 1.0

Status: Implemented (R2 initial module)

---

## Purpose

Provide the first concrete SAE Research Module: a reproducible Monte Carlo simulation of independent draws containing six distinct integers selected uniformly from 1 through 90.

The module demonstrates the R1 contracts for explicit experiment configuration, seed handling, immutable results, provenance, and controlled execution. It does not consume historical Dataset data; its input contract is explicitly `None` because it simulates from a declared abstract draw model.

## Configuration

- `draw_count`: positive integer number of simulated draws; defaults to 10,000.
- Booleans are not accepted as integers.
- The experiment must declare a non-negative integer `random_seed`; a missing seed is an error.
- The experiment's module identifier and version must match the module's stable identity.

No hidden random seed is generated. The implementation uses a local `random.Random(seed)` instance and does not alter global random state.

## Output

The immutable `ResearchResult` payload contains:

- draw count and number-domain constants;
- the observed occurrence count for each number from 1 through 90;
- a distribution describing how many numbers attained each occurrence count.

Execution metadata records the algorithm identifier and explicit seed. Result provenance is copied from the supplied Experiment by the shared R1 result contract.

## Reproducibility

For the same module version, configuration, and seed, the module must produce the same semantic payload. Tests verify deterministic replay and that the sum of all number frequencies equals six times the simulated draw count.

## Interpretation and limitations

This module samples a theoretical model; it does not analyze historical draws, estimate an advantage, predict official outcomes, or recommend bets. Frequencies are properties of the simulated sample, not forecasts. The standard-library pseudorandom generator is sufficient for this initial reproducibility demonstration and is not a cryptographic generator.

## Scope

This initial R2 increment does not add CLI/reporting integration, persistence, parallel execution, external numerical dependencies, or changes to Kernel and Analytics contracts.
