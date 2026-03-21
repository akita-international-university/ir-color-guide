"""
Script to convert palettes.yml into Tableau Preferences.tps, R script files, and
Exploratory palette JSON files.
"""

import json
import os
import re
import subprocess
from typing import Any, Dict, List

import yaml


def load_palettes(yaml_path: str) -> List[Dict[str, Any]]:
    """
    Load palettes from the YAML file.

    Args:
        yaml_path: Path to the palettes.yml file

    Returns:
        List of palette dictionaries

    Raises:
        FileNotFoundError: If the YAML file doesn't exist
        yaml.YAMLError: If the YAML file is malformed
    """
    try:
        with open(yaml_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"YAML file not found: {yaml_path}") from e
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {yaml_path}") from e

    if not data or "palettes" not in data:
        raise ValueError("YAML file must contain 'palettes' key")

    palettes = data.get("palettes", [])
    validate_palettes(palettes)
    return palettes


def validate_string_field(
    field_value: str | None, field_name: str, allow_empty: bool = False
) -> None:
    """
    Validate a string field for disallowed characters.

    Args:
        field_value: The string value to validate
        field_name: Name of the field for error messages
        allow_empty: Whether to allow empty strings

    Raises:
        ValueError: If the field contains disallowed characters or is empty when not allowed
    """
    if not allow_empty and (field_value is None or field_value == ""):
        raise ValueError(f"{field_name} must not be empty")

    if field_value:
        # Check for double quotes
        if '"' in field_value:
            raise ValueError(
                f'{field_name} contains disallowed character: " (double quote)'
            )

        # Check for < and >
        if "<" in field_value or ">" in field_value:
            raise ValueError(f"{field_name} contains disallowed characters: < or >")


def validate_color_value(
    color_value: str | None, palette_name: str, color_key: str
) -> None:
    """
    Validate a color value matches the required hex format.

    Args:
        color_value: The color value to validate
        palette_name: Name of the palette for error messages
        color_key: Key of the color for error messages

    Raises:
        ValueError: If the color value doesn't match the required format
    """
    if not color_value:
        raise ValueError(
            f"Color value for key '{color_key}' in palette '{palette_name}' must not be empty"
        )

    # Color value must match: ^#[a-f0-9]{6}$
    color_pattern = re.compile(r"^#[a-f0-9]{6}$")
    if not color_pattern.match(color_value):
        raise ValueError(
            f"Color value '{color_value}' for key '{color_key}' in palette '{palette_name}' "
            f"must be a hex color code (e.g., #ff00aa) with lowercase letters"
        )


def validate_palettes(  # pylint: disable=too-many-locals,too-many-branches
    palettes: List[Dict[str, Any]],
) -> None:
    """
    Validate all palettes for security and correctness.

    Args:
        palettes: List of palette dictionaries

    Raises:
        ValueError: If any validation fails
    """
    palette_names = []

    for palette in palettes:
        # Validate palette name
        name = palette.get("name", "")
        validate_string_field(name, "Palette name", allow_empty=False)

        # Check for duplicate palette names
        if name in palette_names:
            raise ValueError(f"Duplicate palette name: '{name}'")
        palette_names.append(name)

        # Validate description
        description = palette.get("description", "")
        if description:
            validate_string_field(description, f"Description in palette '{name}'")

        # Validate credit
        credit = palette.get("credit", "")
        if credit:
            validate_string_field(credit, f"Credit in palette '{name}'")

        # Validate colors
        colors = palette.get("colors", [])
        if not colors:
            raise ValueError(f"Palette '{name}' must have at least one color")

        color_keys = []
        for color in colors:
            # Validate color key
            key = color.get("key", "")
            validate_string_field(
                key, f"Color key in palette '{name}'", allow_empty=False
            )

            # Check for duplicate keys within palette
            if key in color_keys:
                raise ValueError(f"Duplicate color key '{key}' in palette '{name}'")
            color_keys.append(key)

            # Validate color value
            value = color.get("value", "")
            validate_color_value(value, name, key)

        # Validate aliases if present
        aliases = palette.get("aliases", [])
        alias_names = []
        for alias in aliases:
            # Validate alias name
            alias_name = alias.get("name", "")
            validate_string_field(
                alias_name, f"Alias name in palette '{name}'", allow_empty=False
            )

            # Check for duplicate alias names within palette
            if alias_name in alias_names:
                raise ValueError(
                    f"Duplicate alias name '{alias_name}' in palette '{name}'"
                )
            alias_names.append(alias_name)

            # Validate alias keys
            alias_keys = alias.get("keys", [])
            if not alias_keys:
                raise ValueError(
                    f"Alias '{alias_name}' in palette '{name}' must have a non-empty 'keys' list"
                )

            # Check that alias keys length matches colors length
            if len(alias_keys) != len(colors):
                raise ValueError(
                    f"Alias '{alias_name}' in palette '{name}' has {len(alias_keys)} keys "
                    f"but palette has {len(colors)} colors"
                )

            # Validate each alias key string
            for i, alias_key in enumerate(alias_keys):
                if not alias_key:
                    raise ValueError(
                        f"Alias key at index {i} in alias '{alias_name}' "
                        f"of palette '{name}' must not be empty"
                    )
                validate_string_field(
                    alias_key,
                    f"Alias key '{alias_key}' in alias '{alias_name}' "
                    f"of palette '{name}'",
                )


