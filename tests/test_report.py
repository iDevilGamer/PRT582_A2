import pytest

from analyser.parser import parse_source
from analyser.report import generate_report
from analyser.parser import parse_file


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


def test_report_includes_location_of_naming_violation():
    source = """
def calculate_total():
    totalAmount = 100
    return totalAmount
"""

    tree = parse_source(source)

    report = generate_report(tree, source)

    assert "naming_violations" in report["locations"]
    assert report["locations"]["naming_violations"]["totalAmount"] == 3
    

def test_report_includes_location_of_duplicate_code():
    source = """
def calculate_total():
    value = 10
    value = 10
    value = 10
    return value
"""

    tree = parse_source(source)

    report = generate_report(tree, source)

    assert "duplicates" in report["locations"]
    assert report["locations"]["duplicates"]["    value = 10"] == 3


def test_report_preserves_analysis_results_with_locations():
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
    assert "locations" in report

def test_invalid_python_source_is_rejected_before_report_generation():
    source = """
def calculate_total(value)
    return value
"""

    with pytest.raises(SyntaxError):
        tree = parse_source(source)
        generate_report(tree, source)
    
def test_missing_python_file_is_rejected():
    file_path = "does_not_exist.py"

    with pytest.raises(FileNotFoundError):
        tree = parse_file(file_path)
        generate_report(tree, "")