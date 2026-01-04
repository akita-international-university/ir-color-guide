"""
Unit tests for ./scripts/build.py
"""

import os
import subprocess
import tempfile
from typing import Any, Dict, List
from unittest.mock import mock_open

import pytest
import yaml

from scripts import build


# Test data fixtures
@pytest.fixture
def sample_palettes() -> List[Dict[str, Any]]:
    """Sample palettes for testing."""
    return [
        {
            "name": "Test Palette",
            "type": "categorical",
            "description": "A test palette",
            "colors": [
                {"key": "Color One", "value": "#ff0000"},
                {"key": "Color Two", "value": "#00ff00"},
            ],
        },
        {
            "name": "Sequential Test",
            "type": "sequential",
            "description": "A sequential palette",
            "colors": [
                {"key": "Light", "value": "#e0e0e0"},
                {"key": "Dark", "value": "#202020"},
            ],
        },
    ]


@pytest.fixture
def sample_yaml_data() -> Dict[str, Any]:
    """Sample YAML data structure."""
    return {
        "organization": {
            "name": "Test Organization",
            "email": "test@example.com",
        },
        "palettes": [
            {
                "name": "Test Palette",
                "type": "categorical",
                "description": "A test palette",
                "colors": [
                    {"key": "Color One", "value": "#ff0000"},
                    {"key": "Color Two", "value": "#00ff00"},
                ],
            }
        ],
    }


# Tests for load_palettes()
def test_load_palettes_success(
    mocker, sample_yaml_data
):  # pylint: disable=redefined-outer-name
    """Test successful loading of palettes from YAML file."""
    # Arrange
    mock_file = mock_open(read_data=yaml.dump(sample_yaml_data))
    mocker.patch("builtins.open", mock_file)

    # Act
    result = build.load_palettes("test.yml")

    # Assert
    assert len(result) == 1
    assert result[0]["name"] == "Test Palette"
    assert result[0]["type"] == "categorical"
    mock_file.assert_called_once_with("test.yml", "r", encoding="utf-8")


def test_load_palettes_file_not_found(mocker):
    """Test FileNotFoundError when YAML file doesn't exist."""
    # Arrange
    mocker.patch("builtins.open", side_effect=FileNotFoundError("File not found"))

    # Act & Assert
    with pytest.raises(FileNotFoundError, match="YAML file not found"):
        build.load_palettes("nonexistent.yml")


def test_load_palettes_yaml_error(mocker):
    """Test yaml.YAMLError when YAML file is malformed."""
    # Arrange
    mock_file = mock_open(read_data="invalid: yaml: content: [")
    mocker.patch("builtins.open", mock_file)

    # Act & Assert
    with pytest.raises(yaml.YAMLError, match="Error parsing YAML file"):
        build.load_palettes("malformed.yml")


def test_load_palettes_missing_palettes_key(mocker):
    """Test ValueError when 'palettes' key is missing."""
    # Arrange
    invalid_data = {"organization": {"name": "Test"}}
    mock_file = mock_open(read_data=yaml.dump(invalid_data))
    mocker.patch("builtins.open", mock_file)

    # Act & Assert
    with pytest.raises(ValueError, match="YAML file must contain 'palettes' key"):
        build.load_palettes("invalid.yml")


def test_load_palettes_empty_file(mocker):
    """Test ValueError when YAML file is empty."""
    # Arrange
    mock_file = mock_open(read_data="")
    mocker.patch("builtins.open", mock_file)

    # Act & Assert
    with pytest.raises(ValueError, match="YAML file must contain 'palettes' key"):
        build.load_palettes("empty.yml")


# Tests for get_tableau_type()
def test_get_tableau_type_categorical():
    """Test conversion of 'categorical' type."""
    assert build.get_tableau_type("categorical") == "regular"


def test_get_tableau_type_sequential():
    """Test conversion of 'sequential' type."""
    assert build.get_tableau_type("sequential") == "ordered-sequential"


def test_get_tableau_type_diverging():
    """Test conversion of 'diverging' type."""
    assert build.get_tableau_type("diverging") == "ordered-diverging"


def test_get_tableau_type_unknown():
    """Test default behavior for unknown type."""
    assert build.get_tableau_type("unknown_type") == "regular"


# Tests for generate_tableau_preferences()
def test_generate_tableau_preferences_creates_file(
    mocker, sample_palettes
):  # pylint: disable=redefined-outer-name
    """Test that generate_tableau_preferences creates a file."""
    # Arrange
    mock_file = mock_open()
    mocker.patch("builtins.open", mock_file)

    # Act
    build.generate_tableau_preferences(sample_palettes, "output.tps")

    # Assert
    mock_file.assert_called_once_with("output.tps", "w", encoding="utf-8", newline="\n")
    handle = mock_file()
    # Verify write was called
    assert handle.write.called


