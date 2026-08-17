# Dataset Specification

## Purpose

Dataset is the Aggregate Root representing an immutable historical
archive of SuperEnalotto draws.

---

## Responsibilities

- own a DrawCollection;
- expose dataset metadata;
- provide a stable API for analytics modules.

---

## Aggregate Root

Dataset

↓

DrawCollection

↓

Draw

---

## Public API

Properties

- draws
- size
- first
- last

Methods

- __len__()
- __iter__()

---

## Invariants

- immutable
- chronological
- unique DrawId
- unique DrawDate

---

## Future Metadata

- source
- version
- first_draw
- last_draw
- draw_count

---

## Non Goals

Dataset never:

- loads CSV files;
- saves files;
- computes statistics;
- performs analytics.

Infrastructure creates Dataset.

Analytics consumes Dataset.
