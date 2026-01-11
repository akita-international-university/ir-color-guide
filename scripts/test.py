"""
Script to run a suite of unit tests.
Also runs formatters and linters.
"""

import subprocess


def main():
    """
    Run the suite of formatters defined in scripts.formatter.py,
    and linters defined in scripts.linter.py,
    then run pytest.
    """
    # First, run formatters and linters
    subprocess.run(["poetry", "run", "linter"], check=True)
    # Run pytest
    subprocess.run(["poetry", "run", "pytest"], check=True)
