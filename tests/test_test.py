"""
Unit tests for ./scripts/test.py
"""

from scripts import test


def test_main(mocker):
    """
    Test for the main function in test.py.
    """
    # Arrange
    mock_subprocess = mocker.patch("subprocess.run")

    # Act
    test.main()

    # Assert
    mock_subprocess.assert_has_calls(
        [
            mocker.call(["poetry", "run", "linter"], check=True),
            mocker.call(["poetry", "run", "pytest"], check=True),
        ]
    )
