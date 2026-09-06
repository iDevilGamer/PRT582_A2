import ast
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

def test_parse_file_reads_and_parses_python_file(tmp_path):
    file_path = tmp_path / "example.py"
    file_path.write_text("x = 10\n", encoding="utf-8")

    tree = parse_file(file_path)

    assert isinstance(tree, ast.Module)
    assert len(tree.body) == 1