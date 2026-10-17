"""
Unit tests for ./scripts/validate.py
"""

import os
from pathlib import Path
import re
from typing import Any, Dict, List

import pytest

from scripts import build, validate

REPO_ROOT = Path(__file__).resolve().parents[1]

# 4-Scale Likert as of the introduction of the checks; the expected values were
# confirmed with the JavaScript checker of the AIU Design System.
LIKERT_4 = ["#386325", "#8dbb54", "#d17dac", "#821851"]


def make_palette(
    values: List[str], palette_type: str = "categorical", **extra: Any
) -> Dict[str, Any]:
    """Build a palette dictionary from a list of color values."""
    return {
        "name": "Test",
        "type": palette_type,
        "colors": [{"key": f"K{i}", "value": value} for i, value in enumerate(values)],
        **extra,
    }


def levels(result: validate.PaletteResult) -> Dict[str, validate.Level]:
    """Map each check name to its level."""
    return {check.name: check.level for check in result.checks}


class TestColorMath:
    """Tests for the color conversion and difference functions."""

    def test_contrast_black_and_white(self):
        """Black and white have the maximum contrast of 21:1."""
        assert validate.contrast("#000000", "#ffffff") == pytest.approx(21.0)
        assert validate.contrast("#ffffff", "#000000") == pytest.approx(21.0)

    def test_contrast_same_color(self):
        """A color has a contrast of 1:1 with itself."""
        assert validate.contrast("#339028", "#339028") == pytest.approx(1.0)

    def test_contrast_defaults_to_white(self):
        """The background defaults to white."""
        assert validate.contrast("#000000") == pytest.approx(21.0)

    def test_contrast_known_value(self):
        """WCAG contrast of #767676 on white is about 4.54:1."""
        assert validate.contrast("#767676") == pytest.approx(4.54, abs=0.01)

    def test_oklch_extremes(self):
        """White has L=1 and black has L=0, both without chroma."""
        white = validate.oklch("#ffffff")
        black = validate.oklch("#000000")
        assert white[0] == pytest.approx(1.0, abs=1e-4)
        assert white[1] == pytest.approx(0.0, abs=1e-4)
        assert black[0] == pytest.approx(0.0, abs=1e-6)

    def test_oklch_hue(self):
        """Pure red has a hue of about 29 degrees in OKLCH."""
        assert validate.oklch("#ff0000")[2] == pytest.approx(29.2, abs=0.1)

    @pytest.mark.parametrize("kind", [None, "protan", "deutan"])
    def test_delta_e_same_color(self, kind):
        """The distance between a color and itself is 0."""
        assert validate.delta_e("#339028", "#339028", kind) == pytest.approx(0.0)

    def test_delta_e_black_and_white(self):
        """Black and white are 100 apart in OKLab x100."""
        assert validate.delta_e("#000000", "#ffffff") == pytest.approx(100.0, abs=0.1)

    def test_cvd_red_green_confusion(self):
        """Red and green are far apart normally but close under simulated CVD."""
        normal = validate.delta_e("#d62728", "#2ca02c")
        assert validate.cvd_delta_e("#d62728", "#2ca02c") < normal / 2

    def test_reference_values_for_4_scale_likert(self):
        """Match the values of the AIU Design System checker (13.2 and 25.2)."""
        pairs = list(zip(LIKERT_4, LIKERT_4[1:]))
        cvd = min(validate.cvd_delta_e(a, b) for a, b in pairs)
        normal = min(validate.delta_e(a, b) for a, b in pairs)
        assert round(cvd, 1) == 13.2
        assert round(normal, 1) == 25.2


