import subprocess
import sys


def run_cli(file_path):
    return subprocess.run(
        [sys.executable, "main.py", str(file_path)],
        capture_output=True,
        text=True
    )


def test_cli_successfully_analyses_python_file(tmp_path):
    file_path = tmp_path / "example.py"
    file_path.write_text(
        "def hello():\n"
        "    value = 10\n"
        "    return value\n",
        encoding="utf-8"
    )

    result = run_cli(file_path)

    assert result.returncode == 0
    assert "PYTHON STATIC CODE ANALYSER" in result.stdout
    assert "Complexity" in result.stdout
    assert "Metrics" in result.stdout


def test_cli_reports_missing_file():
    result = run_cli("does_not_exist.py")

    assert result.returncode == 1
    assert "Error: file not found: does_not_exist.py" in result.stdout


def test_cli_reports_invalid_python(tmp_path):
    file_path = tmp_path / "invalid.py"
    file_path.write_text(
        "def hello(\n"
        "    print('Hello')\n",
        encoding="utf-8"
    )

    result = run_cli(file_path)

    assert result.returncode == 1
    assert "Error: invalid Python syntax" in result.stdout


def test_cli_handles_empty_file(tmp_path):
    file_path = tmp_path / "empty.py"
    file_path.write_text("", encoding="utf-8")

    result = run_cli(file_path)

    assert result.returncode == 0
    assert "Functions: 0" in result.stdout
    assert "Classes: 0" in result.stdout
    assert "Imports: 0" in result.stdout
    assert "Logical LOC: 0" in result.stdout


def test_cli_output_contains_all_analysis_categories(tmp_path):
    file_path = tmp_path / "example.py"
    file_path.write_text(
        "import math\n"
        "\n"
        "def calculate():\n"
        "    unused_value = 10\n"
        "    return math.sqrt(16)\n",
        encoding="utf-8"
    )

    result = run_cli(file_path)

    assert result.returncode == 0
    assert "Complexity" in result.stdout
    assert "Unused Variables" in result.stdout
    assert "Duplicate Code" in result.stdout
    assert "Naming Violations" in result.stdout
    assert "Metrics" in result.stdout