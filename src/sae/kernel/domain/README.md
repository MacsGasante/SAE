# Domain Layer

The Domain Layer contains the business concepts of the
SuperEnalotto Analytics Engine.

Objects contained in this package represent real concepts of
the problem domain rather than implementation details.

## Current Objects

- DrawId

## Design Principles

The Domain Layer follows the same architectural principles
used throughout the Kernel:

- Immutable Value Objects
- Explicit invariants
- Self validation
- Rich domain model
- Test-first development

Every domain object is implemented following the workflow:

Specification

↓

Implementation

↓

Unit Tests

↓

Review

↓

Repository Certification
