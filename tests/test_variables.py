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

def test_unused_parameter_is_detected():
    source = """
def calculate_total(value, tax):
    return value + 10
"""

    tree = parse_source(source)

    unused_variables = find_unused_variables(tree)

    assert "tax" in unused_variables

def test_underscore_parameter_is_not_reported_as_unused():
    source = """
def calculate_total(value, _tax):
    return value + 10
"""

    tree = parse_source(source)

    unused_variables = find_unused_variables(tree)

    assert "_tax" not in unused_variables

def test_used_parameter_is_not_reported_as_unused():
    source = """
def calculate_total(value, tax):
    return value + tax
"""

    tree = parse_source(source)

    unused_variables = find_unused_variables(tree)

    assert "tax" not in unused_variables
    
def test_unused_variables_in_nested_function_are_detected():
    source = """
def outer_function():
    outer_value = 10

    def inner_function():
        inner_value = 20
        return 5

    return outer_value
"""

    tree = parse_source(source)

    unused_variables = find_unused_variables(tree)

    assert "inner_value" in unused_variables

def test_used_variable_in_nested_function_is_not_reported():
    source = """
def outer():
    value = 10

    def inner():
        return value

    return inner
"""

    tree = parse_source(source)

    result = find_unused_variables(tree)

    assert "value" not in result