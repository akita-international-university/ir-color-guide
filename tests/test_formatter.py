"""
Unit tests for ./scripts/formatter.py
"""

from scripts import formatter


def test_main_on_windows(mocker):
    """
    Test for the main() function on Windows environment.
    """
    # Arrange
    mock_os = mocker.patch("scripts.formatter.os")
    mock_os.name = "nt"  # Mock Windows environment
    mock_subprocess = mocker.patch("subprocess.run")
    mock_print = mocker.patch("builtins.print")

    # Act
    formatter.main()

    # Assert
    mock_subprocess.assert_has_calls(
        [
            mocker.call(["npx", "prettier", "--write", "."], check=True, shell=True),
            mocker.call(["isort", "."], check=True),
            mocker.call(["black", "."], check=True),
        ]
    )
    mock_print.assert_has_calls(
        [
            mocker.call("Formatting with Prettier..."),
            mocker.call("Formatting done (Prettier)."),
            mocker.call("Formatting with isort..."),
            mocker.call("Formatting done (isort)."),
            mocker.call("Formatting with black..."),
            mocker.call("Formatting done (black)."),
            mocker.call("All formatting complete."),
        ]
    )


def test_main_on_macos(mocker):
    """
    Test for the main() function on macOS environment.
    """
    # Arrange
    mock_os = mocker.patch("scripts.formatter.os")
    mock_os.name = "posix"  # Mock macOS environment
    mock_subprocess = mocker.patch("subprocess.run")
    mock_print = mocker.patch("builtins.print")

    # Act
    formatter.main()

    # Assert
    mock_subprocess.assert_has_calls(
        [
            mocker.call(["npx", "prettier", "--write", "."], check=True),
            mocker.call(["isort", "."], check=True),
            mocker.call(["black", "."], check=True),
        ]
    )
    mock_print.assert_has_calls(
        [
            mocker.call("Formatting with Prettier..."),
            mocker.call("Formatting done (Prettier)."),
            mocker.call("Formatting with isort..."),
            mocker.call("Formatting done (isort)."),
            mocker.call("Formatting with black..."),
            mocker.call("Formatting done (black)."),
            mocker.call("All formatting complete."),
        ]
    )
