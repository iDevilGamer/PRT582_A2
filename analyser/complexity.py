import ast


def calculate_complexity(tree):
    complexity = 1

    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While)):
            complexity += 1

    return complexity


