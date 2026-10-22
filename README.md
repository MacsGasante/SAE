# SAE

# SuperEnalotto Analytics Engine

SAE is an open-source research project focused on building a modern analytics engine for the Italian SuperEnalotto lottery.

The objective of the project is **not** to predict future draws.

The objective is to provide a rigorous framework for:

* statistical analysis
* probabilistic research
* hypothesis generation
* hypothesis validation
* reproducible experiments

---

## What SAE Is

SAE treats SuperEnalotto as a structured research domain rather than as a prediction or betting problem.

The engine is designed to support reproducible exploration of historical data through statistics, probability, combinatorics, hypothesis generation, and hypothesis validation.

The project combines analytical research with disciplined software engineering, using a structured domain model and an evolvable architecture.

---

## What SAE Is Not

SAE is not a system for predicting winning numbers, guaranteeing outcomes, or recommending bets.

Any predictive or machine-learning techniques explored by the project are considered research subjects and experimental tools, not guarantees of future outcomes.

---

## Project Status

**Pre-Alpha**

The project is currently under active development.

The Kernel Foundation has been completed and certified.

Completed milestones:

* M1.1 — Number
* M1.2 — Combination
* M1.3 — Builder Layer
* M1.4 — Domain Model Foundations
* M1.5 — Dataset Layer
* M1.6 — Analytics
  * A1 — Frequency Engine
  * A2 — Delay Engine
  * A3 — Probability Engine
* C1 — Basic Commands
* C2 — Import Tools
* C3 — Reporting
  * C3.1 — Reporting core
  * C3.2 — CLI reporting
  * C3.3 — JSON and CSV formats
  * C3.4 — Integration and end-to-end validation

All C3 Reporting sub-milestones are complete. The end-to-end pipeline is covered by integration tests, and the Analytics CLI supports text (default), JSON, and CSV output.

Research R0–R3.3 are complete: the initial Research core, seeded Monte Carlo simulation, dedicated reporting boundary, `sae research simulate` CLI, and end-to-end integration validation are implemented. Research output supports text, JSON, and CSV while preserving experiment provenance and execution metadata.

R4.1 introduces the first historical-data research test: it compares the observed marginal number-frequency profile with a null model of independent uniform six-of-90 draws. The test uses a pre-specified maximum absolute standardized deviation and seeded Monte Carlo replicates. It is available as `sae research historical-test <csv> --seed <integer> --replicate-count <positive integer> [--format text|json|csv]`. The replicate count is explicit because no default will be selected before a representative historical-data runtime benchmark. Results assess only compatibility of the marginal frequency profile; they do not predict future draws or recommend bets. CI verification is pending.

---

## Design Principles

* Scientific approach
* Domain-Driven Design (DDD)
* Clean Architecture
* Immutable Value Objects
* Test-first development
* Reproducible research
* Repository Certification
* Documentation as Code

---

## Repository Structure

### Current Repository Structure

The repository currently contains the following principal areas:

```text
SAE/
├── docs/
├── engineering/
├── specifications/
├── src/
└── tests/
```

These directories represent the current implemented repository structure.

### Planned / Future Structure

Additional areas are planned for future development:

```text
SAE/
├── research/
└── workspace/
```

These directories are not currently part of the repository and are not
created until their respective responsibilities are formally introduced.

---

## Development

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Install the project:

```bash
make bootstrap
```

---

## Development Commands

```bash
make test
make lint
make format
make typecheck
make check
```

---

## Roadmap

* M1.1 Kernel Foundation ✅
* M1.2 Collections ✅
* M1.3 Builder Layer ✅
* M1.4 Domain Model Foundations ✅
* M1.5 Dataset Layer ✅
* M1.6 Analytics ✅
  * A1 Frequency Engine ✅
  * A2 Delay Engine ✅
  * A3 Probability Engine ✅
* C1 Basic Commands ✅
* C2 Import Tools ✅
* C3 Reporting
  * C3.1 Reporting core ✅
  * C3.2 CLI reporting ✅
  * C3.3 JSON and CSV formats ✅
  * C3.4 Integration and end-to-end validation ✅
* R4.1 Historical frequency vs null-model research — implementation in review

---

## License

MIT License
