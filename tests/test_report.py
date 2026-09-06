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