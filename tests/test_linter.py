"""
Unit tests for ./scripts/linter.py
"""

from scripts import linter


def test_main(mocker):
    """
    Test for the main function in linter.py.
    """
    # Arrange
    mock_subprocess = mocker.patch("subprocess.run")
    mock_print = mocker.patch("builtins.print")

    # Act
    linter.main()

    # Assert
    mock_subprocess.assert_has_calls(
        [
            mocker.call(["poetry", "run", "formatter"], check=True),
            mocker.call(["poetry", "run", "mypy", "./scripts"], check=True),
            mocker.call(["poetry", "run", "pylint", "./scripts"], check=True),
            mocker.call(["poetry", "run", "mypy", "./tests"], check=True),
            mocker.call(["poetry", "run", "pylint", "./tests"], check=True),
        ],
        any_order=False,
    )
    mock_print.assert_has_calls(
        [
            mocker.call("Linting ./scripts with mypy..."),
            mocker.call("mypy linting done."),
            mocker.call("Linting ./scripts with pylint..."),
            mocker.call("pylint linting done."),
            mocker.call("Linting ./tests with mypy..."),
            mocker.call("mypy linting done."),
            mocker.call("Linting ./tests with pylint..."),
            mocker.call("pylint linting done."),
            mocker.call("All linting complete."),
        ],
        any_order=False,
    )
