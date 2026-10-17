"""
Script to check the palettes in palettes.yml against the quantitative criteria of the
AIU Design System (contrast, color vision deficiencies, number of colors, and lightness
steps), and to generate a Markdown report of the results.

Color vision deficiencies are simulated with the matrices of Machado, Oliveira &
Fernandes (2009) at severity 1.0, applied in linear RGB. Color differences are the
Euclidean distance in OKLab multiplied by 100. The thresholds below assume this
simulation method; revisit them if the method is changed.
"""

from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations
from math import atan2, cbrt, degrees, hypot
import os
import sys
from typing import Any, Dict, List, Sequence, Tuple

from scripts.build import load_palettes

Matrix = Tuple[
    Tuple[float, float, float],
    Tuple[float, float, float],
    Tuple[float, float, float],
]

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied in linear RGB
MACHADO: Dict[str, Matrix] = {
    "protan": (
        (0.152286, 1.052583, -0.204868),
        (0.114503, 0.786281, 0.099216),
        (-0.003882, -0.048116, 1.051998),
    ),
    "deutan": (
        (0.367322, 0.860646, -0.227968),
        (0.280085, 0.672501, 0.047413),
        (-0.011820, 0.042940, 0.968881),
    ),
}

# Background color the palettes are checked against
SURFACE = "#ffffff"

# Thresholds used by the AIU Design System
MARK_CONTRAST = 3.0
CVD_TARGET = 8.0
CVD_FLOOR = 6.0
NORMAL_FLOOR = 15.0
MAX_CATEGORICAL_COLORS = 8
ORDINAL_MIN_DELTA_L = 0.06
ORDINAL_LIGHT_END = 2.0

REPORT_HEADER = [
    "<!-- markdownlint-disable MD013 -->",
    "<!-- This file is created automatically by `poetry run validate`. "
    "Do NOT edit manually. -->",
    "",
    "# Palette Validation Report",
    "",
    "Results of checking each palette in [`palettes.yml`](../palettes.yml) against the "
    "[quantitative criteria](../README.md#quantitative-criteria) of the "
    "IR Data Visualization Color Guidelines.",
    "",
    f"- Background: `{SURFACE}`",
    "- Color vision deficiencies: protanopia and deuteranopia simulated with "
    "Machado et al. (2009), severity 1.0",
    "- Color difference: Euclidean distance in OKLab multiplied by 100",
    "- `FAIL` is treated as an error only for palettes marked "
    "`compliance: validated`; otherwise it is reported as a warning.",
    "",
]


class Level(IntEnum):
    """Result level of a check, ordered by severity."""

    PASS = 0
    WARN = 1
    FAIL = 2


@dataclass
class CheckResult:
    """Result of a single check on a palette."""

    name: str
    level: Level
    detail: str


@dataclass
class PaletteResult:
    """Results of all checks on a palette."""

    name: str
    palette_type: str
    compliance: str
    checks: List[CheckResult]
    keys: List[str]
    values: List[str]

    @property
    def level(self) -> Level:
        """The most severe level among the checks."""
        return max((check.level for check in self.checks), default=Level.PASS)

    @property
    def strict(self) -> bool:
        """Whether failures in this palette are treated as errors."""
        return self.compliance == "validated"


