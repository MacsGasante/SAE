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

Current focus:

* M1.5 — Dataset Layer

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

```text
SAE/
├── docs/
├── engineering/
├── research/
├── specifications/
├── src/
├── tests/
└── workspace/
```

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
* M1.5 Dataset Layer
* M1.6 Analytics
* Research Modules

---

## License

MIT License
