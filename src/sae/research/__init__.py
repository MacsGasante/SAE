"""Research core: reproducible experimental contracts."""

from .execution_context import ExecutionContext
from .executor import ResearchExecutionError, execute_research_module
from .experiment import Experiment
from .experiment_configuration import ExperimentConfiguration
from .historical_frequency import HistoricalFrequencyNullModel, dataset_fingerprint
from .module import ResearchModule
from .monte_carlo import MonteCarloDrawSimulation
from .result import ResearchProvenance, ResearchResult

__all__ = [
    "ExecutionContext",
    "Experiment",
    "ExperimentConfiguration",
    "HistoricalFrequencyNullModel",
    "MonteCarloDrawSimulation",
    "ResearchExecutionError",
    "ResearchModule",
    "ResearchProvenance",
    "ResearchResult",
    "dataset_fingerprint",
    "execute_research_module",
]
