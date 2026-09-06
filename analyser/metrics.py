import ast


def calculate_metrics(tree):
    function_count = 0
    class_count = 0
    import_count = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_count += 1
        elif isinstance(node, ast.ClassDef):
            class_count += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            import_count += 1

    return {
        "function_count": function_count,
        "class_count": class_count,
        "import_count": import_count
    }