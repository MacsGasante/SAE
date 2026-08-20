# ADR-0004

## Title

Dataset Aggregate Root

## Status

Accepted

## Date

2026-08-01

---

# Context

During the design of the Dataset Layer an intermediate
`DrawCollection` abstraction was proposed.

Previous architecture:

Dataset
↓
DrawCollection
↓
tuple[Draw]

A design review showed that `DrawCollection` introduced no additional
domain behaviour.

Its responsibilities would have duplicated those of Dataset and would
have added unnecessary forwarding methods and abstraction.

---

# Decision

The `DrawCollection` abstraction is removed.

The Dataset becomes the Aggregate Root responsible for the immutable
collection of historical Draw objects.

Current architecture:

Dataset
↓
tuple[Draw]

The Dataset directly owns its immutable storage.

---

# Consequences

## Positive

- fewer abstractions;
- simpler API;
- fewer forwarding methods;
- clearer Aggregate ownership;
- lower maintenance cost;
- clearer separation between Dataset integrity and Query behaviour.

## Negative

- Dataset is directly responsible for collection invariants.

This responsibility is considered appropriate for an Aggregate Root.

---

# Query Layer Separation

Query behaviour is deliberately separated from the Dataset Aggregate.

The Dataset exposes:

```
dataset.query
```

which provides access to the dedicated `DatasetQuery` facade.

The Query Layer is responsible for read-oriented operations such as:

- filtering;
- date selection;
- Number queries;
- Combination queries;
- query composition.

The Dataset remains responsible for:

- immutable storage;
- chronological ordering;
- DrawId uniqueness;
- DrawDate uniqueness;
- collection semantics.

This separation prevents query behaviour from expanding the Aggregate
Root beyond its integrity responsibilities.

---

# Alternatives Considered

## Alternative A

Dataset
↓
DrawCollection
↓
tuple[Draw]

Rejected.

Reason:

`DrawCollection` introduces no independent domain behaviour and creates
an unnecessary abstraction layer.

---

# Future Evolution

Future metadata may be introduced through a dedicated
`DatasetMetadata` Value Object.

Possible architecture:

Dataset

├── tuple[Draw]

└── DatasetMetadata

No `DrawCollection` layer shall be reintroduced unless a future
Architecture Decision Record demonstrates a distinct domain
responsibility requiring it.

---

# Related Documents

- `DATASET_GUIDELINES.md`
- `specifications/dataset/dataset.md`
- `specifications/dataset/dataset_structure.md`
- `specifications/dataset/dataset_queries.md`
- `docs/testing/TESTING_GUIDELINES.md`
