"""
Unit tests for scripts/version.py
"""

import pytest

from scripts import version

CURRENT_VERSION = "1.2.3"
NEW_VERSION_PATCH = "1.2.4"


def test_get_version(mocker):
    """
    Check that get_version() correctly retrieves the version number.
    """
    # Arrange
    mocker.patch(
        "subprocess.run", return_value=mocker.Mock(stdout=f"pkg_name {CURRENT_VERSION}")
    )

    # Act & Assert
    assert version.get_version() == CURRENT_VERSION


def test_get_branch(mocker):
    """
    Check that get_branch() correctly retrieves the branch name.
    """
    # Arrange
    branch_name = "my-branch-name"
    mocker.patch("subprocess.run", return_value=mocker.Mock(stdout=branch_name))

    # Act & Assert
    assert version.get_branch() == branch_name


def test_update_init_py_version(mocker):
    """
    Check that update_init_py_version() correctly updates
    the __version__ in __init__.py.
    """
    # Arrange
    open_mock = mocker.patch(  # Mock file read/write
        "builtins.open",
        new_callable=mocker.mock_open,
    )

    # Act
    version.update_init_py_version(CURRENT_VERSION, NEW_VERSION_PATCH)

    # Assert
    assert open_mock.call_count == 2


def test_git_add_commit_version_tag(mocker):
    """
    Check that git_add_commit_version_tag() correctly performs git add,
    git commit, and tagging.
    """
    # Arrange
    mock_subprocess_run = mocker.patch("subprocess.run")

    # Act
    version.git_add_commit_version_tag(NEW_VERSION_PATCH)

    # Assert
    mock_subprocess_run.assert_has_calls(
        [
            mocker.call(["git", "add", "scripts/__init__.py"], check=True),
            mocker.call(["git", "add", "pyproject.toml"], check=True),
            mocker.call(
                ["git", "commit", "-m", f"Bump version to {NEW_VERSION_PATCH}"],
                check=True,
            ),
            mocker.call(["git", "tag", f"v{NEW_VERSION_PATCH}"], check=True),
        ],
        any_order=False,
    )


class TestIsCleanMainBranch:
    """
    Test suite for is_clean_main_branch function
    """

    def test_is_clean_main_branch_success(self, mocker):
        """
        Check that True is returned when on the main branch
        with no uncommitted or unpushed changes.
        """
        # Arrange
        mocker.patch(
            "subprocess.run", return_value=mocker.Mock(stdout="## main...origin/main")
        )

        # Act & Assert
        assert version.is_clean_main_branch() is True

    def test_is_clean_main_branch_not_main_branch(self, mocker):
        """
        Check that False is returned when not on the main branch.
        """
        # Arrange
        mocker.patch(
            "subprocess.run",
            return_value=mocker.Mock(stdout="## not-main...origin/not-main"),
        )

        # Act & Assert
        assert version.is_clean_main_branch() is False

    def test_is_clean_main_branch_uncommitted_changes(self, mocker):
        """
        Check that False is returned when there are uncommitted changes.
        """
        # Arrange
        mocker.patch(
            "subprocess.run",
            return_value=mocker.Mock(stdout="## main...origin/main\n M README.md"),
        )

        # Act & Assert
        assert version.is_clean_main_branch() is False


class TestCheckBranch:
    """
    Test suite for check_branch function
    """

    def test_check_branch_success(self, mocker):
        """
        Check that no error is raised when on the main branch
        with no uncommitted or unpushed changes.
        """
        # Arrange
        mocker.patch("scripts.version.get_branch", return_value="main")
        mocker.patch("scripts.version.is_clean_main_branch", return_value=True)

        # Act & Assert
        version.check_branch()  # No exception should be raised; the test should pass

    def test_check_branch_not_main_branch(self, mocker):
        """
        Check that an error is raised when not on the main branch.
        """
        # Arrange
        mocker.patch("scripts.version.get_branch", return_value="not-main")

        # Act & Assert
        with pytest.raises(RuntimeError) as e:
            version.check_branch()
        assert (
            str(e.value)
            == "The current Git branch is not 'main': not-main\n"
            + "Please switch to the 'main' branch before running this.\n"
            + "Aborting version bump."
        )

    def test_check_branch_uncommitted_changes(self, mocker):
        """
        Check that an error is raised when there are uncommitted changes.
        """
        # Arrange
        mocker.patch("scripts.version.get_branch", return_value="main")
        mocker.patch("scripts.version.is_clean_main_branch", return_value=False)

        # Act & Assert
        with pytest.raises(RuntimeError) as e:
            version.check_branch()
        assert (
            str(e.value)
            == "There are uncommitted or unpushed changes.\n"
            + "Please ensure the 'main' branch is clean before running this.\n"
            + "Aborting version bump."
        )


class TestBumpVersion:
    """
    Test suite for bump_version function
    """

    def test_bump_version_success(self, mocker):
        """
        Check that bump_version function works correctly.
        """
        # Arrange
        mocker.patch(
            "scripts.version.get_version",
            side_effect=[CURRENT_VERSION, NEW_VERSION_PATCH],
        )
        mocker.patch("scripts.version.check_branch")
        mocker.patch("subprocess.run")
        mock_update_init_py_version = mocker.patch(
            "scripts.version.update_init_py_version"
        )
        mock_git_add_commit_version_tag = mocker.patch(
            "scripts.version.git_add_commit_version_tag"
        )
        mock_print = mocker.patch("builtins.print")

        # Act
        version.bump_version("patch")

        # Assert
        mock_update_init_py_version.assert_called_once_with(
            CURRENT_VERSION, NEW_VERSION_PATCH
        )
        mock_git_add_commit_version_tag.assert_called_once_with(NEW_VERSION_PATCH)
        mock_print.assert_called_once()

    def test_bump_version_invalid_version_type(self):
        """
        Check that a ValueError is raised when an invalid version_type is specified.
        """
        # Act & Assert
        with pytest.raises(ValueError) as e:
            version.bump_version("invalid")
        assert str(e.value) == "version_type must be 'major', 'minor', or 'patch'"


class TestMajorMinorPatch:
    """
    Test suite for major, minor, patch functions
    """

    def test_major(self, mocker):
        """
        Check that major function works correctly.
        """
        # Arrange
        mock_bump_version = mocker.patch("scripts.version.bump_version")

        # Act
        version.major()

        # Assert
        mock_bump_version.assert_called_once_with("major")

    def test_minor(self, mocker):
        """
        Check that minor function works correctly.
        """
        # Arrange
        mock_bump_version = mocker.patch("scripts.version.bump_version")

        # Act
        version.minor()

        # Assert
        mock_bump_version.assert_called_once_with("minor")

    def test_patch(self, mocker):
        """
        Check that patch function works correctly.
        """
        # Arrange
        mock_bump_version = mocker.patch("scripts.version.bump_version")

        # Act
        version.patch()

        # Assert
        mock_bump_version.assert_called_once_with("patch")
