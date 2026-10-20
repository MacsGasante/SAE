"""Text renderers for application-facing reports."""

from sae.reporting.model import Report


class TextReportRenderer:
    """Render a report as stable plain text."""

    def render(self, report: Report) -> str:
        """Return the report in the canonical text representation."""
        lines = [report.title, f"Draws: {report.draw_count}"]
        lines.extend(f"{row.label}: {row.value}" for row in report.rows)
        return "\n".join(lines)
