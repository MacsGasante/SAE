import csv
import io
import json

from sae.research.execution_context import ExecutionContext
from sae.research.experiment import Experiment
from sae.research.experiment_configuration import ExperimentConfiguration
from sae.research.result import ResearchProvenance, ResearchResult
from sae.research_reporting import (
    CsvResearchReportRenderer,
    JsonResearchReportRenderer,
    TextResearchReportRenderer,
    build_research_report,
)


def _report():
    experiment = Experiment(
        experiment_id="experiment-42",
        module_id="sae.research.monte-carlo-draw-simulation",
        module_version="1.0.0",
        input_fingerprint="theoretical-model-v1",
        configuration=ExperimentConfiguration({"draw_count": 20}),
        execution_context=ExecutionContext(random_seed=17),
    )
    result = ResearchResult(
        provenance=ResearchProvenance.from_experiment(experiment),
        payload={
            "draw_count": 20,
            "number_frequencies": {"1": 2, "2": 1},
        },
        execution_metadata={
            "algorithm": "python.random.Random.sample",
            "random_seed": 17,
        },
    )
    return build_research_report(result)


def test_json_renderer_preserves_payload_provenance_and_metadata() -> None:
    report = _report()

    rendered = JsonResearchReportRenderer().render(report)
    data = json.loads(rendered)

    assert data["title"] == report.title
    assert data["provenance"]["experiment_id"] == "experiment-42"
    assert data["provenance"]["configuration"] == {"draw_count": 20}
    assert data["provenance"]["execution_context"]["random_seed"] == 17
    assert data["payload"]["number_frequencies"] == {"1": 2, "2": 1}
    assert data["execution_metadata"]["random_seed"] == 17
    assert rendered.endswith("\n")


def test_text_renderer_labels_sections_and_keeps_provenance() -> None:
    rendered = TextResearchReportRenderer().render(_report())

    assert "Provenance:" in rendered
    assert "Execution metadata:" in rendered
    assert "Payload:" in rendered
    assert '"experiment_id": "experiment-42"' in rendered
    assert '"random_seed": 17' in rendered


def test_csv_renderer_preserves_all_report_sections() -> None:
    rendered = CsvResearchReportRenderer().render(_report())
    records = list(csv.reader(io.StringIO(rendered)))

    assert records[0] == ["section", "key", "value"]
    assert ["provenance", "experiment_id", "experiment-42"] in records
    assert ["provenance", "execution_context", '{"random_seed":17}'] in records
    assert [
        "payload",
        "number_frequencies",
        '{"1":2,"2":1}',
    ] in records
    assert ["execution_metadata", "random_seed", "17"] in records
    assert rendered.endswith("\n")
