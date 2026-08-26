from sae.analytics.probability.engine import ProbabilityEngine
from sae.kernel.collections import Combination
from sae.kernel.dataset import Dataset
from sae.kernel.domain import Draw, DrawDate, DrawId
from sae.kernel.foundation import Number


def build_combination(*values: int) -> Combination:
    return Combination(*(Number(value) for value in values))


def build_draw(
    draw_id: int,
    day: int,
    values: tuple[int, ...],
) -> Draw:
    return Draw(
        id=DrawId(draw_id),
        date=DrawDate.from_ymd(2026, 1, day),
        combination=build_combination(*values),
    )


def test_analyze_single_draw() -> None:
    draw = build_draw(
        draw_id=1,
        day=7,
        values=(1, 2, 3, 4, 5, 6),
    )
    dataset = Dataset([draw])

    result = ProbabilityEngine.analyze(dataset)

    assert result.draw_count == 1

    for value in range(1, 7):
        assert result.probability(Number(value)) == 1.0

    assert result.probability(Number(7)) == 0.0
    assert result.probability(Number(90)) == 0.0


def test_analyze_multiple_draws() -> None:
    dataset = Dataset(
        [
            build_draw(
                draw_id=1,
                day=7,
                values=(1, 2, 3, 4, 5, 6),
            ),
            build_draw(
                draw_id=2,
                day=10,
                values=(1, 2, 7, 8, 9, 10),
            ),
            build_draw(
                draw_id=3,
                day=14,
                values=(1, 11, 12, 13, 14, 15),
            ),
        ]
    )

    result = ProbabilityEngine.analyze(dataset)

    assert result.draw_count == 3

    assert result.probability(Number(1)) == 1.0
    assert result.probability(Number(2)) == 2 / 3

    for value in range(3, 7):
        assert result.probability(Number(value)) == 1 / 3

    for value in range(7, 16):
        assert result.probability(Number(value)) == 1 / 3

    assert result.probability(Number(90)) == 0.0


def test_analyze_counts_repeated_numbers_across_draws() -> None:
    dataset = Dataset(
        [
            build_draw(
                draw_id=1,
                day=7,
                values=(10, 20, 30, 40, 50, 60),
            ),
            build_draw(
                draw_id=2,
                day=10,
                values=(10, 20, 30, 70, 80, 90),
            ),
        ]
    )

    result = ProbabilityEngine.analyze(dataset)

    assert result.probability(Number(10)) == 1.0
    assert result.probability(Number(20)) == 1.0
    assert result.probability(Number(30)) == 1.0

    assert result.probability(Number(40)) == 0.5
    assert result.probability(Number(50)) == 0.5
    assert result.probability(Number(60)) == 0.5

    assert result.probability(Number(70)) == 0.5
    assert result.probability(Number(80)) == 0.5
    assert result.probability(Number(90)) == 0.5


def test_analyze_empty_dataset() -> None:
    dataset = Dataset([])

    result = ProbabilityEngine.analyze(dataset)

    assert result.draw_count == 0

    for value in range(1, 91):
        assert result.probability(Number(value)) == 0.0


def test_analyze_does_not_modify_dataset() -> None:
    draws = [
        build_draw(
            draw_id=1,
            day=7,
            values=(1, 2, 3, 4, 5, 6),
        ),
        build_draw(
            draw_id=2,
            day=10,
            values=(7, 8, 9, 10, 11, 12),
        ),
    ]

    dataset = Dataset(draws)
    original_draws = dataset.draws

    ProbabilityEngine.analyze(dataset)

    assert dataset.draws == original_draws
    assert dataset.size == 2


def test_analyze_is_deterministic() -> None:
    dataset = Dataset(
        [
            build_draw(
                draw_id=1,
                day=7,
                values=(1, 2, 3, 4, 5, 6),
            ),
            build_draw(
                draw_id=2,
                day=10,
                values=(1, 2, 7, 8, 9, 10),
            ),
        ]
    )

    first = ProbabilityEngine.analyze(dataset)
    second = ProbabilityEngine.analyze(dataset)

    assert first == second
