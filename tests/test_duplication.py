from analyser.parser import parse_source
from analyser.duplication import find_duplicate_lines


def test_three_identical_consecutive_lines_are_detected():
    source = """
def first_function():
    print("hello")
    print("hello")
    print("hello")
"""

    tree = parse_source(source)

    duplicates = find_duplicate_lines(tree, source)

    assert duplicates

def test_two_identical_consecutive_lines_are_not_detected():
    source = """
def first_function():
    print("hello")
    print("hello")
"""

    tree = parse_source(source)

    duplicates = find_duplicate_lines(tree, source)

    assert not duplicates

def test_exactly_three_identical_consecutive_lines_are_detected():
    source = """
def first_function():
    print("hello")
    print("hello")
    print("hello")
"""

    tree = parse_source(source)

    duplicates = find_duplicate_lines(tree, source)

    assert duplicates

def test_multiple_duplicate_blocks_are_detected():
    source = """
def first_function():
    print("hello")
    print("hello")
    print("hello")


def second_function():
    print("world")
    print("world")
    print("world")
"""

    tree = parse_source(source)

    duplicates = find_duplicate_lines(tree, source)

    assert len(duplicates) >= 2


