from analyser.complexity import calculate_complexity
from analyser.parser import parse_source


def test_simple_function_has_baseline_complexity():
    source = """
def calculate_total(value):
    return value + 10
"""

    tree = parse_source(source)

    complexity = calculate_complexity(tree)

    assert complexity == 1


def test_if_statement_increases_complexity():
    source = """
def calculate_total(value):
    if value > 0:
        return value + 10
    return value
"""

    tree = parse_source(source)

    complexity = calculate_complexity(tree)

    assert complexity == 2

def test_nested_decisions_increase_complexity():
    source = """
def calculate_total(value):
    if value > 0:
        if value < 100:
            return value + 10
    return value
"""

    tree = parse_source(source)

    complexity = calculate_complexity(tree)

    assert complexity == 3
    
def test_and_operator_increases_complexity():
    source = """
def check_value(value):
    if value > 0 and value < 100:
        return True
    return False
"""

    tree = parse_source(source)

    complexity = calculate_complexity(tree)

    assert complexity == 3

def test_or_operator_increases_complexity():
    source = """
def check_value(value):
    if value < 0 or value > 100:
        return False
    return True
"""

    tree = parse_source(source)

    complexity = calculate_complexity(tree)

    assert complexity == 3

def test_except_handler_increases_complexity():
    source = """
def read_value(value):
    try:
        return int(value)
    except ValueError:
        return 0
"""

    tree = parse_source(source)

    complexity = calculate_complexity(tree)

    assert complexity == 2

def test_elif_statement_increases_complexity():
    source = """
def check_value(value):
    if value > 100:
        return "high"
    elif value > 50:
        return "medium"
    return "low"
"""

    tree = parse_source(source)

    complexity = calculate_complexity(tree)

    assert complexity == 3