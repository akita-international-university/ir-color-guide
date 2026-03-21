"""
Unit tests for ./scripts/build.py
"""

# pylint: disable=too-many-lines

import json
import os
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
        {
            "name": "Empty Description Palette",
            "type": "sequential",
            "description": "",
            "colors": [
                {"key": "Start", "value": "#ffffff"},
                {"key": "End", "value": "#000000"},
            ],
        },
        {
            "name": "Palette with Credit",
            "type": "categorical",
            "description": "A palette with credit",
            "credit": "Derived from the ColorBrewer palette",
            "colors": [
                {"key": "First", "value": "#aaaaaa"},
                {"key": "Second", "value": "#bbbbbb"},
            ],
        },
        {
            "name": "Palette with Trailing Newlines",
            "type": "categorical",
            "description": "A palette with trailing newlines\n",
            "credit": "Credit with trailing newline\n",
            "colors": [
                {"key": "Color A", "value": "#cccccc"},
                {"key": "Color B", "value": "#dddddd"},
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


class TestLoadPalettes:
    """Tests for load_palettes() function."""

    def test_load_palettes_success(
        self, mocker, sample_yaml_data
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

    def test_load_palettes_file_not_found(self, mocker):
        """Test FileNotFoundError when YAML file doesn't exist."""
        # Arrange
        mocker.patch("builtins.open", side_effect=FileNotFoundError("File not found"))

        # Act & Assert
        with pytest.raises(FileNotFoundError, match="YAML file not found"):
            build.load_palettes("nonexistent.yml")

    def test_load_palettes_yaml_error(self, mocker):
        """Test yaml.YAMLError when YAML file is malformed."""
        # Arrange
        mock_file = mock_open(read_data="invalid: yaml: content: [")
        mocker.patch("builtins.open", mock_file)

        # Act & Assert
        with pytest.raises(yaml.YAMLError, match="Error parsing YAML file"):
            build.load_palettes("malformed.yml")

    def test_load_palettes_missing_palettes_key(self, mocker):
        """Test ValueError when 'palettes' key is missing."""
        # Arrange
        invalid_data = {"organization": {"name": "Test"}}
        mock_file = mock_open(read_data=yaml.dump(invalid_data))
        mocker.patch("builtins.open", mock_file)

        # Act & Assert
        with pytest.raises(ValueError, match="YAML file must contain 'palettes' key"):
            build.load_palettes("invalid.yml")

    def test_load_palettes_empty_file(self, mocker):
        """Test ValueError when YAML file is empty."""
        # Arrange
        mock_file = mock_open(read_data="")
        mocker.patch("builtins.open", mock_file)

        # Act & Assert
        with pytest.raises(ValueError, match="YAML file must contain 'palettes' key"):
            build.load_palettes("empty.yml")


class TestValidateStringField:
    """Tests for validate_string_field() function."""

    def test_validate_string_field_valid(self):
        """Test validation of valid strings."""
        # Should not raise any exception
        build.validate_string_field("Valid name", "Field")
        build.validate_string_field("Name with spaces", "Field")
        build.validate_string_field("Name-with-hyphens", "Field")
        build.validate_string_field("Name_with_underscores", "Field")
        build.validate_string_field("Name123", "Field")

    def test_validate_string_field_empty_not_allowed(self):
        """Test validation fails for empty string when not allowed."""
        with pytest.raises(ValueError, match="Field must not be empty"):
            build.validate_string_field("", "Field", allow_empty=False)

        with pytest.raises(ValueError, match="Field must not be empty"):
            build.validate_string_field(None, "Field", allow_empty=False)

    def test_validate_string_field_empty_allowed(self):
        """Test validation passes for empty string when allowed."""
        # Should not raise any exception
        build.validate_string_field("", "Field", allow_empty=True)
        build.validate_string_field(None, "Field", allow_empty=True)

    def test_validate_string_field_double_quote(self):
        """Test validation fails for double quotes."""
        with pytest.raises(
            ValueError,
            match='Field contains disallowed character: " \\(double quote\\)',
        ):
            build.validate_string_field('Name with "quotes"', "Field")

    def test_validate_string_field_angle_brackets(self):
        """Test validation fails for angle brackets."""
        with pytest.raises(
            ValueError, match="Field contains disallowed characters: < or >"
        ):
            build.validate_string_field("Name with <tag>", "Field")

        with pytest.raises(
            ValueError, match="Field contains disallowed characters: < or >"
        ):
            build.validate_string_field("Name with <", "Field")

        with pytest.raises(
            ValueError, match="Field contains disallowed characters: < or >"
        ):
            build.validate_string_field("Name with >", "Field")


class TestValidateColorValue:
    """Tests for validate_color_value() function."""

    def test_validate_color_value_valid(self):
        """Test validation of valid hex color codes."""
        # Should not raise any exception
        build.validate_color_value("#ff0000", "Test Palette", "Red")
        build.validate_color_value("#00ff00", "Test Palette", "Green")
        build.validate_color_value("#0000ff", "Test Palette", "Blue")
        build.validate_color_value("#abc123", "Test Palette", "Custom")
        build.validate_color_value("#000000", "Test Palette", "Black")
        build.validate_color_value("#ffffff", "Test Palette", "White")

    def test_validate_color_value_empty(self):
        """Test validation fails for empty color value."""
        with pytest.raises(
            ValueError,
            match="Color value for key 'Red' in palette 'Test' must not be empty",
        ):
            build.validate_color_value("", "Test", "Red")

        with pytest.raises(
            ValueError,
            match="Color value for key 'Red' in palette 'Test' must not be empty",
        ):
            build.validate_color_value(None, "Test", "Red")

    def test_validate_color_value_invalid_format(self):
        """Test validation fails for invalid hex color format."""
        # Missing #
        with pytest.raises(
            ValueError,
            match="Color value 'ff0000' for key 'Red' in palette 'Test' must be a hex color code",
        ):
            build.validate_color_value("ff0000", "Test", "Red")

        # Wrong length
        with pytest.raises(
            ValueError,
            match="Color value '#ff00' for key 'Red' in palette 'Test' must be a hex color code",
        ):
            build.validate_color_value("#ff00", "Test", "Red")

        with pytest.raises(
            ValueError,
            match="Color value '#ff000011' for key 'Red' in palette 'Test' "
            "must be a hex color code",
        ):
            build.validate_color_value("#ff000011", "Test", "Red")

        # Uppercase letters
        with pytest.raises(
            ValueError,
            match="Color value '#FF0000' for key 'Red' in palette 'Test' must be a hex color code",
        ):
            build.validate_color_value("#FF0000", "Test", "Red")

        # Invalid characters
        with pytest.raises(
            ValueError,
            match="Color value '#gggggg' for key 'Red' in palette 'Test' must be a hex color code",
        ):
            build.validate_color_value("#gggggg", "Test", "Red")


class TestValidatePalettes:
    """Tests for validate_palettes() function."""

    def test_validate_palettes_valid(self):
        """Test validation of valid palettes."""
        palettes = [
            {
                "name": "Test Palette",
                "type": "categorical",
                "description": "A test palette",
                "colors": [
                    {"key": "Color One", "value": "#ff0000"},
                    {"key": "Color Two", "value": "#00ff00"},
                ],
            }
        ]
        # Should not raise any exception
        build.validate_palettes(palettes)

    def test_validate_palettes_with_aliases(self):
        """Test validation of palettes with valid aliases."""
        palettes = [
            {
                "name": "Test Palette",
                "type": "categorical",
                "description": "A test palette",
                "colors": [
                    {"key": "Color One", "value": "#ff0000"},
                    {"key": "Color Two", "value": "#00ff00"},
                ],
                "aliases": [
                    {"name": "alias1", "keys": ["Alt One", "Alt Two"]},
                    {"name": "alias2", "keys": ["Other One", "Other Two"]},
                ],
            }
        ]
        # Should not raise any exception
        build.validate_palettes(palettes)

    def test_validate_palettes_empty_name(self):
        """Test validation fails for empty palette name."""
        palettes = [
            {
                "name": "",
                "type": "categorical",
                "colors": [{"key": "Color", "value": "#ff0000"}],
            }
        ]
        with pytest.raises(ValueError, match="Palette name must not be empty"):
            build.validate_palettes(palettes)

    def test_validate_palettes_duplicate_names(self):
        """Test validation fails for duplicate palette names."""
        palettes = [
            {
                "name": "Same Name",
                "type": "categorical",
                "colors": [{"key": "Color", "value": "#ff0000"}],
            },
            {
                "name": "Same Name",
                "type": "sequential",
                "colors": [{"key": "Color", "value": "#00ff00"}],
            },
        ]
        with pytest.raises(ValueError, match="Duplicate palette name: 'Same Name'"):
            build.validate_palettes(palettes)

    def test_validate_palettes_invalid_name_characters(self):
        """Test validation fails for invalid characters in palette name."""
        # Double quote
        palettes = [
            {
                "name": 'Name with "quote"',
                "type": "categorical",
                "colors": [{"key": "Color", "value": "#ff0000"}],
            }
        ]
        with pytest.raises(
            ValueError, match="Palette name contains disallowed character"
        ):
            build.validate_palettes(palettes)

        # Angle brackets
        palettes = [
            {
                "name": "Name with <tag>",
                "type": "categorical",
                "colors": [{"key": "Color", "value": "#ff0000"}],
            }
        ]
        with pytest.raises(
            ValueError, match="Palette name contains disallowed characters"
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_invalid_description(self):
        """Test validation fails for invalid characters in description."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "description": 'Description with "quote"',
                "colors": [{"key": "Color", "value": "#ff0000"}],
            }
        ]
        with pytest.raises(
            ValueError,
            match="Description in palette 'Test' contains disallowed character",
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_invalid_credit(self):
        """Test validation fails for invalid characters in credit."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "credit": "Credit with <tag>",
                "colors": [{"key": "Color", "value": "#ff0000"}],
            }
        ]
        with pytest.raises(
            ValueError, match="Credit in palette 'Test' contains disallowed characters"
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_no_colors(self):
        """Test validation fails for palette without colors."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [],
            }
        ]
        with pytest.raises(
            ValueError, match="Palette 'Test' must have at least one color"
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_empty_color_key(self):
        """Test validation fails for empty color key."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [{"key": "", "value": "#ff0000"}],
            }
        ]
        with pytest.raises(
            ValueError, match="Color key in palette 'Test' must not be empty"
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_duplicate_color_keys(self):
        """Test validation fails for duplicate color keys within a palette."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [
                    {"key": "Same Key", "value": "#ff0000"},
                    {"key": "Same Key", "value": "#00ff00"},
                ],
            }
        ]
        with pytest.raises(
            ValueError, match="Duplicate color key 'Same Key' in palette 'Test'"
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_invalid_color_key_characters(self):
        """Test validation fails for invalid characters in color key."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [{"key": 'Key with "quote"', "value": "#ff0000"}],
            }
        ]
        with pytest.raises(
            ValueError,
            match="Color key in palette 'Test' contains disallowed character",
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_empty_color_value(self):
        """Test validation fails for empty color value."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [{"key": "Red", "value": ""}],
            }
        ]
        with pytest.raises(
            ValueError,
            match="Color value for key 'Red' in palette 'Test' must not be empty",
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_invalid_color_value(self):
        """Test validation fails for invalid color value format."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [{"key": "Red", "value": "#FF0000"}],  # Uppercase
            }
        ]
        with pytest.raises(
            ValueError,
            match="Color value '#FF0000' for key 'Red' in palette 'Test' must be a hex color code",
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_empty_alias_name(self):
        """Test validation fails for empty alias name."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [{"key": "Color", "value": "#ff0000"}],
                "aliases": [{"name": "", "keys": ["Alt"]}],
            }
        ]
        with pytest.raises(
            ValueError, match="Alias name in palette 'Test' must not be empty"
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_duplicate_alias_names(self):
        """Test validation fails for duplicate alias names within a palette."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [{"key": "Color", "value": "#ff0000"}],
                "aliases": [
                    {"name": "same", "keys": ["Alt"]},
                    {"name": "same", "keys": ["Other"]},
                ],
            }
        ]
        with pytest.raises(
            ValueError, match="Duplicate alias name 'same' in palette 'Test'"
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_empty_alias_keys(self):
        """Test validation fails for empty alias keys list."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [{"key": "Color", "value": "#ff0000"}],
                "aliases": [{"name": "alias1", "keys": []}],
            }
        ]
        with pytest.raises(
            ValueError,
            match="Alias 'alias1' in palette 'Test' must have a non-empty 'keys' list",
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_alias_keys_length_mismatch(self):
        """Test validation fails when alias keys length doesn't match colors length."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [
                    {"key": "Color One", "value": "#ff0000"},
                    {"key": "Color Two", "value": "#00ff00"},
                ],
                "aliases": [
                    {"name": "alias1", "keys": ["Only One"]},  # Should have 2 keys
                ],
            }
        ]
        with pytest.raises(
            ValueError,
            match="Alias 'alias1' in palette 'Test' has 1 keys but palette has 2 colors",
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_empty_alias_key_string(self):
        """Test validation fails for empty string in alias keys."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [
                    {"key": "Color One", "value": "#ff0000"},
                    {"key": "Color Two", "value": "#00ff00"},
                ],
                "aliases": [
                    {"name": "alias1", "keys": ["Valid", ""]},
                ],
            }
        ]
        with pytest.raises(
            ValueError,
            match="Alias key at index 1 in alias 'alias1' of palette 'Test' must not be empty",
        ):
            build.validate_palettes(palettes)

    def test_validate_palettes_invalid_alias_key_characters(self):
        """Test validation fails for invalid characters in alias keys."""
        palettes = [
            {
                "name": "Test",
                "type": "categorical",
                "colors": [{"key": "Color", "value": "#ff0000"}],
                "aliases": [
                    {"name": "alias1", "keys": ['Key with "quote"']},
                ],
            }
        ]
        with pytest.raises(
            ValueError,
            match="Alias key 'Key with \"quote\"' in alias 'alias1' "
            "of palette 'Test' contains disallowed character",
        ):
            build.validate_palettes(palettes)


class TestGetTableauType:
    """Tests for get_tableau_type() function."""

    def test_get_tableau_type_categorical(self):
        """Test conversion of 'categorical' type."""
        assert build.get_tableau_type("categorical") == "regular"

    def test_get_tableau_type_sequential(self):
        """Test conversion of 'sequential' type."""
        assert build.get_tableau_type("sequential") == "ordered-sequential"

    def test_get_tableau_type_diverging(self):
        """Test conversion of 'diverging' type."""
        assert build.get_tableau_type("diverging") == "ordered-diverging"

    def test_get_tableau_type_unknown(self):
        """Test default behavior for unknown type."""
        assert build.get_tableau_type("unknown_type") == "regular"


class TestGenerateTableauPreferences:
    """Tests for generate_tableau_preferences() function."""

    def test_generate_tableau_preferences_creates_file(
        self, mocker, sample_palettes
    ):  # pylint: disable=redefined-outer-name
        """Test that generate_tableau_preferences creates a file."""
        # Arrange
        mock_file = mock_open()
        mocker.patch("builtins.open", mock_file)

        # Act
        build.generate_tableau_preferences(sample_palettes, "output.tps")

        # Assert
        mock_file.assert_called_once_with(
            "output.tps", "w", encoding="utf-8", newline="\n"
        )
        handle = mock_file()
        # Verify write was called
        assert handle.write.called

    def test_generate_tableau_preferences_content(
        self, sample_palettes
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

    def test_generate_tableau_preferences_empty_palettes(self):
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

    def test_generate_tableau_preferences_with_credit(
        self, sample_palettes
    ):  # pylint: disable=redefined-outer-name
        """Test that credit attribute is included in Tableau preferences output."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tps") as tmp:
            tmp_path = tmp.name

        try:
            # Act
            build.generate_tableau_preferences(sample_palettes, tmp_path)

            # Assert
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check that credit comment is present for palette with credit
            assert "<!-- Credit: Derived from the ColorBrewer palette -->" in content

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_generate_tableau_preferences_without_credit(self):
        """Test that palettes without credit attribute work correctly."""
        # Arrange
        palettes_without_credit = [
            {
                "name": "No Credit Palette",
                "type": "categorical",
                "description": "A palette without credit",
                "colors": [
                    {"key": "Color A", "value": "#111111"},
                    {"key": "Color B", "value": "#222222"},
                ],
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tps") as tmp:
            tmp_path = tmp.name

        try:
            # Act
            build.generate_tableau_preferences(palettes_without_credit, tmp_path)

            # Assert
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check that no credit comment is present
            assert "<!-- Credit:" not in content
            # But description should still be present
            assert "<!-- A palette without credit -->" in content

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_generate_tableau_preferences_normalizes_trailing_newlines(
        self, sample_palettes
    ):  # pylint: disable=redefined-outer-name
        """Test that trailing newlines in description/credit are stripped."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tps") as tmp:
            tmp_path = tmp.name

        try:
            # Act
            build.generate_tableau_preferences(sample_palettes, tmp_path)

            # Assert
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check that description and credit are on single lines without split
            assert "<!-- A palette with trailing newlines -->" in content
            assert "<!-- Credit: Credit with trailing newline -->" in content

            # Verify comments are not split across multiple lines
            # (no standalone " -->" on next line)
            lines = content.split("\n")
            for line in lines:
                # If we find the credit comment, verify it's complete on one line
                if "Credit with trailing newline" in line:
                    assert line.strip().endswith("-->")

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestSanitizeVariableName:
    """Tests for sanitize_variable_name() function."""

    def test_sanitize_variable_name_basic(self):
        """Test basic conversion to snake_case."""
        assert build.sanitize_variable_name("Test Palette") == "test_palette"

    def test_sanitize_variable_name_with_hyphens_and_special_chars(self):
        """Test that hyphens are converted to underscores and special characters are removed."""
        assert build.sanitize_variable_name("Test-Palette!@#$") == "test_palette"

    def test_sanitize_variable_name_with_hyphens(self):
        """Test that hyphens are converted to underscores."""
        assert build.sanitize_variable_name("ja-short") == "ja_short"
        assert build.sanitize_variable_name("ja-full") == "ja_full"

    def test_sanitize_variable_name_multiple_spaces(self):
        """Test multiple spaces converted to underscores."""
        assert (
            build.sanitize_variable_name("Test  Multiple   Spaces")
            == "test__multiple___spaces"
        )

    def test_sanitize_variable_name_numbers(self):
        """Test that numbers are preserved."""
        assert build.sanitize_variable_name("Test 123 Palette") == "test_123_palette"

    def test_sanitize_variable_name_already_snake_case(self):
        """Test that already snake_case names are preserved."""
        assert build.sanitize_variable_name("test_palette") == "test_palette"

    def test_sanitize_variable_name_mixed_case(self):
        """Test mixed case conversion."""
        assert build.sanitize_variable_name("TestPalette") == "testpalette"


class TestFormatRType:
    """Tests for format_r_type() function."""

    def test_format_r_type_categorical(self):
        """Test formatting of 'categorical' type."""
        assert build.format_r_type("categorical") == "Categorical"

    def test_format_r_type_sequential(self):
        """Test formatting of 'sequential' type."""
        assert build.format_r_type("sequential") == "Sequential"

    def test_format_r_type_diverging(self):
        """Test formatting of 'diverging' type."""
        assert build.format_r_type("diverging") == "Diverging"

    def test_format_r_type_lowercase(self):
        """Test that lowercase input is capitalized."""
        assert build.format_r_type("lowercase") == "Lowercase"


class TestGenerateRPaletteDefinition:
    """Tests for generate_r_palette_definition() function."""

    def test_generate_r_palette_definition_basic(self):
        """Test basic palette definition generation."""
        # Arrange
        variable_name = "color_values_test"
        palette_type = "categorical"
        description = "Test palette"
        credit = ""
        keys = ["Red", "Green", "Blue"]
        values = ["#ff0000", "#00ff00", "#0000ff"]

        # Act
        result = build.generate_r_palette_definition(
            variable_name, palette_type, description, credit, keys, values
        )

        # Assert
        assert "color_values_test <- c(" in result
        assert "    # Type: Categorical" in result
        assert "    # Description: Test palette" in result
        assert '    "Red" = "#ff0000",' in result
        assert '    "Green" = "#00ff00",' in result
        assert '    "Blue" = "#0000ff"' in result  # No comma on last item
        assert ")" in result

    def test_generate_r_palette_definition_with_credit(self):
        """Test palette definition with credit."""
        # Arrange
        variable_name = "color_values_test"
        palette_type = "sequential"
        description = "Test palette"
        credit = "Test credit"
        keys = ["A", "B"]
        values = ["#111111", "#222222"]

        # Act
        result = build.generate_r_palette_definition(
            variable_name, palette_type, description, credit, keys, values
        )

        # Assert
        assert "    # Credit: Test credit" in result

    def test_generate_r_palette_definition_with_alias(self):
        """Test palette definition as an alias."""
        # Arrange
        variable_name = "color_values_test_ja"
        palette_type = "categorical"
        description = "Test palette"
        credit = ""
        keys = ["赤", "緑", "青"]
        values = ["#ff0000", "#00ff00", "#0000ff"]
        alias_of = "color_values_test"

        # Act
        result = build.generate_r_palette_definition(
            variable_name,
            palette_type,
            description,
            credit,
            keys,
            values,
            alias_of=alias_of,
        )

        # Assert
        assert "    # Alias of color_values_test" in result
        assert '    "赤" = "#ff0000",' in result
        assert '    "緑" = "#00ff00",' in result
        assert '    "青" = "#0000ff"' in result


class TestGenerateRScript:
    """Tests for generate_r_script() function."""

    def test_generate_r_script_creates_file(
        self, mocker, sample_palettes
    ):  # pylint: disable=redefined-outer-name
        """Test that generate_r_script creates a file."""
        # Arrange
        mock_file = mock_open()
        mocker.patch("builtins.open", mock_file)

        # Act
        build.generate_r_script(sample_palettes, "output.R")

        # Assert
        mock_file.assert_called_once_with(
            "output.R", "w", encoding="utf-8", newline="\n"
        )
        handle = mock_file()
        assert handle.write.called

    def test_generate_r_script_content(
        self, sample_palettes
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
            assert (
                "# This file is created automatically. Do NOT edit manually." in content
            )

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

    def test_generate_r_script_empty_palettes(self):
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
            assert (
                "# This file is created automatically. Do NOT edit manually." in content
            )

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_generate_r_script_with_credit(
        self, sample_palettes
    ):  # pylint: disable=redefined-outer-name
        """Test that credit attribute is included in R script output."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".R") as tmp:
            tmp_path = tmp.name

        try:
            # Act
            build.generate_r_script(sample_palettes, tmp_path)

            # Assert
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check that credit comment is present for palette with credit
            assert "# Credit: Derived from the ColorBrewer palette" in content

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_generate_r_script_without_credit(self):
        """Test that palettes without credit attribute work correctly."""
        # Arrange
        palettes_without_credit = [
            {
                "name": "No Credit Palette",
                "type": "categorical",
                "description": "A palette without credit",
                "colors": [
                    {"key": "Color A", "value": "#111111"},
                    {"key": "Color B", "value": "#222222"},
                ],
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".R") as tmp:
            tmp_path = tmp.name

        try:
            # Act
            build.generate_r_script(palettes_without_credit, tmp_path)

            # Assert
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check that no credit comment is present
            assert "# Credit:" not in content
            # But description should still be present
            assert "# Description: A palette without credit" in content

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_generate_r_script_normalizes_trailing_newlines(
        self, sample_palettes
    ):  # pylint: disable=redefined-outer-name
        """Test that trailing newlines in description/credit are stripped."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".R") as tmp:
            tmp_path = tmp.name

        try:
            # Act
            build.generate_r_script(sample_palettes, tmp_path)

            # Assert
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check that description and credit are on single lines without extra newlines
            assert "# Description: A palette with trailing newlines" in content
            assert "# Credit: Credit with trailing newline" in content

            # Verify no extra blank lines in the palette block
            # The pattern should be: description, credit, then color entries
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "A palette with trailing newlines" in line:
                    # Next line should be credit comment
                    assert "Credit with trailing newline" in lines[i + 1]
                    # Then should come color entries, not blank lines
                    assert lines[i + 2].strip() != ""

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_generate_r_script_with_aliases(self):
        """Test generation of R script with alias palettes."""
        # Arrange
        palettes_with_aliases = [
            {
                "name": "Test Palette",
                "type": "categorical",
                "description": "A test palette",
                "colors": [
                    {"key": "A", "value": "#ff0000"},
                    {"key": "B", "value": "#00ff00"},
                    {"key": "C", "value": "#0000ff"},
                ],
                "aliases": [
                    {"name": "ja", "keys": ["A日程", "B日程", "C日程"]},
                    {"name": "ja-short", "keys": ["あ", "い", "う"]},
                ],
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".R") as tmp:
            tmp_path = tmp.name

        try:
            # Act
            build.generate_r_script(palettes_with_aliases, tmp_path)

            # Assert
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check main palette
            assert "color_values_test_palette <- c(" in content
            assert '"A" = "#ff0000",' in content
            assert '"B" = "#00ff00",' in content
            assert '"C" = "#0000ff"' in content

            # Check first alias (ja)
            assert "color_values_test_palette_ja <- c(" in content
            assert "# Alias of color_values_test_palette" in content
            assert '"A日程" = "#ff0000",' in content
            assert '"B日程" = "#00ff00",' in content
            assert '"C日程" = "#0000ff"' in content

            # Check second alias (ja-short with hyphen converted to underscore)
            assert "color_values_test_palette_ja_short <- c(" in content
            assert '"あ" = "#ff0000",' in content
            assert '"い" = "#00ff00",' in content
            assert '"う" = "#0000ff"' in content

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_generate_r_script_with_aliases_preserves_order(self):
        """Test that aliases use the same color values in order."""
        # Arrange
        palettes_with_aliases = [
            {
                "name": "Order Test",
                "type": "categorical",
                "description": "Testing color order preservation",
                "colors": [
                    {"key": "First", "value": "#111111"},
                    {"key": "Second", "value": "#222222"},
                    {"key": "Third", "value": "#333333"},
                ],
                "aliases": [
                    {"name": "alias1", "keys": ["1st", "2nd", "3rd"]},
                ],
            }
        ]
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".R") as tmp:
            tmp_path = tmp.name

        try:
            # Act
            build.generate_r_script(palettes_with_aliases, tmp_path)

            # Assert
            with open(tmp_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Verify that the alias uses the same colors in the same order
            assert '"1st" = "#111111",' in content
            assert '"2nd" = "#222222",' in content
            assert '"3rd" = "#333333"' in content

        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestMain:
    """Tests for main() function."""

    def test_main_success(
        self, mocker, sample_yaml_data
    ):  # pylint: disable=redefined-outer-name
        """Test successful execution of main function."""
        # Arrange
        mock_load_palettes = mocker.patch(
            "scripts.build.load_palettes", return_value=sample_yaml_data["palettes"]
        )
        mock_generate_tableau = mocker.patch(
            "scripts.build.generate_tableau_preferences"
        )
        mock_generate_r = mocker.patch("scripts.build.generate_r_script")
        mock_generate_exploratory = mocker.patch(
            "scripts.build.generate_exploratory_palettes"
        )
        mock_subprocess = mocker.patch("subprocess.run")
        mock_makedirs = mocker.patch("os.makedirs")
        mock_print = mocker.patch("builtins.print")

        # Mock os.path functions
        mocker.patch("os.path.dirname", return_value=os.path.join("fake", "path"))
        mocker.patch(
            "os.path.abspath",
            return_value=os.path.join("fake", "path", "scripts", "build.py"),
        )

        # Act
        build.main()

        # Assert
        mock_load_palettes.assert_called_once()
        mock_generate_tableau.assert_called_once()
        mock_generate_r.assert_called_once()
        mock_generate_exploratory.assert_called_once()
        mock_subprocess.assert_has_calls(
            [mocker.call(["poetry", "run", "formatter"], check=True)], any_order=False
        )
        assert (  # For tableau, r_script, and exploratory directories
            mock_makedirs.call_count == 3
        )

        # Verify print statements
        expected_prints = [
            mocker.call(
                f"Loading palettes from {os.path.join('fake', 'path', 'palettes.yml')}..."
            ),
            mocker.call("Loaded 1 palette(s)."),
            mocker.call(
                "Generating Tableau Preferences file at"
                + f" {os.path.join('fake', 'path', 'tableau', 'Preferences.tps')}..."
            ),
            mocker.call("Tableau Preferences file generated."),
            mocker.call(
                "Generating R script file at"
                + f" {os.path.join('fake', 'path', 'r_script', 'ir_color_palettes.R')}..."
            ),
            mocker.call("R script file generated."),
            mocker.call(
                "Generating Exploratory palette files in"
                + f" {os.path.join('fake', 'path', 'exploratory')}..."
            ),
            mocker.call("Exploratory palette files generated."),
            mocker.call("All files generated successfully."),
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

    def test_main_creates_directories(
        self, mocker, sample_yaml_data
    ):  # pylint: disable=redefined-outer-name
        """Test that main function creates necessary directories."""
        # Arrange
        mocker.patch(
            "scripts.build.load_palettes", return_value=sample_yaml_data["palettes"]
        )
        mocker.patch("scripts.build.generate_tableau_preferences")
        mocker.patch("scripts.build.generate_r_script")
        mocker.patch("scripts.build.generate_exploratory_palettes")
        mocker.patch("subprocess.run")
        mock_makedirs = mocker.patch("os.makedirs")
        mocker.patch("builtins.print")

        # Mock os.path functions
        mocker.patch("os.path.dirname", return_value=os.path.join("fake", "path"))
        mocker.patch(
            "os.path.abspath",
            return_value=os.path.join("fake", "path", "scripts", "build.py"),
        )

        # Act
        build.main()

        # Assert
        assert mock_makedirs.call_count == 3
        # Check that makedirs was called with exist_ok=True
        for call in mock_makedirs.call_args_list:
            assert call[1]["exist_ok"] is True

    def test_main_handles_load_error(self, mocker):
        """Test that main function properly propagates load_palettes errors."""
        # Arrange
        mocker.patch(
            "scripts.build.load_palettes",
            side_effect=FileNotFoundError("File not found"),
        )
        mocker.patch("os.path.dirname", return_value=os.path.join("fake", "path"))
        mocker.patch(
            "os.path.abspath",
            return_value=os.path.join("fake", "path", "scripts", "build.py"),
        )
        mocker.patch("builtins.print")

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            build.main()


class TestHexToRgba:
    """Tests for hex_to_rgba() function."""

    def test_hex_to_rgba_red(self):
        """Test conversion of red hex color."""
        assert build.hex_to_rgba("#ff0000") == "rgba(255,0,0,1)"

    def test_hex_to_rgba_green(self):
        """Test conversion of green hex color."""
        assert build.hex_to_rgba("#00ff00") == "rgba(0,255,0,1)"

    def test_hex_to_rgba_blue(self):
        """Test conversion of blue hex color."""
        assert build.hex_to_rgba("#0000ff") == "rgba(0,0,255,1)"

    def test_hex_to_rgba_black(self):
        """Test conversion of black hex color."""
        assert build.hex_to_rgba("#000000") == "rgba(0,0,0,1)"

    def test_hex_to_rgba_white(self):
        """Test conversion of white hex color."""
        assert build.hex_to_rgba("#ffffff") == "rgba(255,255,255,1)"

    def test_hex_to_rgba_mixed(self):
        """Test conversion of a mixed hex color."""
        assert build.hex_to_rgba("#386325") == "rgba(56,99,37,1)"

    def test_hex_to_rgba_alpha_always_one(self):
        """Test that alpha value is always 1."""
        result = build.hex_to_rgba("#aabbcc")
        assert result.endswith(",1)")


class TestGenerateExploratoryPalette:
    """Tests for generate_exploratory_palette() function."""

    def test_generates_json_file(self):
        """Test that a JSON file is created for the palette."""
        palette = {
            "name": "Test Palette",
            "type": "categorical",
            "description": "A test palette",
            "colors": [
                {"key": "Color One", "value": "#ff0000"},
                {"key": "Color Two", "value": "#00ff00"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palette(palette, tmp_dir)
            expected_file = os.path.join(tmp_dir, "aiu-ir-palette-test_palette.json")
            assert os.path.exists(expected_file)

    def test_json_structure(self):
        """Test that the generated JSON has the expected structure."""
        palette = {
            "name": "Test Palette",
            "type": "categorical",
            "description": "A test palette",
            "colors": [
                {"key": "Color One", "value": "#ff0000"},
                {"key": "Color Two", "value": "#00ff00"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palette(palette, tmp_dir)
            file_path = os.path.join(tmp_dir, "aiu-ir-palette-test_palette.json")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert data["displayName"] == "Test Palette"
            assert data["colors"] == ["rgba(255,0,0,1)", "rgba(0,255,0,1)"]
            assert data["textColors"] == []
            assert data["id"] == "aiu-ir-palette-test_palette"

    def test_id_uses_sanitized_name(self):
        """Test that id uses the sanitized palette name."""
        palette = {
            "name": "My Test-Palette",
            "type": "categorical",
            "description": "",
            "colors": [{"key": "A", "value": "#aaaaaa"}],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palette(palette, tmp_dir)
            file_path = os.path.join(tmp_dir, "aiu-ir-palette-my_test_palette.json")
            assert os.path.exists(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert data["id"] == "aiu-ir-palette-my_test_palette"

    def test_colors_converted_to_rgba(self):
        """Test that hex colors are converted to rgba strings."""
        palette = {
            "name": "RGBA Test",
            "type": "categorical",
            "description": "",
            "colors": [
                {"key": "Dark Green", "value": "#386325"},
                {"key": "Light Green", "value": "#8dbb54"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palette(palette, tmp_dir)
            file_path = os.path.join(tmp_dir, "aiu-ir-palette-rgba_test.json")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert "rgba(56,99,37,1)" in data["colors"]
            assert "rgba(141,187,84,1)" in data["colors"]

    def test_display_name_is_original_palette_name(self):
        """Test that displayName is the original (non-sanitized) palette name."""
        palette = {
            "name": "AIU Exchange Region",
            "type": "categorical",
            "description": "",
            "colors": [{"key": "A", "value": "#aaaaaa"}],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palette(palette, tmp_dir)
            file_path = os.path.join(tmp_dir, "aiu-ir-palette-aiu_exchange_region.json")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert data["displayName"] == "AIU Exchange Region"

    def test_text_colors_is_empty_list(self):
        """Test that textColors is always an empty list."""
        palette = {
            "name": "Simple Palette",
            "type": "categorical",
            "description": "",
            "colors": [{"key": "A", "value": "#123456"}],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palette(palette, tmp_dir)
            file_path = os.path.join(tmp_dir, "aiu-ir-palette-simple_palette.json")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert data["textColors"] == []

    def test_json_file_ends_with_newline(self):
        """Test that the generated JSON file ends with a newline."""
        palette = {
            "name": "Newline Test",
            "type": "categorical",
            "description": "",
            "colors": [{"key": "A", "value": "#aabbcc"}],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palette(palette, tmp_dir)
            file_path = os.path.join(tmp_dir, "aiu-ir-palette-newline_test.json")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            assert content.endswith("\n")


class TestGenerateExploratoryPalettes:
    """Tests for generate_exploratory_palettes() function."""

    def test_generates_one_file_per_palette(self):
        """Test that one JSON file is created for each palette."""
        palettes = [
            {
                "name": "Palette A",
                "type": "categorical",
                "description": "",
                "colors": [{"key": "X", "value": "#111111"}],
            },
            {
                "name": "Palette B",
                "type": "sequential",
                "description": "",
                "colors": [{"key": "Y", "value": "#222222"}],
            },
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palettes(palettes, tmp_dir)
            files = os.listdir(tmp_dir)
            assert len(files) == 2
            assert "aiu-ir-palette-palette_a.json" in files
            assert "aiu-ir-palette-palette_b.json" in files

    def test_empty_palettes_list(self):
        """Test that no files are generated for an empty list."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palettes([], tmp_dir)
            assert os.listdir(tmp_dir) == []

    def test_each_file_has_correct_content(self):
        """Test that each generated file has the correct content."""
        palettes = [
            {
                "name": "Color Set",
                "type": "categorical",
                "description": "",
                "colors": [
                    {"key": "Red", "value": "#ff0000"},
                    {"key": "Blue", "value": "#0000ff"},
                ],
            }
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            build.generate_exploratory_palettes(palettes, tmp_dir)
            file_path = os.path.join(tmp_dir, "aiu-ir-palette-color_set.json")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert data["displayName"] == "Color Set"
            assert data["colors"] == ["rgba(255,0,0,1)", "rgba(0,0,255,1)"]
            assert data["textColors"] == []
            assert data["id"] == "aiu-ir-palette-color_set"

    def test_removes_stale_generated_files(self):
        """Test that stale aiu-ir-palette-*.json files are removed before regenerating."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create a stale file that would remain if not cleaned up
            stale_path = os.path.join(tmp_dir, "aiu-ir-palette-old_palette.json")
            with open(stale_path, "w", encoding="utf-8") as f:
                f.write("{}")

            # Run with a different palette
            palettes = [
                {
                    "name": "New Palette",
                    "type": "categorical",
                    "description": "",
                    "colors": [{"key": "A", "value": "#aaaaaa"}],
                }
            ]
            build.generate_exploratory_palettes(palettes, tmp_dir)

            files = os.listdir(tmp_dir)
            assert "aiu-ir-palette-old_palette.json" not in files
            assert "aiu-ir-palette-new_palette.json" in files

    def test_preserves_non_generated_files(self):
        """Test that non-generated files in the directory are not removed."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create a file that should not be removed
            other_path = os.path.join(tmp_dir, "README.md")
            with open(other_path, "w", encoding="utf-8") as f:
                f.write("# README")

            palettes = [
                {
                    "name": "My Palette",
                    "type": "categorical",
                    "description": "",
                    "colors": [{"key": "A", "value": "#111111"}],
                }
            ]
            build.generate_exploratory_palettes(palettes, tmp_dir)

            assert os.path.exists(other_path)
