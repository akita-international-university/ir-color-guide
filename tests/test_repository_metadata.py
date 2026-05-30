"""Regression tests for repository contact metadata."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

OUTDATED_TERMS = (
    "Division of Institutional Research",
    "教学IRチーム",
    "ir.div@aiu.ac.jp",
    "IR Team",
)

EXPECTED_TERMS = {
    "README.md": ("Office of Strategic Planning",),
    "README-ja.md": ("企画戦略課",),
    "palettes.yml": (
        "Office of Strategic Planning, AIU",
        "国際教養大学企画戦略課",
        "strategic-planning@aiu.ac.jp",
    ),
    ".github/CONTRIBUTING.md": (
        "Office of Strategic Planning",
        "国際教養大学企画戦略課",
        "strategic-planning@aiu.ac.jp",
    ),
    ".github/SECURITY.md": ("strategic-planning@aiu.ac.jp",),
    ".github/CODE_OF_CONDUCT.md": ("strategic-planning@aiu.ac.jp",),
    ".github/copilot-instructions.md": (
        "Office of Strategic Planning",
        "国際教養大学企画戦略課",
        "strategic-planning@aiu.ac.jp",
    ),
    ".github/instructions/palettes.instructions.md": (
        "Office of Strategic Planning, AIU",
        "国際教養大学企画戦略課",
        "strategic-planning@aiu.ac.jp",
    ),
}


def test_department_and_contact_references_are_updated():
    """Ensure the repository no longer references the retired team name or email."""
    for relative_path, expected_terms in EXPECTED_TERMS.items():
        content = (REPO_ROOT / relative_path).read_text(encoding="utf-8")

        for expected in expected_terms:
            assert (
                expected in content
            ), f"Expected term {expected!r} not found in {relative_path}"

        for outdated in OUTDATED_TERMS:
            assert (
                outdated not in content
            ), f"Outdated term {outdated!r} still present in {relative_path}"
