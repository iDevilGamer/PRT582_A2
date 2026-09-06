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

