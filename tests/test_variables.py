from analyser.parser import parse_source
from analyser.variables import find_unused_variables


def test_unused_variable_is_detected():
    source = """
def calculate_total(value):
    tax = 10
    return value + 10
"""

    tree = parse_source(source)

    unused_variables = find_unused_variables(tree)

    assert "tax" in unused_variables


def test_used_variable_is_not_reported():
    source = """
def calculate_total(value):
    tax = 10
    return value + tax
"""

    tree = parse_source(source)

    unused_variables = find_unused_variables(tree)

    assert "tax" not in unused_variables


def test_multiple_unused_variables_are_detected():
    source = """
def calculate_total(value):
    tax = 10
    discount = 5
    return value
"""

    tree = parse_source(source)

    unused_variables = find_unused_variables(tree)

    assert "tax" in unused_variables
    assert "discount" in unused_variables