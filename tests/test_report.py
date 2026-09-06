import pytest

from analyser.parser import parse_source
from analyser.report import analyse_file, generate_report
from analyser.parser import parse_file
from analyser.complexity import calculate_complexity
from analyser.variables import find_unused_variables
from analyser.duplication import find_duplicate_lines
from analyser.naming import find_naming_violations
from analyser.metrics import calculate_metrics


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
    

def test_analyse_file_accepts_python_file(tmp_path):
    file_path = tmp_path / "sample.py"

    file_path.write_text(
        """
def calculate_total(value):
    return value + 10
""",
        encoding="utf-8"
    )

    report = analyse_file(file_path)

    assert report["complexity"] == 1
    assert report["metrics"]["function_count"] == 1

import ast

from analyser.parser import parse_source
from analyser.complexity import calculate_complexity
from analyser.variables import find_unused_variables
from analyser.duplication import find_duplicate_lines
from analyser.naming import find_naming_violations
from analyser.metrics import calculate_metrics


def generate_report(tree, source):
    unused_variables = find_unused_variables(tree)
    naming_violations = find_naming_violations(tree)
    duplicates = find_duplicate_lines(tree, source)

    locations = {
        "unused_variables": {},
        "naming_violations": {},
        "duplicates": {}
    }

    # Find locations of unused variables.
    for node in tree.body:
        if hasattr(node, "body"):
            for child in node.body:
                if hasattr(child, "targets"):
                    for target in child.targets:
                        if hasattr(target, "id") and target.id in unused_variables:
                            locations["unused_variables"][target.id] = target.lineno

    # Find locations of naming violations.
    for node in ast.walk(tree):
        if hasattr(node, "name") and node.name in naming_violations:
            locations["naming_violations"][node.name] = node.lineno

        if isinstance(node, ast.Name):
            if node.id in naming_violations and isinstance(node.ctx, ast.Store):
                locations["naming_violations"][node.id] = node.lineno

    # Find locations of duplicate code.
    lines = source.splitlines()

    for i in range(len(lines) - 2):
        if lines[i] == lines[i + 1] == lines[i + 2]:
            if (
                lines[i] in duplicates
                and lines[i] not in locations["duplicates"]
            ):
                locations["duplicates"][lines[i]] = i + 1

    return {
        "complexity": calculate_complexity(tree),
        "unused_variables": unused_variables,
        "duplicates": duplicates,
        "naming_violations": naming_violations,
        "metrics": calculate_metrics(tree),
        "locations": locations
    }


def test_analyse_file_rejects_missing_file():
    file_path = "does_not_exist.py"

    with pytest.raises(FileNotFoundError):
        analyse_file(file_path)

def test_analyse_file_does_not_execute_source(tmp_path):
    file_path = tmp_path / "unsafe.py"

    file_path.write_text(
        """
raise RuntimeError("This code must not be executed")
""",
        encoding="utf-8"
    )

    report = analyse_file(file_path)

    assert report is not None

def test_analyse_file_handles_empty_python_file(tmp_path):
    file_path = tmp_path / "empty.py"

    file_path.write_text("", encoding="utf-8")

    report = analyse_file(file_path)

    assert report["complexity"] == 1
    assert report["unused_variables"] == []
    assert report["duplicates"] == []
    assert report["naming_violations"] == []
    assert report["metrics"]["logical_loc"] == 0

def test_analyse_file_handles_comment_only_file(tmp_path):
    file_path = tmp_path / "comments.py"

    file_path.write_text(
        """
# This is a comment
# Another comment
""",
        encoding="utf-8"
    )

    report = analyse_file(file_path)

    assert report["complexity"] == 1
    assert report["unused_variables"] == []
    assert report["duplicates"] == []
    assert report["naming_violations"] == []
    assert report["metrics"]["logical_loc"] == 0

def test_report_has_expected_result_types(tmp_path):
    file_path = tmp_path / "sample.py"

    file_path.write_text(
        """
def calculate_total(value):
    unused_value = 10
    if value > 0:
        return value
    return 0
""",
        encoding="utf-8"
    )

    report = analyse_file(file_path)

    assert isinstance(report["complexity"], int)
    assert isinstance(report["unused_variables"], list)
    assert isinstance(report["duplicates"], list)
    assert isinstance(report["naming_violations"], list)
    assert isinstance(report["metrics"], dict)
    assert isinstance(report["locations"], dict)

def test_analysis_components_can_be_used_independently():
    source = """
def calculate_total(value):
    unused_value = 10
    if value > 0:
        return value
    return 0
"""

    tree = parse_source(source)

    complexity = calculate_complexity(tree)
    unused_variables = find_unused_variables(tree)
    duplicates = find_duplicate_lines(tree, source)
    naming_violations = find_naming_violations(tree)
    metrics = calculate_metrics(tree)

    assert complexity == 2
    assert "unused_value" in unused_variables
    assert duplicates == []
    assert naming_violations == []
    assert metrics["function_count"] == 1


def test_report_preserves_locations_for_multiple_unused_variables():
    source = """
def calculate_total(value):
    first_unused = 10
    second_unused = 20
    return value
"""

    tree = parse_source(source)

    report = generate_report(tree, source)

    assert report["locations"]["unused_variables"]["first_unused"] == 3
    assert report["locations"]["unused_variables"]["second_unused"] == 4

def test_report_preserves_locations_for_multiple_duplicate_blocks():
    source = """
def calculate_total():
    first = 10
    first = 10
    first = 10

    second = 20
    second = 20
    second = 20

    return first + second
"""

    tree = parse_source(source)

    report = generate_report(tree, source)

    assert report["locations"]["duplicates"]["    first = 10"] == 3
    assert report["locations"]["duplicates"]["    second = 20"] == 7

def test_analyse_file_accepts_python_source_file(tmp_path):
    file_path = tmp_path / "example.py"

    file_path.write_text(
        """
import math

def calculate_area(radius):
    return math.pi * radius ** 2
""",
        encoding="utf-8"
    )

    report = analyse_file(file_path)

    assert report["complexity"] == 1
    assert report["metrics"]["function_count"] == 1
    assert report["metrics"]["import_count"] == 1
    assert report["metrics"]["logical_loc"] == 3