"""Render Research reports as stable text, JSON, and CSV."""

import csv
import io
import json
from collections.abc import Mapping, Sequence
from typing import TypeAlias

from sae.research_reporting.model import ResearchReport

JSONScalar: TypeAlias = str | int | float | bool | None


def _plain(value: object) -> object:
    """Convert immutable Research values to JSON-compatible containers."""
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    return value


def _report_data(report: ResearchReport) -> dict[str, object]:
    """Return the canonical structured representation of a Research report."""
    provenance = report.provenance
    return {
        "title": report.title,
        "provenance": {
            "experiment_id": provenance.experiment_id,
            "module_id": provenance.module_id,
            "module_version": provenance.module_version,
            "input_fingerprint": provenance.input_fingerprint,
            "schema_version": provenance.schema_version,
            "configuration": json.loads(provenance.configuration.to_json()),
            "execution_context": {
                "random_seed": provenance.execution_context.random_seed,
            },
        },
        "payload": _plain(report.payload),
        "execution_metadata": _plain(report.execution_metadata),
    }


class TextResearchReportRenderer:
    """Render Research reports as readable text with explicit provenance."""

    def render(self, report: ResearchReport) -> str:
        """Return a deterministic text representation."""
        data = _report_data(report)
        lines = [
            str(data["title"]),
            "",
            "Provenance:",
            json.dumps(data["provenance"], ensure_ascii=False, indent=2),
            "",
            "Execution metadata:",
            json.dumps(data["execution_metadata"], ensure_ascii=False, indent=2),
            "",
            "Payload:",
            json.dumps(data["payload"], ensure_ascii=False, indent=2),
        ]
        return "\n".join(lines) + "\n"


class JsonResearchReportRenderer:
    """Render Research reports as deterministic, structured JSON."""

    def render(self, report: ResearchReport) -> str:
        """Return the canonical JSON representation with a final newline."""
        return (
            json.dumps(
                _report_data(report),
                ensure_ascii=False,
                indent=2,
                allow_nan=False,
            )
            + "\n"
        )


class CsvResearchReportRenderer:
    """Render Research reports as stable section/key/value CSV records.

    Nested values are encoded as compact JSON in the value column. This keeps
    payload and provenance information available without inventing a
    domain-specific tabular interpretation for arbitrary Research outputs.
    """

    def render(self, report: ResearchReport) -> str:
        """Return CSV containing provenance, metadata, and payload entries."""
        data = _report_data(report)
        output = io.StringIO(newline="")
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(("section", "key", "value"))

        for section in ("provenance", "execution_metadata", "payload"):
            values = data[section]
            if isinstance(values, Mapping):
                for key, value in values.items():
                    rendered = (
                        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                        if isinstance(value, (Mapping, list))
                        else "" if value is None else str(value)
                    )
                    writer.writerow((section, key, rendered))
            else:
                writer.writerow((section, "value", str(values)))

        return output.getvalue()
