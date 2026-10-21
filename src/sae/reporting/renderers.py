"""Render presentation-neutral reports into stable output formats."""

import csv
import io
import json

from sae.reporting.model import Report


class TextReportRenderer:
    """Render a report as stable plain text."""

    def render(self, report: Report) -> str:
        """Return the report in the canonical text representation."""
        lines = [report.title, f"Draws: {report.draw_count}"]
        lines.extend(f"{row.label}: {row.value}" for row in report.rows)
        return "\n".join(lines)


class JsonReportRenderer:
    """Render a report as deterministic JSON."""

    def render(self, report: Report) -> str:
        """Return the report as a JSON object with title, draw count, and rows."""
        payload = {
            "title": report.title,
            "draw_count": report.draw_count,
            "rows": [{"label": row.label, "value": row.value} for row in report.rows],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


class CsvReportRenderer:
    """Render a report as stable CSV records."""

    def render(self, report: Report) -> str:
        """Return CSV with report metadata repeated on each row.

        The columns are title, draw_count, label, and value. An empty report
        produces one metadata record with empty label and value fields so that
        its title and draw count remain represented in the CSV output.
        """
        output = io.StringIO(newline="")
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(("title", "draw_count", "label", "value"))

        rows = report.rows or (None,)
        for row in rows:
            writer.writerow(
                (
                    report.title,
                    report.draw_count,
                    "" if row is None else row.label,
                    "" if row is None else row.value,
                )
            )

        return output.getvalue()
