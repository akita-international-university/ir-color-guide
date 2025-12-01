"""
Script to run linters after running formatters defined in scripts.formatter.py.
"""

import subprocess

# Lint対象のディレクトリ
LINT_TARGET = ["./scripts"]  # , "./tests"]


def main():
    """
    Run linters after running the set of formatters defined in scripts.formatter.py.
    """
    # First, run the formatter
    subprocess.run(["poetry", "run", "formatter"], check=True)
    for target in LINT_TARGET:
        # Run mypy
        print(f"Linting {target} with mypy...")
        subprocess.run(["poetry", "run", "mypy", target], check=True)
        print("mypy linting done.")
        # Run pylint
        print(f"Linting {target} with pylint...")
        subprocess.run(["poetry", "run", "pylint", target], check=True)
        print("pylint linting done.")
    print("All linting complete.")
