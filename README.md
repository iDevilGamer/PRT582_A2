# PRT582_A2 – Python Static Code Analyser

## Overview

This project is a Python static code analyser developed for the PRT582 Assignment 2. The analyser examines Python source code without executing it and reports several software quality characteristics.

The project was developed using a Test-Driven Development (TDD) approach. Automated tests are provided using pytest.

## Features

The analyser currently provides the following analysis:

- Cyclomatic Complexity
  - Calculates a baseline complexity of 1.
  - Detects decision points such as if, elif, except, and, and or.
  - Accounts for nested decision structures.

- Code Duplication
  - Detects three or more identical consecutive source-code lines.
  - Reports the first detected line of each duplicate block.

- Naming Convention Analysis
  - Checks variable and function names for snake_case.
  - Checks class names for PascalCase.
  - Checks module-level constants for uppercase naming.
  - Ignores underscore-prefixed names.

- Unused Variable Detection
  - Detects local variables that are assigned but never used.
  - Detects unused function parameters.
  - Ignores intentionally unused parameters beginning with _.

- Source Code Metrics
  - Counts functions.
  - Counts classes.
  - Counts imports.
  - Calculates logical lines of code (LOC), excluding documentation strings.

- Python Parsing
  - Parses Python source code using Python's ast module.
  - Reports invalid Python syntax without executing the source file.

- Command-Line Interface
  - Analyses a Python file from the command line.
  - Displays analysis results and source-code locations.
  - Provides error messages for missing files and invalid Python syntax.

## Requirements

- Python 3.14 or compatible Python 3 version
- pytest
- pytest-cov

## Running the Analyser

From the project directory, run:

python main.py example_test.py

The analyser will display the detected complexity, unused variables, duplicate code, naming violations, and source-code metrics.

To analyse another Python file:

python main.py path/to/file.py

## Running the Tests

Run the complete test suite with:

python -m pytest -v

The project currently contains 71 automated tests.

The latest test run produced:

71 passed

## Test Coverage

Coverage can be measured using:

python -m pytest --cov=analyser --cov-report=term-missing

The current test suite provides:

TOTAL    134 statements    6 missed    96% coverage

## Development Approach

The project follows a Test-Driven Development approach:

1. Requirements and expected behaviour were defined.
2. Tests were designed for the required functionality.
3. Implementation was developed to satisfy the tests.
4. Tests were repeatedly executed during development.
5. Integration tests were added for the command-line interface.
6. Final testing confirmed that all automated tests pass.

The analyser uses Python's Abstract Syntax Tree (ast) module to inspect source code rather than executing the analysed program.
