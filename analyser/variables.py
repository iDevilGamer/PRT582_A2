import ast


def find_unused_variables(tree):
    unused_variables = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            assigned_variables = set()
            used_variables = set()

            # Function parameters count as assigned variables,
            # except underscore-prefixed parameters.
            for argument in node.args.args:
                if not argument.arg.startswith("_"):
                    assigned_variables.add(argument.arg)

            for child in ast.walk(node):
                if isinstance(child, ast.Name):
                    if isinstance(child.ctx, ast.Store):
                        assigned_variables.add(child.id)
                    elif isinstance(child.ctx, ast.Load):
                        used_variables.add(child.id)

            unused_variables.extend(
                assigned_variables - used_variables
            )

    return unused_variables