from sae.analytics.frequency.engine import FrequencyEngine
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

    result = FrequencyEngine.analyze(dataset)

    assert result.draw_count == 1

    for value in range(1, 7):
        assert result.frequency(Number(value)) == 1

    assert result.frequency(Number(7)) == 0
    assert result.frequency(Number(90)) == 0


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

    result = FrequencyEngine.analyze(dataset)

    assert result.draw_count == 3

    assert result.frequency(Number(1)) == 3
    assert result.frequency(Number(2)) == 2

    for value in range(3, 7):
        assert result.frequency(Number(value)) == 1

    for value in range(7, 16):
        assert result.frequency(Number(value)) == 1

    assert result.frequency(Number(90)) == 0


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

    result = FrequencyEngine.analyze(dataset)

    assert result.frequency(Number(10)) == 2
    assert result.frequency(Number(20)) == 2
    assert result.frequency(Number(30)) == 2

    assert result.frequency(Number(40)) == 1
    assert result.frequency(Number(50)) == 1
    assert result.frequency(Number(60)) == 1

    assert result.frequency(Number(70)) == 1
    assert result.frequency(Number(80)) == 1
    assert result.frequency(Number(90)) == 1


def test_analyze_empty_dataset() -> None:
    dataset = Dataset([])

    result = FrequencyEngine.analyze(dataset)

    assert result.draw_count == 0

    for value in range(1, 91):
        assert result.frequency(Number(value)) == 0


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

    FrequencyEngine.analyze(dataset)

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

    first = FrequencyEngine.analyze(dataset)
    second = FrequencyEngine.analyze(dataset)

    assert first == second
