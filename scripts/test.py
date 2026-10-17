"""
Script to run a suite of unit tests.
Also runs the palette checks, formatters, and linters.
"""

import subprocess


def main():
    """
    Run the palette checks defined in scripts.validate.py,
    the suite of formatters defined in scripts.formatter.py,
    and linters defined in scripts.linter.py,
    then run pytest.
    """
    # First, check the palettes. This also writes the validation report,
    # which is then formatted by the formatter.
    subprocess.run(["poetry", "run", "validate"], check=True)
    # Run formatters and linters
    subprocess.run(["poetry", "run", "linter"], check=True)
    # Run pytest
    subprocess.run(["poetry", "run", "pytest"], check=True)
