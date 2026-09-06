import ast


def calculate_metrics(tree):
    function_count = 0
    class_count = 0
    import_count = 0
    logical_loc = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_count += 1
        elif isinstance(node, ast.ClassDef):
            class_count += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            import_count += 1

        if isinstance(node, ast.stmt):
            logical_loc += 1

    # Remove actual module, class, and function docstrings.
    docstring_nodes = set()

    if ast.get_docstring(tree, clean=False) is not None:
        if tree.body and isinstance(tree.body[0], ast.Expr):
            docstring_nodes.add(tree.body[0])

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ast.get_docstring(node, clean=False) is not None:
                if node.body and isinstance(node.body[0], ast.Expr):
                    docstring_nodes.add(node.body[0])

    logical_loc -= len(docstring_nodes)

    return {
        "function_count": function_count,
        "class_count": class_count,
        "import_count": import_count,
        "logical_loc": logical_loc
    }