def get_tableau_type(palette_type: str) -> str:
    """
    Convert palette type to Tableau type.

    Args:
        palette_type: Type from palettes.yml (categorical, sequential, diverging)

    Returns:
        Tableau type string (regular, ordered-sequential, ordered-diverging)
    """
    type_mapping = {
        "categorical": "regular",
        "sequential": "ordered-sequential",
        "diverging": "ordered-diverging",
    }
    return type_mapping.get(palette_type, "regular")


def generate_tableau_preferences(palettes: List[Dict[str, Any]], output_path: str):
    """
    Generate Tableau Preferences.tps file from palettes.

    Args:
        palettes: List of palette dictionaries
        output_path: Path to output Preferences.tps file
    """
    lines = ["<?xml version='1.0'?>", "<workbook>", "  <preferences>"]

    # Add header comments
    lines.extend(
        [
            "    <!-- Color palettes based on the IR Data Visualization Color Guidelines -->",
            "    <!-- This file is created automatically. Do NOT edit manually. -->",
            "    <!-- See: https://github.com/akita-international-university/ir-color-guide -->",
        ]
    )

    for palette in palettes:
        name = palette.get("name", "")
        palette_type = palette.get("type", "categorical")
        description = palette.get("description", "").strip()
        credit = palette.get("credit", "").strip()
        colors = palette.get("colors", [])

        tableau_type = get_tableau_type(palette_type)

        # Add color-palette element
        lines.append(f'    <color-palette name="{name}" type="{tableau_type}">')

        # Add description as comment
        if description:
            lines.append(f"      <!-- {description} -->")

        # Add credit as comment
        if credit:
            lines.append(f"      <!-- Credit: {credit} -->")

        # Add colors with keys as comments
        for color in colors:
            key = color.get("key", "")
            value = color.get("value", "")
            lines.append(f"      <!-- {key} -->")
            lines.append(f"      <color>{value}</color>")

        lines.append("    </color-palette>")

    lines.extend(["  </preferences>", "</workbook>"])

    # Write to file
    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(lines) + "\n")


def sanitize_variable_name(name: str) -> str:
    """
    Convert palette name to a valid R variable name.

    Args:
        name: Palette name

    Returns:
        Sanitized variable name in snake_case
    """
    # Convert to lowercase and replace spaces and hyphens with underscores
    sanitized = name.lower().replace(" ", "_").replace("-", "_")
    # Remove any characters that aren't alphanumeric or underscore
    sanitized = "".join(c for c in sanitized if c.isalnum() or c == "_")
    return sanitized


def format_r_type(palette_type: str) -> str:
    """
    Format palette type for R comments.

    Args:
        palette_type: Type from palettes.yml

    Returns:
        Capitalized type string
    """
    return palette_type.capitalize()


def generate_r_palette_definition(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    variable_name: str,
    palette_type: str,
    description: str,
    credit: str,
    keys: List[str],
    values: List[str],
    alias_of: str = "",
) -> List[str]:
    """
    Generate R code lines for a single palette definition.

    Args:
        variable_name: R variable name for the palette
        palette_type: Type of palette (categorical, sequential, diverging)
        description: Description of the palette
        credit: Credit information (optional)
        keys: List of color keys
        values: List of color values
        alias_of: Variable name of the original palette if this is an alias

    Returns:
        List of code lines for the palette definition
    """
    lines = []
    lines.append(f"{variable_name} <- c(")
    lines.append(f"    # Type: {format_r_type(palette_type)}")
    lines.append(f"    # Description: {description}")
    if credit:
        lines.append(f"    # Credit: {credit}")
    if alias_of:
        lines.append(f"    # Alias of {alias_of}")

    # Add color entries
    for i, (key, value) in enumerate(zip(keys, values)):
        # Last item should not have a comma
        comma = "," if i < len(keys) - 1 else ""
        lines.append(f'    "{key}" = "{value}"{comma}')

    lines.append(")")
    lines.append("")  # Add blank line after palette

    return lines