class TestChecks:
    """Tests for the individual checks."""

    def test_contrast_pass(self):
        """Dark colors pass the contrast check."""
        result = validate.check_contrast(["A", "B"], ["#000000", "#194e13"])
        assert result.level == validate.Level.PASS

    def test_contrast_lists_low_colors(self):
        """Colors below 3:1 are listed with a warning."""
        result = validate.check_contrast(["Dark", "Pale"], ["#000000", "#ffc685"])
        assert result.level == validate.Level.WARN
        assert "Pale" in result.detail
        assert "Dark" not in result.detail

    def test_color_vision_pass(self):
        """Distinct adjacent colors pass."""
        result = validate.check_color_vision(["A", "B"], ["#000000", "#ffffff"])
        assert result.level == validate.Level.PASS

    def test_color_vision_fail(self):
        """Red and green next to each other fail under simulated CVD."""
        result = validate.check_color_vision(["R", "G"], ["#d62728", "#2ca02c"])
        assert result.level == validate.Level.FAIL
        assert "R (`#d62728`) / G (`#2ca02c`)" in result.detail

    def test_color_vision_warn_between_floor_and_target(self, mocker):
        """A minimum between 6 and 8 requires supplementary cues."""
        mocker.patch("scripts.validate.cvd_delta_e", return_value=7.0)
        result = validate.check_color_vision(["A", "B"], ["#000000", "#ffffff"])
        assert result.level == validate.Level.WARN
        assert "supplementary cues" in result.detail

    def test_color_vision_uses_adjacent_pairs_only(self):
        """Non-adjacent similar colors are reported but do not fail."""
        values = ["#000000", "#ffffff", "#000000"]
        result = validate.check_color_vision(["A", "B", "C"], values)
        assert result.level == validate.Level.PASS
        assert "all pairs minimum 0.0" in result.detail

    def test_typical_vision_fail(self):
        """Similar adjacent colors fail under typical color vision."""
        result = validate.check_typical_vision(["A", "B"], ["#2db7c0", "#2fbaa9"])
        assert result.level == validate.Level.FAIL

    def test_typical_vision_pass(self):
        """The 4-Scale Likert palette passes under typical color vision."""
        keys = ["A", "B", "C", "D"]
        result = validate.check_typical_vision(keys, LIKERT_4)
        assert result.level == validate.Level.PASS

    @pytest.mark.parametrize(
        "check", [validate.check_color_vision, validate.check_typical_vision]
    )
    def test_single_color_passes(self, check):
        """A single color has no pairs to compare."""
        assert check(["A"], ["#000000"]).level == validate.Level.PASS

    def test_color_count(self):
        """Up to 8 colors pass; 9 or more warn."""
        assert validate.check_color_count(["#000000"] * 8).level == validate.Level.PASS
        assert validate.check_color_count(["#000000"] * 9).level == validate.Level.WARN

    @pytest.mark.parametrize(
        "values",
        [
            ["#74c476", "#31a354", "#006d2c"],
            ["#006d2c", "#31a354", "#74c476"],
        ],
    )
    def test_lightness_steps_pass_in_either_direction(self, values):
        """Monotone steps pass from light to dark and from dark to light."""
        assert validate.check_lightness_steps(values).level == validate.Level.PASS

    def test_lightness_steps_not_monotone(self):
        """Steps that go back and forth fail."""
        result = validate.check_lightness_steps(["#c7e9c0", "#006d2c", "#74c476"])
        assert result.level == validate.Level.FAIL
        assert "not monotone" in result.detail

    def test_lightness_steps_too_close(self):
        """Adjacent steps closer than 0.06 in L fail."""
        result = validate.check_lightness_steps(["#74c476", "#6dbd70", "#006d2c"])
        assert result.level == validate.Level.FAIL
        assert "below 0.06" in result.detail

    def test_lightness_steps_lightest_too_light(self):
        """A lightest step below 2:1 against white fails."""
        result = validate.check_lightness_steps(["#f7fcf5", "#74c476", "#006d2c"])
        assert result.level == validate.Level.FAIL
        assert "lightest step `#f7fcf5`" in result.detail

    def test_split_diverging_even(self):
        """Each side is ordered from the center outward."""
        assert validate.split_diverging(["a", "b", "c", "d"]) == (
            ["b", "a"],
            ["c", "d"],
        )

    def test_split_diverging_odd(self):
        """The neutral middle color is excluded."""
        assert validate.split_diverging(["a", "b", "m", "c", "d"]) == (
            ["b", "a"],
            ["c", "d"],
        )

    def test_diverging_steps_pass(self):
        """The 4-Scale Likert palette gets darker toward both ends."""
        result = validate.check_diverging_steps(LIKERT_4)
        assert result.level == validate.Level.PASS

    def test_diverging_steps_fail_when_center_is_dark(self):
        """A side that gets lighter toward the end fails."""
        values = ["#8dbb54", "#386325", "#d17dac", "#821851"]
        result = validate.check_diverging_steps(values)
        assert result.level == validate.Level.FAIL
        assert "first side: lightness is not monotone" in result.detail

    def test_diverging_steps_single_color(self):
        """A palette too short to have sides passes."""
        result = validate.check_diverging_steps(["#999999"])
        assert result.level == validate.Level.PASS


