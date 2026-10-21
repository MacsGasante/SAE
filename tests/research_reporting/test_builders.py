from sae.research.execution_context import ExecutionContext
from sae.research.experiment import Experiment
from sae.research.experiment_configuration import ExperimentConfiguration
from sae.research.result import ResearchProvenance, ResearchResult
from sae.research_reporting import build_research_report


def _result() -> ResearchResult:
    experiment = Experiment(
        experiment_id="experiment-1",
        module_id="sae.research.monte-carlo-draw-simulation",
        module_version="1.0.0",
        input_fingerprint="theoretical-model-v1",
        configuration=ExperimentConfiguration({"draw_count": 20}),
        execution_context=ExecutionContext(random_seed=17),
    )
    return ResearchResult(
        provenance=ResearchProvenance.from_experiment(experiment),
        payload={"draw_count": 20, "number_frequencies": {"1": 2}},
        execution_metadata={"random_seed": 17},
    )


def test_builder_preserves_payload_and_provenance() -> None:
    result = _result()

    report = build_research_report(result)

    assert report.title == f"Research Report — {result.module_id}"
    assert report.provenance == result.provenance
    assert report.payload == result.payload
    assert report.execution_metadata == result.execution_metadata


def test_builder_rejects_non_research_result() -> None:
    try:
        build_research_report(object())  # type: ignore[arg-type]
    except TypeError as exc:
        assert str(exc) == "result must be a ResearchResult."
    else:
        raise AssertionError("Expected TypeError.")
