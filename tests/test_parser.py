from analyser.parser import parse_source


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