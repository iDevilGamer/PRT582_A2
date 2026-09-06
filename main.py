import argparse

from analyser.report import analyse_file


def print_report(report):
    print("=" * 50)
    print("          PYTHON STATIC CODE ANALYSER")
    print("=" * 50)

    print("\nComplexity")
    print("-" * 50)
    print(f"Cyclomatic complexity: {report['complexity']}")

    print("\nUnused Variables")
    print("-" * 50)

    if report["unused_variables"]:
        for variable in report["unused_variables"]:
            line = report["locations"]["unused_variables"].get(variable)
            print(f"{variable} (line {line})")
    else:
        print("None detected")

    print("\nDuplicate Code")
    print("-" * 50)

    if report["duplicates"]:
        for duplicate in report["duplicates"]:
            line = report["locations"]["duplicates"].get(duplicate)
            print(f"{duplicate.strip()} (line {line})")
    else:
        print("None detected")

    print("\nNaming Violations")
    print("-" * 50)

    if report["naming_violations"]:
        for name in report["naming_violations"]:
            line = report["locations"]["naming_violations"].get(name)
            print(f"{name} (line {line})")
    else:
        print("None detected")

    print("\nMetrics")
    print("-" * 50)

    metrics = report["metrics"]

    print(f"Functions: {metrics['function_count']}")
    print(f"Classes: {metrics['class_count']}")
    print(f"Imports: {metrics['import_count']}")
    print(f"Logical LOC: {metrics['logical_loc']}")

    print("\n" + "=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Analyse a Python source file statically."
    )

    parser.add_argument(
        "file",
        help="Path to the Python file to analyse"
    )

    args = parser.parse_args()

    try:
        report = analyse_file(args.file)

    except FileNotFoundError:
        print(f"Error: file not found: {args.file}")
        return 1

    except SyntaxError as error:
        print(
            f"Error: invalid Python syntax "
            f"at line {error.lineno}: {error.msg}"
        )
        return 1

    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())