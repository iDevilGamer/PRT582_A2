from analyser.complexity import calculate_complexity
from analyser.variables import find_unused_variables
from analyser.duplication import find_duplicate_lines
from analyser.naming import find_naming_violations
from analyser.metrics import calculate_metrics


def generate_report(tree, source):
    unused_variables = find_unused_variables(tree)

    locations = {
        "unused_variables": {}
    }

    for node in tree.body:
        if hasattr(node, "body"):
            for child in node.body:
                if hasattr(child, "targets"):
                    for target in child.targets:
                        if hasattr(target, "id") and target.id in unused_variables:
                            locations["unused_variables"][target.id] = target.lineno

    return {
        "complexity": calculate_complexity(tree),
        "unused_variables": unused_variables,
        "duplicates": find_duplicate_lines(tree, source),
        "naming_violations": find_naming_violations(tree),
        "metrics": calculate_metrics(tree),
        "locations": locations
    }