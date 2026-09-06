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