def generate_r_script(  # pylint: disable=too-many-locals
    palettes: List[Dict[str, Any]], output_path: str
):
    """
    Generate R script file from palettes.

    Args:
        palettes: List of palette dictionaries
        output_path: Path to output R script file
    """
    lines = [
        "# Color palettes based on the IR Data Visualization Color Guidelines",
        "# This file is created automatically. Do NOT edit manually.",
        "# See: https://github.com/akita-international-university/ir-color-guide",
        "",
    ]

    for palette in palettes:
        name = palette.get("name", "")
        palette_type = palette.get("type", "categorical")
        description = palette.get("description", "").strip()
        credit = palette.get("credit", "").strip()
        colors = palette.get("colors", [])

        variable_name = f"color_values_{sanitize_variable_name(name)}"

        # Get color keys and values
        keys = [color.get("key", "") for color in colors]
        values = [color.get("value", "") for color in colors]

        # Generate the main palette definition
        lines.extend(
            generate_r_palette_definition(
                variable_name, palette_type, description, credit, keys, values
            )
        )

        # Process aliases if they exist
        aliases = palette.get("aliases", [])
        for alias in aliases:
            alias_name = alias["name"]
            alias_keys = alias["keys"]

            # Generate alias variable name by appending the alias name
            alias_variable_name = (
                f"{variable_name}_{sanitize_variable_name(alias_name)}"
            )

            # Generate the alias palette definition
            lines.extend(
                generate_r_palette_definition(
                    alias_variable_name,
                    palette_type,
                    description,
                    credit,
                    alias_keys,
                    values,
                    alias_of=variable_name,
                )
            )

    # Write to file
    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(lines))


def hex_to_rgba(hex_color: str) -> str:
    """
    Convert a hex color code to an rgba string.

    Args:
        hex_color: Hex color code (e.g., '#ff0000')

    Returns:
        RGBA string (e.g., 'rgba(255,0,0,1)')
    """
    hex_stripped = hex_color.lstrip("#")
    r = int(hex_stripped[0:2], 16)
    g = int(hex_stripped[2:4], 16)
    b = int(hex_stripped[4:6], 16)
    return f"rgba({r},{g},{b},1)"


def generate_exploratory_palette(palette: Dict[str, Any], output_dir: str) -> None:
    """
    Generate an Exploratory JSON file for a single palette.

    Args:
        palette: Palette dictionary
        output_dir: Path to the output directory
    """
    name = palette.get("name", "")
    colors = palette.get("colors", [])

    sanitized = sanitize_variable_name(name)
    palette_id = f"aiu-ir-palette-{sanitized}"

    palette_data = {
        "displayName": name,
        "colors": [hex_to_rgba(color.get("value", "")) for color in colors],
        "textColors": [],
        "id": palette_id,
    }

    output_path = os.path.join(output_dir, f"{palette_id}.json")
    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        json.dump(palette_data, file, ensure_ascii=False, indent=4)
        file.write("\n")


def generate_exploratory_palettes(
    palettes: List[Dict[str, Any]], output_dir: str
) -> None:
    """
    Generate Exploratory JSON files for all palettes.

    Removes any existing 'aiu-ir-palette-*.json' files in output_dir before
    generating new ones, so stale files from renamed or removed palettes are
    not left behind.

    Args:
        palettes: List of palette dictionaries
        output_dir: Path to the output directory
    """
    # Remove stale generated files before regenerating
    for existing_file in os.listdir(output_dir):
        if existing_file.startswith("aiu-ir-palette-") and existing_file.endswith(
            ".json"
        ):
            os.remove(os.path.join(output_dir, existing_file))

    for palette in palettes:
        generate_exploratory_palette(palette, output_dir)


def main():
    """
    Main function to convert palettes.yml to Tableau, R, and Exploratory files.
    """
    # Define file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    yaml_path = os.path.join(repo_root, "palettes.yml")
    tableau_path = os.path.join(repo_root, "tableau", "Preferences.tps")
    r_script_path = os.path.join(repo_root, "r_script", "ir_color_palettes.R")
    exploratory_dir = os.path.join(repo_root, "exploratory")

    # Load palettes
    print(f"Loading palettes from {yaml_path}...")
    palettes = load_palettes(yaml_path)
    print(f"Loaded {len(palettes)} palette(s).")

    # Ensure output directories exist
    os.makedirs(os.path.dirname(tableau_path), exist_ok=True)
    os.makedirs(os.path.dirname(r_script_path), exist_ok=True)
    os.makedirs(exploratory_dir, exist_ok=True)

    # Generate Tableau Preferences file
    print(f"Generating Tableau Preferences file at {tableau_path}...")
    generate_tableau_preferences(palettes, tableau_path)
    print("Tableau Preferences file generated.")

    # Generate R script file
    print(f"Generating R script file at {r_script_path}...")
    generate_r_script(palettes, r_script_path)
    print("R script file generated.")

    # Generate Exploratory palette files
    print(f"Generating Exploratory palette files in {exploratory_dir}...")
    generate_exploratory_palettes(palettes, exploratory_dir)
    print("Exploratory palette files generated.")

    # Run formatters
    subprocess.run(["poetry", "run", "formatter"], check=True)

    print("All files generated successfully.")
