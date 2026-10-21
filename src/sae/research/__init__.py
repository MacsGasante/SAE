"""Research core: reproducible experimental contracts."""

from .execution_context import ExecutionContext
from .executor import ResearchExecutionError, execute_research_module
from .experiment import Experiment
from .experiment_configuration import ExperimentConfiguration
from .module import ResearchModule
from .result import ResearchProvenance, ResearchResult

__all__ = [
    "ExecutionContext",
    "Experiment",
    "ExperimentConfiguration",
    "ResearchExecutionError",
    "ResearchModule",
    "ResearchProvenance",
    "ResearchResult",
    "execute_research_module",
]
