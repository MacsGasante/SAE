"""Presentation boundary for Research Results."""

from sae.research_reporting.builders import build_research_report
from sae.research_reporting.model import ResearchReport
from sae.research_reporting.renderers import (
    CsvResearchReportRenderer,
    JsonResearchReportRenderer,
    TextResearchReportRenderer,
)

__all__ = [
    "CsvResearchReportRenderer",
    "JsonResearchReportRenderer",
    "ResearchReport",
    "TextResearchReportRenderer",
    "build_research_report",
]
