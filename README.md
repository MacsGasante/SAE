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

## Project Status

**Pre-Alpha**

The project is currently under active development.

The Kernel Foundation has been completed and certified.

Completed milestones:

* M1.1 — Number
* M1.2 — Combination
* M1.3 — Builder Layer

Current focus:

* M1.4 — Domain Model Foundations

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
* M1.4 Domain Model Foundations
* M1.5 Draw Domain
* Analytics Engine
* Research Modules

---

## License

MIT License
