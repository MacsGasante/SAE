# ADR-0006 — Reporting Boundary and Rendering

## Status

Accepted

## Context

SAE already provides analytical engines for Frequency, Delay, and Probability. Their result objects represent analytical data and are intentionally independent from presentation concerns.

C3 introduces Reporting as an application-facing capability. Reporting must make analytical results readable without moving formatting logic into the Kernel or changing the existing Analytics result contracts.

The CLI is an application-facing layer and may consume reporting capabilities, while the Kernel must remain independent from both Analytics and presentation concerns.

## Decision

Reporting is a separate application-facing package.

The Reporting boundary will:

- consume existing Analytics result objects without changing their contracts;
- transform analytical results into presentation-neutral report data;
- keep output formatting inside dedicated renderers;
- keep presentation formatting out of the Kernel and Analytics packages;
- support stable text, JSON, and CSV output formats without changing analytical engines;
- be consumable by the CLI as the application-facing reporting entry point.

The report model remains presentation-neutral. Its row values are strings, preserving the existing builders' formatted values across output formats.

### Output contracts

- **Text:** title, draw count, then one `label: value` line per report row. The CLI's default format remains text for backward compatibility.
- **JSON:** one object with `title`, `draw_count`, and `rows`; each row contains `label` and `value`. Output is UTF-8-friendly, indented, deterministic, and newline-terminated. Values remain strings.
- **CSV:** header `title,draw_count,label,value`; report title and draw count are repeated for each row. An empty report emits one row with empty label and value fields to preserve metadata. CSV uses standard quoting and a newline terminator.

The CLI selects the output format with `sae report <analysis> <input> --format <text|json|csv>`. If omitted, `text` is used.

## Consequences

### Positive

- Analytics remain focused on computation and immutable results.
- Reporting is independently testable.
- CLI code remains thin and delegates presentation work.
- Additional output formats can be added without modifying Analytics engines.
- Consumers can parse JSON and CSV while existing text output remains unchanged.

### Negative

- A new architectural package is introduced between Analytics and the CLI.
- Report models and renderers add some indirection compared with formatting directly in the CLI.
- JSON and CSV expose the presentation-neutral model's string values rather than retyping analytics values.

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
- `src/sae/reporting/`
