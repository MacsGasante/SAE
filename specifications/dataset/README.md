# Dataset Specifications

The Dataset Layer represents the complete immutable historical archive of
official SuperEnalotto draws.

The Dataset Layer belongs to the Kernel because it models domain concepts
and does not depend on infrastructure, persistence, analytics or
presentation.

The Dataset Layer provides the Dataset Aggregate Root and its dedicated
Query Layer.

---

## Components

- Dataset Aggregate Root
- Dataset Query Layer

The Dataset Aggregate Root directly owns the immutable collection of
Draw objects.

No intermediate DrawCollection abstraction exists.

---

## Design Goals

- Immutable
- Chronologically ordered
- Deterministic
- Reproducible
- Infrastructure-independent
- Analytics-independent

---

## Non Goals

The Dataset Layer does not:

- read CSV files;
- parse external formats;
- connect to databases;
- perform statistical analysis;
- calculate frequencies or delays;
- implement persistence;
- implement repository behaviour.

Those responsibilities belong to Infrastructure and Analytics.

---

## Dependency Graph

Dataset

↓

tuple[Draw]

↓

Draw

↓

Combination

↓

Number

---

## Query Layer

The Dataset Query Layer provides read-oriented operations over Dataset
instances.

The Dataset exposes the query facade through:

```
dataset.query
```

which returns:

```
DatasetQuery
```

The Query Layer provides operations such as:

- generic filtering;
- date-based selection;
- Number queries;
- Combination queries;
- query composition.

Query operations never modify the Dataset Aggregate.

---

## Architecture

Current Dataset architecture:

Dataset
│
└── tuple[Draw]

Current Query architecture:

Dataset
│
└── DatasetQuery

The Dataset Aggregate is responsible for archive integrity and immutable
storage.

The Query Layer is responsible for read-oriented query behaviour.
