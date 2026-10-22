"""End-to-end tests for the Research simulation CLI pipeline."""

import json

from sae.cli.main import main


def _run_json(seed: int, draw_count: int, capsys) -> dict[str, object]:
    assert (
        main(
            [
                "research",
                "simulate",
                "--seed",
                str(seed),
                "--draw-count",
                str(draw_count),
                "--format",
                "json",
            ]
        )
        == 0
    )
    return json.loads(capsys.readouterr().out)


def test_research_cli_pipeline_preserves_reproducibility_and_frequency_invariants(
    capsys,
) -> None:
    first = _run_json(seed=2026, draw_count=137, capsys=capsys)
    second = _run_json(seed=2026, draw_count=137, capsys=capsys)

    assert first == second
    assert first["provenance"]["execution_context"]["random_seed"] == 2026
    assert first["provenance"]["configuration"] == {"draw_count": 137}
    assert first["payload"]["draw_count"] == 137
    assert first["execution_metadata"]["random_seed"] == 2026

    frequencies = first["payload"]["number_frequencies"]
    assert len(frequencies) == 90
    assert set(frequencies) == {str(number) for number in range(1, 91)}
    assert sum(frequencies.values()) == 6 * 137
    assert all(0 <= count <= 137 for count in frequencies.values())