class TestCheckPalette:
    """Tests for selecting the checks by palette type."""

    def test_categorical(self):
        """Categorical palettes get the distinguishability checks."""
        result = validate.check_palette(make_palette(["#000000", "#ffffff"]))
        assert list(levels(result)) == [
            "Contrast",
            "Color vision deficiencies",
            "Typical color vision",
            "Number of colors",
        ]

    def test_categorical_ordinal(self):
        """Categorical palettes marked as ordinal get the lightness check."""
        palette = make_palette(["#c7e9c0", "#006d2c"], scale="ordinal")
        assert list(levels(validate.check_palette(palette))) == [
            "Contrast",
            "Lightness steps",
        ]

    def test_sequential(self):
        """Sequential palettes get the lightness check."""
        palette = make_palette(["#c7e9c0", "#006d2c"], "sequential")
        assert list(levels(validate.check_palette(palette))) == [
            "Contrast",
            "Lightness steps",
        ]

    def test_diverging(self):
        """Diverging palettes get the lightness check on each side."""
        result = validate.check_palette(make_palette(LIKERT_4, "diverging"))
        assert "first side" in result.checks[1].detail

    def test_result_level_and_strictness(self):
        """The palette level is the most severe check level."""
        palette = make_palette(["#d62728", "#2ca02c"], compliance="validated")
        result = validate.check_palette(palette)
        assert result.level == validate.Level.FAIL
        assert result.strict
        assert not validate.check_palette(make_palette(["#000000"])).strict

    def test_check_palettes_keeps_order(self):
        """Results follow the order of the palettes."""
        palettes = [
            {**make_palette(["#000000"]), "name": "First"},
            {**make_palette(["#000000"]), "name": "Second"},
        ]
        names = [r.name for r in validate.check_palettes(palettes)]
        assert names == ["First", "Second"]


class TestReports:
    """Tests for the text and Markdown reports."""

    def test_text_report(self):
        """Failures outside validated palettes are marked as warnings only."""
        results = validate.check_palettes(
            [
                make_palette(["#d62728", "#2ca02c"]),
                {
                    **make_palette(["#000000", "#2a5783"]),
                    "name": "Strict",
                    "compliance": "validated",
                },
            ]
        )
        text = validate.format_text_report(results)
        assert "[FAIL (warning only)] Test (categorical, compliance: not set)" in text
        assert "[PASS] Strict (categorical, compliance: validated)" in text
        assert text.endswith("2 palette(s): 1 pass, 0 warn, 1 fail")

    def test_markdown_report(self):
        """The report has a summary row and a color row for each palette."""
        palette = make_palette(["#000000"])
        palette["colors"][0]["key"] = "A|B"
        report = validate.render_markdown_report(validate.check_palettes([palette]))
        assert report.startswith("<!-- markdownlint-disable MD013 -->")
        assert "| Test | categorical | not set | PASS |" in report
        assert "| A\\|B | `#000000` | 21.00:1 | 0.000 |" in report

    def test_committed_report_is_up_to_date(self):
        """docs/palette-report.md matches palettes.yml (run `poetry run build`)."""

        def normalize(text: str) -> List[str]:
            # Ignore the table padding added by Prettier
            lines = []
            for line in text.strip().splitlines():
                line = re.sub(r"-{3,}", "---", line)
                lines.append(re.sub(r"\s+", " ", line).strip())
            return lines

        results = validate.check_palettes(
            build.load_palettes(str(REPO_ROOT / "palettes.yml"))
        )
        committed = (REPO_ROOT / "docs" / "palette-report.md").read_text(
            encoding="utf-8"
        )
        assert normalize(committed) == normalize(
            validate.render_markdown_report(results)
        )


class TestMain:
    """Tests for the main function."""

    @pytest.fixture
    def repo(self, tmp_path, mocker):
        """Point the script at a temporary repository root."""
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        mocker.patch(
            "scripts.validate.os.path.abspath",
            return_value=str(scripts_dir / "validate.py"),
        )
        mocker.patch("builtins.print")
        return tmp_path

    def test_main_writes_report(self, repo, mocker):
        """The report is written and warnings do not fail."""
        mocker.patch(
            "scripts.validate.load_palettes",
            return_value=[make_palette(["#d62728", "#2ca02c"])],
        )
        validate.main()
        report = (repo / "docs" / "palette-report.md").read_text(encoding="utf-8")
        assert "FAIL (warning only)" in report

    def test_main_exits_on_validated_failure(self, repo, mocker):
        """A failure in a validated palette exits with status 1."""
        mocker.patch(
            "scripts.validate.load_palettes",
            return_value=[make_palette(["#d62728", "#2ca02c"], compliance="validated")],
        )
        with pytest.raises(SystemExit) as excinfo:
            validate.main()
        assert excinfo.value.code == 1
        assert os.path.exists(repo / "docs" / "palette-report.md")
