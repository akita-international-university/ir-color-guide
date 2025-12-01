"""
Script to run code formatters: Prettier for Markdown/HTML (*.tps) and isort/black for Python.
"""

import os
import subprocess


def main():
    """
    Run code formatters.
    """
    # Prettier
    print("Formatting with Prettier...")
    if os.name == "nt":
        # Running on Windows
        subprocess.run(["npx", "prettier", "--write", "."], check=True, shell=True)
    else:
        # Running on other OS
        subprocess.run(["npx", "prettier", "--write", "."], check=True)
    print("Formatting done (Prettier).")
    # isort
    print("Formatting with isort...")
    subprocess.run(["isort", "."], check=True)
    print("Formatting done (isort).")
    # black
    print("Formatting with black...")
    subprocess.run(["black", "."], check=True)
    print("Formatting done (black).")
    print("All formatting complete.")
