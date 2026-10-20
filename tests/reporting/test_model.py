from sae.reporting.model import Report, ReportRow


def test_report_is_immutable() -> None:
    report = Report(
        title="Frequency Report",
        draw_count=10,
        rows=(ReportRow(label="Number 1", value="3"),),
    )

    assert report.title == "Frequency Report"
    assert report.draw_count == 10
    assert report.rows == (ReportRow(label="Number 1", value="3"),)

    try:
        report.title = "Other"  # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("Report must be immutable")
