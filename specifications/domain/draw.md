# Draw Specification

## Classification

Aggregate Root

---

## Purpose

Represents one official SuperEnalotto draw.

A Draw aggregates the immutable domain objects describing a single
official extraction.

---

## Components

- DrawId
- DrawDate
- Combination

---

## Identity

Identity is represented exclusively by DrawId.

Two Draw instances with the same DrawId represent the same
domain entity.

---

## Responsibilities

A Draw is responsible for:

- exposing its identifier;
- exposing the official draw date;
- exposing the winning combination;
- answering simple domain queries about its numbers.

No statistical behaviour belongs to Draw.

---

## Public API

Properties

- id
- date
- combination
- numbers

Methods

- contains(Number)

---

## Equality

Identity-based.

DrawId defines equality.

---

## Ordering

Not supported.

Ordering must always be explicit.

Examples:

- by DrawId
- by DrawDate

---

## Immutability

Draw is immutable.

All contained objects are immutable.

---

## Dependencies

Foundation

- Number

Collections

- Combination

Domain

- DrawId
- DrawDate

---

## Validation

Construction validates:

- DrawId
- DrawDate
- Combination

Invalid values raise InvalidDrawError.

---

## Tests

The implementation must verify:

- valid creation;
- invalid identifier;
- invalid date;
- invalid combination;
- identity equality;
- hashing;
- numbers delegation;
- contains();
- repr().
