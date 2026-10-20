# ADR-0006 — Reporting Boundary and Rendering

## Status

Proposed

## Context

SAE already provides analytical engines for Frequency, Delay, and Probability. Their result objects represent analytical data and are intentionally independent from presentation concerns.

C3 introduces Reporting as an application-facing capability. Reporting must make analytical results readable without moving formatting logic into the Kernel or changing the existing Analytics result contracts.

The CLI is an application-facing layer and may consume reporting capabilities, while the Kernel must remain independent from both Analytics and presentation concerns.

## Decision

Reporting will be introduced as a separate application-facing package.

The Reporting boundary will:

- consume existing Analytics result objects without changing their contracts;
- transform analytical results into presentation-neutral report data;
- keep terminal/text formatting inside dedicated renderers;
- keep presentation formatting out of the Kernel and Analytics packages;
- allow additional renderers or output formats to be added without changing analytical engines;
- be consumable by the CLI as the application-facing reporting entry point.

The first C3 implementation will target a stable text report. Other formats, such as JSON or CSV, are deferred until explicitly required by the C3 contract.

## Consequences

### Positive

- Analytics remain focused on computation and immutable results.
- Reporting becomes independently testable.
- CLI code remains thin and delegates presentation work.
- Additional output formats can be added without modifying Analytics engines.

### Negative

- A new architectural package is introduced between Analytics and the CLI.
- Report models and renderers add some indirection compared with formatting directly in the CLI.

## Alternatives

### Format directly in the CLI

Rejected because it couples the CLI to every Analytics result shape and makes additional output formats harder to introduce.

### Add formatting methods to Analytics result classes

Rejected because analytical results should remain presentation-neutral and reusable outside the CLI.

### Put Reporting inside the Kernel

Rejected because the Kernel must remain independent from application-facing presentation concerns.

## Related Documents

- `ROADMAP.md`
- `docs/architecture/README.md`
- `src/sae/analytics/`
- `src/sae/cli/`
