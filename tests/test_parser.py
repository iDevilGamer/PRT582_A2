import pytest
from analyser.parser import parse_file, parse_source


def test_valid_python_source_is_parsed():
    source = """
def calculate_total(value):
    return value + 10
"""

    tree = parse_source(source)

    assert tree is not None


def test_empty_source_is_parsed():
    source = ""

    tree = parse_source(source)

    assert tree is not None
    

def test_comment_only_source_is_parsed():
    source = """
# This is a comment
# Another comment
"""

    tree = parse_source(source)

    assert tree is not None


def test_invalid_python_source_raises_syntax_error():
    source = """
def calculate_total(value)
    return value + 10
"""

    with pytest.raises(SyntaxError):
        parse_source(source)


def test_nonexistent_file_raises_file_not_found_error():
    file_path = "does_not_exist.py"

    with pytest.raises(FileNotFoundError):
        parse_file(file_path)

