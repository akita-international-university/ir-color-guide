"""
Script for version management like Node.js's `npm version [major|minor|patch]`.
It updates the `version` in pyproject.toml according to semantic versioning,
commits the change to git, and tags it with `vX.Y.Z`.
By defining it in pyproject.toml's [tool.poetry.scripts],
it can be run as `poetry run version_[major|minor|patch]`.
"""

import subprocess


def get_version() -> str:
    """
    Get the `version` from pyproject.toml.

    Returns:
        str: a version number in X.Y.Z format according to Semantic Versioning,
            without a leading `v` (e.g., 1.2.3).
    """
    result = subprocess.run(
        ["poetry", "version"], check=True, text=True, stdout=subprocess.PIPE
    )
    return result.stdout.split(" ")[1].strip()


def get_branch() -> str:
    """Get the current Git branch name."""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return result.stdout.strip()


def update_init_py_version(current_version: str, new_version: str) -> None:
    """
    Update the __version__ in scripts/__init__.py.

    Args:
        current_version (str):
            Current version number in X.Y.Z format according to Semantic Versioning,
            without a leading `v` (e.g., 1.2.3).
        new_version (str):
            New version number in X.Y.Z format according to Semantic Versioning,
            without a leading `v` (e.g., 1.2.3).
    """
    # Read the entire __init__.py and replace only the __version__ line
    with open("scripts/__init__.py", "r", encoding="utf-8") as fread:
        script_text = fread.read()
    with open("scripts/__init__.py", "w", encoding="utf-8", newline="\n") as fwrite:
        script_text = script_text.replace(
            f'__version__ = "{current_version}"', f'__version__ = "{new_version}"'
        )
        fwrite.write(script_text)


def git_add_commit_version_tag(new_version: str) -> None:
    """
    Commit the version update by running git add and git commit.

    Args:
        new_version (str):
            New version number in X.Y.Z format according to Semantic Versioning,
            without a leading `v` (e.g., 1.2.3).
    """
    # Commit the version update
    subprocess.run(["git", "add", "scripts/__init__.py"], check=True)
    subprocess.run(["git", "add", "pyproject.toml"], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Bump version to {new_version}"], check=True
    )
    # Tag the new version
    subprocess.run(["git", "tag", f"v{new_version}"], check=True)


def is_clean_main_branch() -> bool:
    """
    Return True if the current Git branch is 'main'
    and there are no uncommitted or unpushed changes.
    Return False otherwise.

    Returns:
        bool: True if on clean 'main' branch, False otherwise.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain", "--branch"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    lines = result.stdout.strip().split("\n")
    if len(lines) == 1 and lines[0] == "## main...origin/main":
        return True
    return False


def check_branch() -> None:
    """
    Checks that the current Git branch is 'main'
    and that there are no uncommitted or unpushed changes.

    Raises:
        RuntimeError: if the current branch is not 'main'
                      or if there are uncommitted or unpushed changes.
    """
    current_branch = get_branch()
    if not current_branch == "main":
        raise RuntimeError(
            f"The current Git branch is not 'main': {current_branch}\n"
            "Please switch to the 'main' branch before running this.\n"
            "Aborting version bump."
        )
    if not is_clean_main_branch():
        raise RuntimeError(
            "There are uncommitted or unpushed changes.\n"
            "Please ensure the 'main' branch is clean before running this.\n"
            "Aborting version bump."
        )


def bump_version(version_type: str) -> None:
    """
    Update the `version` in pyproject.toml according to semantic versioning,
    commit the changes to git, and tag the commit with `vX.Y.Z`.

    Args:
        version_type (str): "major", "minor", or "patch"
    Raises:
        ValueError: if version_type is not one of "major", "minor", or "patch"
    """
    if version_type not in ["major", "minor", "patch"]:
        raise ValueError("version_type must be 'major', 'minor', or 'patch'")
    # Check that the current Git branch is 'main' and there are no uncommitted or unpushed changes
    check_branch()
    # Get the current version
    current_version = get_version()
    # Update the version in pyproject.toml
    subprocess.run(["poetry", "version", version_type], check=True)
    # Get the updated version
    new_version = get_version()
    # Update __version__ in scripts/__init__.py
    update_init_py_version(current_version, new_version)
    # Commit and tag the version update
    git_add_commit_version_tag(new_version)
    # Completion message
    message = (
        f"Bumped version to {new_version}.\n"
        "Don't forget to push the changes and the tag to the remote repository by running:\n\n"
        "\tgit push\n"
        "\tgit push --tags"
    )
    print(message)


def major():
    """
    Major version bump. Apply when there are backward-incompatible changes.
    Example: v1.1.0 -> v2.0.0
    """
    bump_version("major")


def minor():
    """
    Minor version bump. Apply when there are backward-compatible new features.
    Example: v1.1.0 -> v1.2.0
    """
    bump_version("minor")


def patch():
    """
    Patch version bump. Apply when there are backward-compatible bug fixes or minor changes.
    Example: v1.1.0 -> v1.1.1
    """
    bump_version("patch")
