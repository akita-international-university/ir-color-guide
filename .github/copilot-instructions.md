<!-- markdownlint-disable MD040 -->

# GitHub Copilot Custom Instructions for IR Color Guide

## Overview

This repository contains the IR Data Visualization Color Guidelines for Akita International University (AIU). It defines and manages color palettes for data visualization produced by the Division of Institutional Research (IR). The repository uses a single source of truth (`palettes.yml`) to generate platform-specific files for Tableau and R.

## Repository Structure

```
.
├── .github/
│   ├── instructions/          # Custom instructions for specific file patterns
│   ├── linters/               # Linter configurations (zizmor.yaml)
│   └── workflows/             # GitHub Actions workflows
├── scripts/                   # Python scripts for building and maintenance
│   ├── build.py              # Generates Tableau/R files from palettes.yml
│   ├── formatter.py          # Runs all formatters (Prettier, isort, black)
│   └── linter.py             # Runs all linters (mypy, pylint)
├── r_script/                 # Generated R color palette scripts
│   └── ir_color_palettes.R   # AUTO-GENERATED - DO NOT EDIT
├── tableau/                  # Generated Tableau preference files
│   └── Preferences.tps       # AUTO-GENERATED - DO NOT EDIT
├── palettes.yml              # SOURCE OF TRUTH for all color palettes
├── pyproject.toml            # Python project config with Poetry
├── package.json              # Node.js dependencies (Prettier)
├── README.md                 # English documentation
└── README-ja.md              # Japanese documentation
```

## Build and Development Commands

### Prerequisites

- **Python**: 3.12+ (specified in pyproject.toml)
- **Poetry**: For Python dependency management
- **Node.js & npm**: For Prettier formatting

### Setup

Install dependencies:

```bash
# Install Python dependencies
poetry install

# Install Node.js dependencies
npm install
```

### Build Process

**Generate platform-specific files from palettes.yml:**

```bash
poetry run build
```

This command:

1. Reads `palettes.yml`
2. Generates `tableau/Preferences.tps` (Tableau color preferences)
3. Generates `r_script/ir_color_palettes.R` (R color palette definitions)
4. Runs Prettier on the generated files

**IMPORTANT:** Always run this after modifying `palettes.yml`.

### Code Formatting

**Format all code:**

```bash
poetry run formatter
```

This runs:

1. Prettier (Markdown, YAML, JSON, HTML/TPS files)
2. isort (Python import sorting)
3. black (Python code formatting)

### Linting

**Lint Python code:**

```bash
poetry run linter
```

This runs the formatter first, then:

1. mypy (type checking on `./scripts` directory)
2. pylint (code quality on `./scripts` directory)

Both linters must pass with no errors.

### Testing

**Current status:** No test suite exists (package.json shows `"test": "echo \"Error: no test specified\" && exit 1"`).

## File Modification Guidelines

### CRITICAL: Do Not Edit Auto-Generated Files

These files are automatically generated and should **NEVER** be edited manually:

- `tableau/Preferences.tps`
- `r_script/ir_color_palettes.R`

Always edit `palettes.yml` and run `poetry run build` to update these files.

### Editing palettes.yml

The `palettes.yml` file is the single source of truth. Structure:

```yaml
organization:
  name: 'Division of Institutional Research, Office of Academic Affairs, AIU'
  name_ja: '国際教養大学教務課教学IRチーム'
  email: 'ir.div@aiu.ac.jp'
palettes:
  - name: 'Palette Name'
    type: 'categorical' # categorical, sequential, or diverging
    description: 'Description of the palette'
    colors:
      - key: 'Label'
        value: '#hexcolor'
```

**IMPORTANT:** When editing `palettes.yml`, the generated files **must** be synchronized. See `.github/instructions/palettes.instructions.md` for detailed guidelines including:

- Verification that generated files are included in the PR
- Ensuring generated files match the build output
- Requirements for running `poetry run build`

### README File Synchronization

**IMPORTANT:** The repository maintains bilingual documentation:

- `README.md` (English)
- `README-ja.md` (Japanese)

When editing either file, the corresponding content in the other locale **must** be kept synchronized. See `.github/instructions/readme.instructions.md` for detailed translation guidelines including:

- Document title translations
- Organization name translations
- Tone and formality requirements

## Code Style and Conventions

### Python

