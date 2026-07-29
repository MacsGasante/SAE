# DrawDate Specification

## Purpose

Represents the official calendar date of a SuperEnalotto draw.

---

## Classification

Value Object

---

## Underlying Type

Python `datetime.date`

---

## Responsibilities

DrawDate is responsible for:

- representing a valid calendar date;
- exposing year, month and day;
- supporting ordering;
- supporting hashing;
- exposing ISO-8601 formatting.

---

## Invariants

- value is an instance of `datetime.date`.

Calendar validation is delegated to Python's standard library.

No restriction is imposed on past or future dates.

---

## Construction

```python
DrawDate.from_parts(year, month, day)

DrawDate.from_date(date(...))
```

---

## Public API

- value
- year
- month
- day
- to_date()
- isoformat()

---

## Equality

Two DrawDate objects are equal when their underlying dates are equal.

---

## Ordering

Natural chronological ordering.

---

## Exceptions

Construction raises:

- InvalidDrawDateError

when the supplied value is not valid.

---

## Dependencies

- datetime.date
- ValueObject
- InvalidDrawDateError

---

## Tests

The following behaviours must be verified:

- valid construction;
- invalid calendar dates;
- invalid type;
- equality;
- ordering;
- hashability;
- ISO formatting;
- conversion to datetime.date.
