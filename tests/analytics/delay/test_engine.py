from sae.analytics.delay.engine import DelayEngine
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

    result = DelayEngine.analyze(dataset)

    assert result.draw_count == 1

    for value in range(1, 7):
        assert result.delay(Number(value)) == 0

    assert result.delay(Number(7)) is None
    assert result.delay(Number(90)) is None


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

    result = DelayEngine.analyze(dataset)

    assert result.draw_count == 3

    assert result.delay(Number(1)) == 0
    assert result.delay(Number(2)) == 1

    for value in range(7, 11):
        assert result.delay(Number(value)) == 1

    for value in range(11, 16):
        assert result.delay(Number(value)) == 0

    for value in range(3, 7):
        assert result.delay(Number(value)) == 2

    assert result.delay(Number(90)) is None


def test_analyze_counts_delay_from_most_recent_occurrence() -> None:
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
            build_draw(
                draw_id=3,
                day=14,
                values=(10, 20, 30, 40, 50, 60),
            ),
        ]
    )

    result = DelayEngine.analyze(dataset)

    assert result.delay(Number(10)) == 0
    assert result.delay(Number(20)) == 0
    assert result.delay(Number(30)) == 0
    assert result.delay(Number(40)) == 0
    assert result.delay(Number(50)) == 0
    assert result.delay(Number(60)) == 0

    assert result.delay(Number(70)) == 1
    assert result.delay(Number(80)) == 1
    assert result.delay(Number(90)) == 1


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

    DelayEngine.analyze(dataset)

    assert dataset.draws == original_draws
    assert dataset.size == 2


def test_analyze_empty_dataset() -> None:
    dataset = Dataset([])

    result = DelayEngine.analyze(dataset)

    assert result.draw_count == 0

    for value in range(1, 91):
        assert result.delay(Number(value)) is None


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

    first = DelayEngine.analyze(dataset)
    second = DelayEngine.analyze(dataset)

    assert first == second
