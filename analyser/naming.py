import ast
import re


def find_naming_violations(tree):
    violations = []

    # Identify module-level constant assignments.
    constant_names = set()

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    constant_names.add(target.id)

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id.startswith("_"):
                continue

            if node.id in constant_names:
                if not re.fullmatch(r"[A-Z][A-Z0-9_]*", node.id):
                    violations.append(node.id)
            elif not re.fullmatch(r"[a-z_][a-z0-9_]*", node.id):
                violations.append(node.id)

        elif isinstance(node, ast.ClassDef):
            if not re.fullmatch(r"[A-Z][a-zA-Z0-9]*", node.name):
                violations.append(node.name)

        elif isinstance(node, ast.FunctionDef):
            if not re.fullmatch(r"[a-z_][a-z0-9_]*", node.name):
                violations.append(node.name)

    return violations