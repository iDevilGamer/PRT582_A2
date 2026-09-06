import ast
import re


def find_naming_violations(tree):
    violations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id.startswith("_"):
                continue

            if not re.fullmatch(r"[a-z_][a-z0-9_]*", node.id):
                violations.append(node.id)

        elif isinstance(node, ast.ClassDef):
            if not re.fullmatch(r"[A-Z][a-zA-Z0-9]*", node.name):
                violations.append(node.name)

    return violations