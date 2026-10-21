"""Presentation-neutral report model for Research Results."""

from dataclasses import dataclass
from sae.research.result import ResearchProvenance



@dataclass(frozen=True, slots=True)
class ResearchReport:
    """Immutable presentation model for a Research Result.

    The report keeps the result payload separate from provenance and execution
    metadata so presentation cannot blur experimental observations with their
    origin or with existing Analytics reports.
    """

    title: str
    provenance: ResearchProvenance
    payload: object
    execution_metadata: object
