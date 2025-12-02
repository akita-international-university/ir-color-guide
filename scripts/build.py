"""
Script to convert palettes.yml into Tableau Preferences.tps and R script files.
"""

import os
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

    return data.get("palettes", [])


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
        description = palette.get("description", "")
        colors = palette.get("colors", [])

        tableau_type = get_tableau_type(palette_type)

        # Add color-palette element
        lines.append(f'    <color-palette name="{name}" type="{tableau_type}">')

        # Add description as comment
        if description:
            lines.append(f"      <!-- {description} -->")

        # Add colors with keys as comments
        for color in colors:
            key = color.get("key", "")
            value = color.get("value", "")
            if key:
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
    # Convert to lowercase and replace spaces with underscores
    sanitized = name.lower().replace(" ", "_")
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


def generate_r_script(palettes: List[Dict[str, Any]], output_path: str):
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
        description = palette.get("description", "")
        colors = palette.get("colors", [])

        variable_name = f"color_values_{sanitize_variable_name(name)}"

        lines.append(f"{variable_name} <- c(")
        lines.append(f"    # Type: {format_r_type(palette_type)}")
        lines.append(f"    # Description: {description}")

        # Add color entries
        for i, color in enumerate(colors):
            key = color.get("key", "")
            value = color.get("value", "")
            # Last item should not have a comma
            comma = "," if i < len(colors) - 1 else ""
            lines.append(f'    "{key}" = "{value}"{comma}')

        lines.append(")")
        lines.append("")  # Add blank line between palettes

    # Write to file
    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(lines))


def run_prettier(file_path: str):
    """
    Run Prettier on the specified file.

    Note:
        This function requires Node.js and npm to be installed and available in PATH.
        Prettier is run via npx, which should be available with npm 5.2+.

    Args:
        file_path: Path to the file to format

    Raises:
        subprocess.CalledProcessError: If Prettier fails to run
        FileNotFoundError: If npx/prettier is not installed
    """
    print(f"Running Prettier on {file_path}...")
    # Convert to absolute path for cross-platform compatibility
    # This ensures the path is properly resolved on Windows
    abs_file_path = os.path.abspath(file_path)
    try:
        subprocess.run(
            ["npx", "prettier", abs_file_path, "--write"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Prettier failed for {file_path}.\nError output:\n{e.stderr}")
        raise
    print(f"Prettier formatting done for {file_path}.")


def main():
    """
    Main function to convert palettes.yml to Tableau and R files.
    """
    # Define file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    yaml_path = os.path.join(repo_root, "palettes.yml")
    tableau_path = os.path.join(repo_root, "tableau", "Preferences.tps")
    r_script_path = os.path.join(repo_root, "r_script", "ir_color_palettes.R")

    # Load palettes
    print(f"Loading palettes from {yaml_path}...")
    palettes = load_palettes(yaml_path)
    print(f"Loaded {len(palettes)} palette(s).")

    # Ensure output directories exist
    os.makedirs(os.path.dirname(tableau_path), exist_ok=True)
    os.makedirs(os.path.dirname(r_script_path), exist_ok=True)

    # Generate Tableau Preferences file
    print(f"Generating Tableau Preferences file at {tableau_path}...")
    generate_tableau_preferences(palettes, tableau_path)
    print("Tableau Preferences file generated.")

    # Run Prettier on Tableau file
    run_prettier(tableau_path)

    # Generate R script file
    print(f"Generating R script file at {r_script_path}...")
    generate_r_script(palettes, r_script_path)
    print("R script file generated.")

    print("All files generated successfully.")


if __name__ == "__main__":
    main()
