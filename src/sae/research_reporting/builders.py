"""Build presentation-neutral reports from Research Results."""

from sae.research.result import ResearchResult
from sae.research_reporting.model import ResearchReport


def build_research_report(result: ResearchResult) -> ResearchReport:
    """Build a Research report without adding statistical interpretation."""
    if not isinstance(result, ResearchResult):
        raise TypeError("result must be a ResearchResult.")

    return ResearchReport(
        title=f"Research Report — {result.module_id}",
        provenance=result.provenance,
        payload=result.payload,
        execution_metadata=result.execution_metadata,
    )
