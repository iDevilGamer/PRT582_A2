import ast


def parse_source(source):
    return ast.parse(source)


def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()

    return parse_source(source)
