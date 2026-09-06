from analyser.parser import parse_source
from analyser.metrics import calculate_metrics


def test_function_count_is_correct():
    source = """
def first_function():
    return 1


def second_function():
    return 2
"""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["function_count"] == 2

def test_class_count_is_correct():
    source = """
class FirstClass:
    pass


class SecondClass:
    pass
"""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["class_count"] == 2

def test_import_count_is_correct():
    source = """
import os
import sys
from pathlib import Path

def calculate_total():
    return 100
"""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["import_count"] == 3

def test_empty_source_has_zero_metrics():
    source = ""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["function_count"] == 0
    assert metrics["class_count"] == 0
    assert metrics["import_count"] == 0

def test_comment_only_source_has_zero_metrics():
    source = """
# This is a comment
# Another comment
"""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["function_count"] == 0
    assert metrics["class_count"] == 0
    assert metrics["import_count"] == 0

def test_logical_loc_is_calculated():
    source = """
# This is a comment

def calculate_total(value):
    tax = 10
    total = value + tax
    return total
"""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["logical_loc"] == 4


def test_comment_only_source_has_zero_logical_loc():
    source = """
# This is a comment
# Another comment
"""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["logical_loc"] == 0

def test_empty_source_has_zero_logical_loc():
    source = ""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["logical_loc"] == 0

def test_docstring_does_not_count_as_logical_loc():
    source = '''
def calculate_total(value):
    """Calculate the total value."""
    return value + 10
'''

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["logical_loc"] == 2

def test_non_docstring_string_expression_counts_as_logical_loc():
    source = '''
def calculate_total(value):
    total = value + 10
    "This is not a docstring."
    return total
'''

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["logical_loc"] == 4

def test_control_flow_statements_count_as_logical_loc():
    source = """
def check_value(value):
    if value > 0:
        return value
    else:
        return 0
"""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["logical_loc"] == 4

def test_loop_statements_count_as_logical_loc():
    source = """
def calculate_total(values):
    total = 0
    for value in values:
        total = total + value
    return total
"""

    tree = parse_source(source)

    metrics = calculate_metrics(tree)

    assert metrics["logical_loc"] == 5