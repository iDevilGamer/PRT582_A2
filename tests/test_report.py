from analyser.parser import parse_source
from analyser.report import generate_report


def test_report_contains_all_analysis_categories():
    source = """
def calculate_total(value):
    unused_value = 10
    if value > 0:
        return value
    return 0
"""

    tree = parse_source(source)

    report = generate_report(tree, source)

    assert "complexity" in report
    assert "unused_variables" in report
    assert "duplicates" in report
    assert "naming_violations" in report
    assert "metrics" in report


def test_report_contains_correct_analysis_results():
    source = """
def calculate_total(value):
    unused_value = 10
    if value > 0:
        return value
    return 0
"""

    tree = parse_source(source)

    report = generate_report(tree, source)

    assert report["complexity"] == 2
    assert "unused_value" in report["unused_variables"]
    assert report["duplicates"] == []
    assert report["naming_violations"] == []
    assert report["metrics"]["function_count"] == 1
    assert report["metrics"]["logical_loc"] == 5

def test_report_includes_location_of_unused_variable():
    source = """
def calculate_total(value):
    unused_value = 10
    return value
"""

    tree = parse_source(source)

    report = generate_report(tree, source)

    assert "locations" in report
    assert "unused_variables" in report["locations"]
    assert report["locations"]["unused_variables"]["unused_value"] == 3