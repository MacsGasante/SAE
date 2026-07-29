# SAE

# SuperEnalotto Analytics Engine

SAE is an open-source research project focused on building a modern analytics engine for the Italian SuperEnalotto lottery.

The objective of the project is **not** to predict future draws.

The objective is to provide a rigorous framework for:

- statistical analysis
- probabilistic research
- hypothesis generation
- hypothesis validation
- reproducible experiments

---

## Project Status

**Pre-Alpha**

The project is currently under active development.

Architecture is frozen.

Kernel implementation has started.

---

## Design Principles

- Scientific approach
- Domain-Driven Design (DDD)
- Clean Architecture
- Immutable Value Objects
- Test-first development
- Reproducible research

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

- Repository Bootstrap
- Kernel Foundation
- Domain Model
- Dataset Engine
- Analytics Engine
- Research Modules

---

## License

MIT License