- **Formatter**: Black (line length default)
- **Import sorter**: isort with Black profile
- **Type checking**: mypy with strict typing enabled
- **Linter**: pylint
- **Python version**: 3.12+

All Python code is in the `scripts/` directory and must:

- Include type hints for all function parameters and return values
- Pass mypy and pylint without errors
- Be formatted with black and isort

### Markdown, YAML, JSON, HTML

- **Formatter**: Prettier
- **Configuration**: See `.prettierrc`
  - Tab width: 2 spaces
  - Single quotes preferred
  - Trailing commas: all
  - End of line: LF
  - Special: `*.tps` files parsed as HTML

### Special File: Preferences.tps

Tableau preference files (`.tps`) are XML but use `.tps` extension. Prettier treats them as HTML (configured in `.prettierrc`).

## GitHub Actions & CI

### Super Linter Workflow

Located: `.github/workflows/super-linter.yml`

Runs on every push and PR. Configuration:

- Uses `super-linter/super-linter/slim@v8.3.0`
- Linter rules in `.github/linters/`
- Disabled linters:
  - Biome formatter (conflicts with Prettier)
  - Natural language validation
  - Ruff formatter (conflicts with Black & isort)

**Before committing:** Always run `poetry run linter` locally to catch issues early.

### Accessibility Bot

Located: `.github/workflows/a11y-alt-text-bot.yml`

Automatically checks for alt text in images in issues, PRs, and discussions.

### Dependabot

Located: `.github/dependabot.yml`

Automatically updates:

- pip packages (Python)
- npm packages (Node.js)
- GitHub Actions

Weekly updates assigned to @ttsukagoshi.

## Typical Workflows

### Adding a New Color Palette

1. Edit `palettes.yml` to add the new palette
2. Run `poetry run build` to generate files
3. Run `poetry run formatter` to ensure formatting
4. Run `poetry run linter` to verify code quality
5. Commit changes

### Modifying Existing Palettes

1. Edit `palettes.yml` only (never edit generated files)
2. Run `poetry run build`
3. Run `poetry run formatter`
4. Run `poetry run linter`
5. Commit changes

### Updating Documentation

1. Edit `README.md` or `README-ja.md`
2. **Important**: Update the corresponding translation
3. Run `poetry run formatter` (Prettier will format Markdown)
4. Commit both files together

### Modifying Python Scripts

1. Edit Python files in `scripts/` directory
2. Run `poetry run linter` (includes formatter)
3. Fix any mypy or pylint errors
4. Commit changes

## Common Pitfalls and Solutions

### Build Script Issues

**Problem**: `poetry run build` fails with "npx not found"

- **Solution**: Run `npm install` first to ensure Prettier is available

**Problem**: Generated files don't match expected output

- **Solution**: Check `palettes.yml` syntax. YAML is indentation-sensitive.

### Linting Failures

**Problem**: Super Linter fails in CI but passes locally

- **Solution**: Ensure all files are formatted. Run `poetry run formatter` before committing.

**Problem**: mypy reports type errors

- **Solution**: Add type hints. All functions must have parameter and return type annotations.

### Poetry Virtual Environment

Poetry creates a virtual environment in `.venv/` (configured in `poetry.toml`):

```toml
[virtualenvs]
in-project = true
prefer-active-python = true
```

If having issues:

```bash
# Remove and recreate virtual environment
rm -rf .venv/
poetry install
```

## Important Notes

1. **Trust these instructions**: The commands and workflows documented here have been verified. Only search for additional information if these instructions are incomplete or incorrect.

2. **No manual editing of generated files**: The `r_script/ir_color_palettes.R` and `tableau/Preferences.tps` files are generated by `scripts/build.py`. Direct edits will be overwritten.

3. **Run commands in order**: When making changes to `palettes.yml`:
   - First: `poetry run build`
   - Second: `poetry run formatter`
   - Third: `poetry run linter`

4. **README synchronization is mandatory**: When editing README files, both English and Japanese versions must be updated to maintain content parity.

5. **VSCode integration**: If using VSCode, settings in `.vscode/settings.json` configure:
   - Black as Python formatter
   - Prettier for Markdown/YAML/JSON/HTML
   - Format on save enabled
   - Python type checking enabled

6. **Git hooks**: No pre-commit hooks are configured. Always run linter manually before committing.

7. **Line endings**: All files use LF (Unix) line endings (enforced by Prettier and VSCode settings).
