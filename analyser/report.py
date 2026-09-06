import ast

from analyser.parser import parse_source
from analyser.complexity import calculate_complexity
from analyser.variables import find_unused_variables
from analyser.duplication import find_duplicate_lines
from analyser.naming import find_naming_violations
from analyser.metrics import calculate_metrics


def generate_report(tree, source):
    unused_variables = find_unused_variables(tree)
    naming_violations = find_naming_violations(tree)
    duplicates = find_duplicate_lines(tree, source)

    locations = {
        "unused_variables": {},
        "naming_violations": {},
        "duplicates": {}
    }

    # Find locations of unused variables.
    for node in tree.body:
        if hasattr(node, "body"):
            for child in node.body:
                if hasattr(child, "targets"):
                    for target in child.targets:
                        if hasattr(target, "id") and target.id in unused_variables:
                            locations["unused_variables"][target.id] = target.lineno

    # Find locations of naming violations.
    for node in ast.walk(tree):
        if hasattr(node, "name") and node.name in naming_violations:
            locations["naming_violations"][node.name] = node.lineno

        if isinstance(node, ast.Name):
            if node.id in naming_violations and isinstance(node.ctx, ast.Store):
                locations["naming_violations"][node.id] = node.lineno

    # Find locations of duplicate code.
    lines = source.splitlines()

    for i in range(len(lines) - 2):
        if lines[i] == lines[i + 1] == lines[i + 2]:
            if (
                lines[i] in duplicates
                and lines[i] not in locations["duplicates"]
            ):
                locations["duplicates"][lines[i]] = i + 1

    return {
        "complexity": calculate_complexity(tree),
        "unused_variables": unused_variables,
        "duplicates": duplicates,
        "naming_violations": naming_violations,
        "metrics": calculate_metrics(tree),
        "locations": locations
    }


def analyse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()

    tree = parse_source(source)

    return generate_report(tree, source)