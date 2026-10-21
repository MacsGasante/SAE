# User Guide

## Purpose

This section contains documentation intended for users of the SAE software.

Unlike development documentation, these documents explain how to use the application rather than how it is implemented.

## Reporting from a CSV dataset

The `sae report` command imports an official SuperEnalotto CSV dataset, runs one analytics engine, and writes the resulting report to standard output.

```bash
sae report frequency path/to/dataset.csv
sae report delay path/to/dataset.csv
sae report probability path/to/dataset.csv
```

The supported analyses are:

- `frequency` — occurrence counts for numbers 1–90
- `delay` — delay values for numbers 1–90; `Never` indicates a number not observed in the dataset
- `probability` — observed relative frequencies from the historical dataset, not predictions of future draws

### Output formats

Text is the default and can be selected explicitly:

```bash
sae report frequency path/to/dataset.csv --format text
```

JSON and CSV are also supported:

```bash
sae report frequency path/to/dataset.csv --format json
sae report frequency path/to/dataset.csv --format csv
```

JSON output contains `title`, `draw_count`, and `rows`; each row contains a `label` and a string `value`.

CSV output uses the columns `title,draw_count,label,value`. Report metadata is repeated for each row. If a report has no rows, CSV still emits a metadata row with empty `label` and `value` fields.

The command reads the input dataset and prints the report to standard output. It does not write an output file or modify the source CSV.

## Scope

SAE is a research and analytics project. Its reports describe historical data and do not predict future draws, guarantee outcomes, or recommend bets.
