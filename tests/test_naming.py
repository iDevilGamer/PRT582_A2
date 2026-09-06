from analyser.parser import parse_source
from analyser.naming import find_naming_violations


def test_valid_variable_name_is_not_reported():
    source = """
def calculate_total():
    total_amount = 100
    return total_amount
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "total_amount" not in violations

def test_invalid_variable_name_is_reported():
    source = """
def calculate_total():
    totalAmount = 100
    return totalAmount
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "totalAmount" in violations


def test_valid_class_name_is_not_reported():
    source = """
class ShoppingCart:
    pass
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "ShoppingCart" not in violations


def test_invalid_class_name_is_reported():
    source = """
class shopping_cart:
    pass
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "shopping_cart" in violations
    
def test_valid_function_name_is_not_reported():
    source = """
def calculate_total():
    return 100
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "calculate_total" not in violations
    
def test_invalid_function_name_is_reported():
    source = """
def calculateTotal():
    return 100
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "calculateTotal" in violations

def test_valid_constant_name_is_not_reported():
    source = """
MAX_RETRIES = 3

def calculate_total():
    return MAX_RETRIES
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "MAX_RETRIES" not in violations

def test_invalid_constant_name_is_reported():
    source = """
max_retries = 3

def calculate_total():
    return max_retries
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "max_retries" in violations

def test_constant_name_with_digits_is_valid():
    source = """
MAX_RETRIES_2 = 3
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "MAX_RETRIES_2" not in violations

def test_mixed_case_constant_name_is_reported():
    source = """
MAX_Retries = 3
"""

    tree = parse_source(source)

    violations = find_naming_violations(tree)

    assert "MAX_Retries" in violations