def _linear_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert a hex color code to linear RGB."""
    h = hex_color.lstrip("#")
    srgb = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = (
        v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in srgb
    )
    return r, g, b


def contrast(color_a: str, color_b: str = SURFACE) -> float:
    """
    Calculate the WCAG 2.x contrast ratio between two colors.

    Args:
        color_a: Hex color code
        color_b: Hex color code (defaults to the background color)

    Returns:
        Contrast ratio (1 to 21)
    """

    def luminance(hex_color: str) -> float:
        r, g, b = _linear_rgb(hex_color)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    high, low = sorted((luminance(color_a), luminance(color_b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def _oklab(rgb: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """Convert linear RGB to OKLab."""
    r, g, b = rgb
    l_ = cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m_ = cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s_ = cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def oklch(hex_color: str) -> Tuple[float, float, float]:
    """
    Convert a hex color code to OKLCH.

    Args:
        hex_color: Hex color code

    Returns:
        Tuple of lightness (0 to 1), chroma, and hue in degrees
    """
    lightness, a, b = _oklab(_linear_rgb(hex_color))
    return lightness, hypot(a, b), degrees(atan2(b, a)) % 360


def _simulate(hex_color: str, kind: str) -> Tuple[float, float, float]:
    """Simulate a color vision deficiency on a color, returning linear RGB."""
    rgb = _linear_rgb(hex_color)
    matrix = MACHADO[kind]
    out = [sum(matrix[i][j] * rgb[j] for j in range(3)) for i in range(3)]
    r, g, b = (min(1.0, max(0.0, v)) for v in out)
    return r, g, b


def delta_e(color_a: str, color_b: str, kind: str | None = None) -> float:
    """
    Calculate the Euclidean distance in OKLab multiplied by 100.

    Args:
        color_a: Hex color code
        color_b: Hex color code
        kind: Color vision deficiency to simulate ("protan" or "deutan"),
            or None for typical color vision

    Returns:
        Color difference
    """
    lab_a = _oklab(_simulate(color_a, kind) if kind else _linear_rgb(color_a))
    lab_b = _oklab(_simulate(color_b, kind) if kind else _linear_rgb(color_b))
    return 100 * hypot(lab_a[0] - lab_b[0], lab_a[1] - lab_b[1], lab_a[2] - lab_b[2])


def cvd_delta_e(color_a: str, color_b: str) -> float:
    """
    Calculate the smaller color difference under protanopia and deuteranopia.

    Args:
        color_a: Hex color code
        color_b: Hex color code

    Returns:
        Color difference under the worse of the two simulations
    """
    return min(delta_e(color_a, color_b, "protan"), delta_e(color_a, color_b, "deutan"))


def _format_pair(keys: Sequence[str], values: Sequence[str], i: int, j: int) -> str:
    return f"{keys[i]} (`{values[i]}`) / {keys[j]} (`{values[j]}`)"


def check_contrast(keys: Sequence[str], values: Sequence[str]) -> CheckResult:
    """
    List the colors with a contrast ratio below 3:1 against the background.

    Args:
        keys: Color keys
        values: Hex color codes

    Returns:
        WARN if any color is below the threshold (labels or a data table are required)
    """
    ratios = [contrast(value) for value in values]
    low = [
        f"{key} (`{value}`) {ratio:.2f}:1"
        for key, value, ratio in zip(keys, values, ratios)
        if ratio < MARK_CONTRAST
    ]
    if low:
        return CheckResult(
            "Contrast",
            Level.WARN,
            f"Below {MARK_CONTRAST:g}:1 (use labels or a data table): "
            + ", ".join(low),
        )
    return CheckResult("Contrast", Level.PASS, f"Minimum {min(ratios):.2f}:1")


def check_color_vision(keys: Sequence[str], values: Sequence[str]) -> CheckResult:
    """
    Check the color difference between adjacent colors under simulated
    protanopia and deuteranopia.

    Args:
        keys: Color keys
        values: Hex color codes

    Returns:
        PASS at or above the target, WARN between the floor and the target
        (supplementary cues required), FAIL below the floor
    """
    name = "Color vision deficiencies"
    if len(values) < 2:
        return CheckResult(name, Level.PASS, "Only one color")
    distances = [cvd_delta_e(a, b) for a, b in zip(values, values[1:])]
    worst = min(range(len(distances)), key=lambda i: distances[i])
    all_pairs = min(cvd_delta_e(a, b) for a, b in combinations(values, 2))
    detail = (
        f"Adjacent minimum {distances[worst]:.1f} at "
        f"{_format_pair(keys, values, worst, worst + 1)}; "
        f"all pairs minimum {all_pairs:.1f} (reference)"
    )
    if distances[worst] < CVD_FLOOR:
        return CheckResult(name, Level.FAIL, detail)
    if distances[worst] < CVD_TARGET:
        return CheckResult(name, Level.WARN, detail + "; supplementary cues required")
    return CheckResult(name, Level.PASS, detail)


def check_typical_vision(keys: Sequence[str], values: Sequence[str]) -> CheckResult:
    """
    Check the color difference between adjacent colors under typical color vision.

    Args:
        keys: Color keys
        values: Hex color codes

    Returns:
        FAIL if the minimum is below the threshold
    """
    name = "Typical color vision"
    if len(values) < 2:
        return CheckResult(name, Level.PASS, "Only one color")
    distances = [delta_e(a, b) for a, b in zip(values, values[1:])]
    worst = min(range(len(distances)), key=lambda i: distances[i])
    detail = (
        f"Adjacent minimum {distances[worst]:.1f} at "
        f"{_format_pair(keys, values, worst, worst + 1)}"
    )
    level = Level.FAIL if distances[worst] < NORMAL_FLOOR else Level.PASS
    return CheckResult(name, level, detail)


def check_color_count(values: Sequence[str]) -> CheckResult:
    """
    Check the number of colors in a categorical palette.

    Args:
        values: Hex color codes

    Returns:
        WARN if the palette has more colors than the maximum
    """
    name = "Number of colors"
    if len(values) > MAX_CATEGORICAL_COLORS:
        return CheckResult(
            name,
            Level.WARN,
            f"{len(values)} colors; group the categories after the "
            f"{MAX_CATEGORICAL_COLORS}th into 'Other'",
        )
    return CheckResult(name, Level.PASS, f"{len(values)} colors")


def _check_steps(values: Sequence[str], require_darkening: bool) -> List[str]:
    """
    Return the problems found in a series of lightness steps.

    Args:
        values: Hex color codes in order
        require_darkening: Whether the steps must get darker in order;
            otherwise either direction is accepted

    Returns:
        List of problems (empty if none)
    """
    lightness = [oklch(value)[0] for value in values]
    steps = [a - b for a, b in zip(lightness, lightness[1:])]
    problems: List[str] = []
    darkening = all(step > 0 for step in steps)
    lightening = all(step < 0 for step in steps)
    if not (darkening or (lightening and not require_darkening)):
        problems.append("lightness is not monotone")
    elif steps and min(abs(step) for step in steps) < ORDINAL_MIN_DELTA_L:
        problems.append(
            f"adjacent lightness difference {min(abs(s) for s in steps):.3f} "
            f"is below {ORDINAL_MIN_DELTA_L}"
        )
    lightest = values[lightness.index(max(lightness))]
    if contrast(lightest) < ORDINAL_LIGHT_END:
        problems.append(
            f"lightest step `{lightest}` has a contrast of "
            f"{contrast(lightest):.2f}:1, below {ORDINAL_LIGHT_END:g}:1"
        )
    return problems


def _steps_summary(values: Sequence[str]) -> str:
    lightness = [oklch(value)[0] for value in values]
    return " → ".join(f"{value:.3f}" for value in lightness)


def check_lightness_steps(values: Sequence[str]) -> CheckResult:
    """
    Check that the colors of an ordered palette form lightness steps.

    Args:
        values: Hex color codes in order (light to dark or dark to light)

    Returns:
        FAIL if the lightness is not monotone, if adjacent steps are too close,
        or if the lightest step is too light against the background
    """
    problems = _check_steps(values, require_darkening=False)
    detail = f"OKLCH L {_steps_summary(values)}"
    if problems:
        return CheckResult(
            "Lightness steps", Level.FAIL, detail + "; " + "; ".join(problems)
        )
    return CheckResult("Lightness steps", Level.PASS, detail)


def split_diverging(values: Sequence[str]) -> Tuple[List[str], List[str]]:
    """
    Split a diverging palette into its two sides, each ordered from the
    center outward. The middle color of an odd-length palette is excluded.

    Args:
        values: Hex color codes in palette order

    Returns:
        Tuple of the first side and the second side
    """
    half = len(values) // 2
    first = list(reversed(values[:half]))
    second = list(values[len(values) - half :])
    return first, second


def check_diverging_steps(values: Sequence[str]) -> CheckResult:
    """
    Check that each side of a diverging palette gets darker from the center outward.

    Args:
        values: Hex color codes in palette order

    Returns:
        FAIL if either side does not meet the lightness step criteria
    """
    details: List[str] = []
    problems: List[str] = []
    for label, side in zip(("first side", "second side"), split_diverging(values)):
        if not side:
            continue
        details.append(f"{label} {_steps_summary(side)}")
        problems.extend(
            f"{label}: {problem}"
            for problem in _check_steps(side, require_darkening=True)
        )
    detail = "OKLCH L from the center: " + "; ".join(details)
    if problems:
        return CheckResult(
            "Lightness steps", Level.FAIL, detail + "; " + "; ".join(problems)
        )
    return CheckResult("Lightness steps", Level.PASS, detail)


def check_palette(palette: Dict[str, Any]) -> PaletteResult:
    """
    Run the checks that apply to a palette, based on its type and scale.

    Categorical palettes are checked for adjacent color differences and the
    number of colors, unless they are marked `scale: ordinal`, in which case
    they are checked for lightness steps like sequential palettes. Diverging
    palettes are checked for lightness steps on each side. All palettes are
    checked for contrast against the background.

    Args:
        palette: Palette dictionary

    Returns:
        Results of the checks
    """
    palette_type = palette.get("type", "categorical")
    colors = palette.get("colors", [])
    keys = [str(color.get("key", "")) for color in colors]
    values = [str(color.get("value", "")) for color in colors]

    checks = [check_contrast(keys, values)]
    if palette_type == "diverging":
        checks.append(check_diverging_steps(values))
    elif palette_type == "sequential" or palette.get("scale") == "ordinal":
        checks.append(check_lightness_steps(values))
    else:
        checks.extend(
            [
                check_color_vision(keys, values),
                check_typical_vision(keys, values),
                check_color_count(values),
            ]
        )

    return PaletteResult(
        name=palette.get("name", ""),
        palette_type=palette_type,
        compliance=palette.get("compliance", ""),
        checks=checks,
        keys=keys,
        values=values,
    )


def check_palettes(palettes: List[Dict[str, Any]]) -> List[PaletteResult]:
    """
    Run the checks on all palettes.

    Args:
        palettes: List of palette dictionaries

    Returns:
        List of results, in the order of the palettes
    """
    return [check_palette(palette) for palette in palettes]


def _effective_level(result: PaletteResult) -> str:
    """Level label of a palette, noting failures that are not treated as errors."""
    if result.level == Level.FAIL and not result.strict:
        return "FAIL (warning only)"
    return result.level.name


def format_text_report(results: List[PaletteResult]) -> str:
    """
    Format the results as plain text for the console.

    Args:
        results: List of palette results

    Returns:
        Text report
    """
    lines: List[str] = []
    for result in results:
        compliance = result.compliance or "not set"
        lines.append(
            f"[{_effective_level(result)}] {result.name} "
            f"({result.palette_type}, compliance: {compliance})"
        )
        for check in result.checks:
            lines.append(f"  {check.level.name:<4}  {check.name}: {check.detail}")
        lines.append("")
    counts = {level: 0 for level in Level}
    for result in results:
        counts[result.level] += 1
    lines.append(
        f"{len(results)} palette(s): {counts[Level.PASS]} pass, "
        f"{counts[Level.WARN]} warn, {counts[Level.FAIL]} fail"
    )
    return "\n".join(lines)


def _escape(text: str) -> str:
    """Escape characters that break a Markdown table cell."""
    return text.replace("|", "\\|")


def render_markdown_report(results: List[PaletteResult]) -> str:
    """
    Render the results as a Markdown report.

    Args:
        results: List of palette results

    Returns:
        Markdown text
    """
    lines = list(REPORT_HEADER)
    lines.extend(
        [
            "## Summary",
            "",
            "| Palette | Type | Compliance | Result |",
            "| --- | --- | --- | --- |",
        ]
    )
    for result in results:
        lines.append(
            f"| {_escape(result.name)} | {result.palette_type} | "
            f"{result.compliance or 'not set'} | {_effective_level(result)} |"
        )
    lines.append("")

    for result in results:
        lines.extend(
            [
                f"## {_escape(result.name)}",
                "",
                "| Check | Result | Details |",
                "| --- | --- | --- |",
            ]
        )
        for check in result.checks:
            lines.append(
                f"| {check.name} | {check.level.name} | {_escape(check.detail)} |"
            )
        lines.extend(
            [
                "",
                f"| Key | Color | Contrast against `{SURFACE}` | OKLCH L |",
                "| --- | --- | --- | --- |",
            ]
        )
        for key, value in zip(result.keys, result.values):
            lines.append(
                f"| {_escape(key)} | `{value}` | {contrast(value):.2f}:1 | "
                f"{oklch(value)[0]:.3f} |"
            )
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    """
    Check palettes.yml, print the results, and write the Markdown report.

    Exits with status 1 if any palette marked `compliance: validated` fails a check.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    yaml_path = os.path.join(repo_root, "palettes.yml")
    report_path = os.path.join(repo_root, "docs", "palette-report.md")

    print(f"Checking palettes in {yaml_path}...")
    results = check_palettes(load_palettes(yaml_path))
    print(format_text_report(results))

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(render_markdown_report(results))
    print(f"Report written to {report_path}.")

    errors = [r.name for r in results if r.strict and r.level == Level.FAIL]
    if errors:
        print(
            "Palettes marked 'compliance: validated' failed the checks: "
            + ", ".join(errors)
        )
        sys.exit(1)