def test_generate_tableau_preferences_content(
    sample_palettes,
):  # pylint: disable=redefined-outer-name
    """Test the content of generated Tableau preferences file."""
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tps") as tmp:
        tmp_path = tmp.name

    try:
        # Act
        build.generate_tableau_preferences(sample_palettes, tmp_path)

        # Assert
        with open(tmp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check XML structure
        assert "<?xml version='1.0'?>" in content
        assert "<workbook>" in content
        assert "<preferences>" in content
        assert "</preferences>" in content
        assert "</workbook>" in content

        # Check palette names and types
        assert 'name="Test Palette"' in content
        assert 'type="regular"' in content
        assert 'name="Sequential Test"' in content
        assert 'type="ordered-sequential"' in content

        # Check colors
        assert "<color>#ff0000</color>" in content
        assert "<color>#00ff00</color>" in content
        assert "<!-- Color One -->" in content
        assert "<!-- Color Two -->" in content

        # Check description
        assert "<!-- A test palette -->" in content

    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_generate_tableau_preferences_empty_palettes():
    """Test generation with empty palette list."""
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tps") as tmp:
        tmp_path = tmp.name

    try:
        # Act
        build.generate_tableau_preferences([], tmp_path)

        # Assert
        with open(tmp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Should still have basic XML structure
        assert "<?xml version='1.0'?>" in content
        assert "<workbook>" in content
        assert "<preferences>" in content
        assert "</preferences>" in content
        assert "</workbook>" in content

    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# Tests for sanitize_variable_name()
def test_sanitize_variable_name_basic():
    """Test basic conversion to snake_case."""
    assert build.sanitize_variable_name("Test Palette") == "test_palette"


def test_sanitize_variable_name_with_special_chars():
    """Test removal of special characters."""
    assert build.sanitize_variable_name("Test-Palette!@#$") == "testpalette"


def test_sanitize_variable_name_multiple_spaces():
    """Test multiple spaces converted to underscores."""
    assert (
        build.sanitize_variable_name("Test  Multiple   Spaces")
        == "test__multiple___spaces"
    )


def test_sanitize_variable_name_numbers():
    """Test that numbers are preserved."""
    assert build.sanitize_variable_name("Test 123 Palette") == "test_123_palette"


def test_sanitize_variable_name_already_snake_case():
    """Test that already snake_case names are preserved."""
    assert build.sanitize_variable_name("test_palette") == "test_palette"


def test_sanitize_variable_name_mixed_case():
    """Test mixed case conversion."""
    assert build.sanitize_variable_name("TestPalette") == "testpalette"


# Tests for format_r_type()
def test_format_r_type_categorical():
    """Test formatting of 'categorical' type."""
    assert build.format_r_type("categorical") == "Categorical"


def test_format_r_type_sequential():
    """Test formatting of 'sequential' type."""
    assert build.format_r_type("sequential") == "Sequential"


def test_format_r_type_diverging():
    """Test formatting of 'diverging' type."""
    assert build.format_r_type("diverging") == "Diverging"


def test_format_r_type_lowercase():
    """Test that lowercase input is capitalized."""
    assert build.format_r_type("lowercase") == "Lowercase"


# Tests for generate_r_script()
def test_generate_r_script_creates_file(
    mocker, sample_palettes
):  # pylint: disable=redefined-outer-name
    """Test that generate_r_script creates a file."""
    # Arrange
    mock_file = mock_open()
    mocker.patch("builtins.open", mock_file)

    # Act
    build.generate_r_script(sample_palettes, "output.R")

    # Assert
    mock_file.assert_called_once_with("output.R", "w", encoding="utf-8", newline="\n")
    handle = mock_file()
    assert handle.write.called


def test_generate_r_script_content(
    sample_palettes,
):  # pylint: disable=redefined-outer-name
    """Test the content of generated R script file."""
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".R") as tmp:
        tmp_path = tmp.name

    try:
        # Act
        build.generate_r_script(sample_palettes, tmp_path)

        # Assert
        with open(tmp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check header comments
        assert (
            "# Color palettes based on the IR Data Visualization Color Guidelines"
            in content
        )
        assert "# This file is created automatically. Do NOT edit manually." in content

        # Check variable names
        assert "color_values_test_palette <- c(" in content
        assert "color_values_sequential_test <- c(" in content

        # Check type comments
        assert "# Type: Categorical" in content
        assert "# Type: Sequential" in content

        # Check descriptions
        assert "# Description: A test palette" in content
        assert "# Description: A sequential palette" in content

        # Check color entries
        assert '"Color One" = "#ff0000",' in content
        assert '"Color Two" = "#00ff00"' in content
        assert '"Light" = "#e0e0e0",' in content
        assert '"Dark" = "#202020"' in content

    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_generate_r_script_empty_palettes():
    """Test generation with empty palette list."""
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".R") as tmp:
        tmp_path = tmp.name

    try:
        # Act
        build.generate_r_script([], tmp_path)

        # Assert
        with open(tmp_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Should have header comments
        assert (
            "# Color palettes based on the IR Data Visualization Color Guidelines"
            in content
        )
        assert "# This file is created automatically. Do NOT edit manually." in content

    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# Tests for run_prettier()
def test_run_prettier_success(mocker):
    """Test successful execution of Prettier."""
    # Arrange
    mock_subprocess = mocker.patch("subprocess.run")
    mock_print = mocker.patch("builtins.print")

    # Act
    build.run_prettier("test.tps")

    # Assert
    mock_subprocess.assert_called_once_with(
        ["npx", "prettier", "test.tps", "--write"],
        check=True,
        capture_output=True,
        text=True,
        shell=True,
    )
    mock_print.assert_any_call("Running Prettier on test.tps...")
    mock_print.assert_any_call("Prettier formatting done for test.tps.")


def test_run_prettier_failure(mocker):
    """Test handling of Prettier failure."""
    # Arrange
    mock_error = subprocess.CalledProcessError(1, "npx")
    mock_error.stderr = "Prettier error message"
    mock_subprocess = mocker.patch("subprocess.run", side_effect=mock_error)
    mock_print = mocker.patch("builtins.print")

    # Act & Assert
    with pytest.raises(subprocess.CalledProcessError):
        build.run_prettier("test.tps")

    mock_subprocess.assert_called_once()
    mock_print.assert_any_call("Running Prettier on test.tps...")
    mock_print.assert_any_call(
        "Prettier failed for test.tps.\nError output:\nPrettier error message"
    )


# Tests for main()
def test_main_success(mocker, sample_yaml_data):  # pylint: disable=redefined-outer-name
    """Test successful execution of main function."""
    # Arrange
    mock_load_palettes = mocker.patch(
        "scripts.build.load_palettes", return_value=sample_yaml_data["palettes"]
    )
    mock_generate_tableau = mocker.patch("scripts.build.generate_tableau_preferences")
    mock_generate_r = mocker.patch("scripts.build.generate_r_script")
    mock_run_prettier = mocker.patch("scripts.build.run_prettier")
    mock_makedirs = mocker.patch("os.makedirs")
    mock_print = mocker.patch("builtins.print")

    # Mock os.path functions
    mocker.patch("os.path.dirname", return_value="/fake/path")
    mocker.patch("os.path.abspath", return_value="/fake/path/scripts/build.py")

    # Act
    build.main()

    # Assert
    mock_load_palettes.assert_called_once()
    mock_generate_tableau.assert_called_once()
    mock_generate_r.assert_called_once()
    mock_run_prettier.assert_called_once()
    assert mock_makedirs.call_count == 2  # For both tableau and r_script directories

    # Verify print statements
    expected_prints = [
        mocker.call("Loading palettes from /fake/path/palettes.yml..."),
        mocker.call("Loaded 1 palette(s)."),
        mocker.call(
            "Generating Tableau Preferences file at /fake/path/tableau/Preferences.tps..."
        ),
        mocker.call("Tableau Preferences file generated."),
        mocker.call(
            "Generating R script file at /fake/path/r_script/ir_color_palettes.R..."
        ),
        mocker.call("R script file generated."),
        mocker.call("All files generated successfully."),
    ]
    mock_print.assert_has_calls(expected_prints)


def test_main_creates_directories(
    mocker, sample_yaml_data
):  # pylint: disable=redefined-outer-name
    """Test that main function creates necessary directories."""
    # Arrange
    mocker.patch(
        "scripts.build.load_palettes", return_value=sample_yaml_data["palettes"]
    )
    mocker.patch("scripts.build.generate_tableau_preferences")
    mocker.patch("scripts.build.generate_r_script")
    mocker.patch("scripts.build.run_prettier")
    mock_makedirs = mocker.patch("os.makedirs")
    mocker.patch("builtins.print")

    # Mock os.path functions
    mocker.patch("os.path.dirname", return_value="/fake/path")
    mocker.patch("os.path.abspath", return_value="/fake/path/scripts/build.py")

    # Act
    build.main()

    # Assert
    assert mock_makedirs.call_count == 2
    # Check that makedirs was called with exist_ok=True
    for call in mock_makedirs.call_args_list:
        assert call[1]["exist_ok"] is True


def test_main_handles_load_error(mocker):
    """Test that main function properly propagates load_palettes errors."""
    # Arrange
    mocker.patch(
        "scripts.build.load_palettes", side_effect=FileNotFoundError("File not found")
    )
    mocker.patch("os.path.dirname", return_value="/fake/path")
    mocker.patch("os.path.abspath", return_value="/fake/path/scripts/build.py")
    mocker.patch("builtins.print")

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        build.main()
