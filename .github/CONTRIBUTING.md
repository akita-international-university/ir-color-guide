# Contributing to IR Data Visualization Color Guidelines

Thank you for your interest in the IR Data Visualization Color Guidelines repository!

> [!IMPORTANT]
> **This repository is maintained by the Division of Institutional Research at Akita International University (AIU) as an internal guideline for the AIU community.** While we warmly welcome suggestions, questions, and comments via GitHub issues, we do not expect or solicit pull requests from members outside the AIU community.
>
> This repository is disclosed publicly to:
>
> - Provide transparency in our data visualization practices
> - Serve as an example of enhancing inclusiveness within the university's community
> - Share our approach to standardizing color palettes for accessibility
>
> The repository maintainers will be responsible for reviewing and deciding whether to implement any suggestions made through GitHub issues.

## How to Contribute (AIU Community Members)

If you are a member of the AIU community and would like to contribute to this repository, please follow the guidelines below.

### Reporting Issues and Making Suggestions

We encourage all community members to:

- **Report issues**: If you find bugs, inconsistencies, or accessibility problems with the color palettes
- **Suggest improvements**: If you have ideas for new palettes or enhancements to existing ones
- **Ask questions**: If you need clarification on how to use the palettes or the repository structure

To submit an issue:

1. Check [existing issues](https://github.com/akita-international-university/ir-color-guide/issues) to see if your concern has already been raised
2. If not, [create a new issue](https://github.com/akita-international-university/ir-color-guide/issues/new) with a clear and descriptive title
3. Provide as much relevant information as possible:
   - What you expected to happen
   - What actually happened
   - Steps to reproduce (if applicable)
   - Screenshots or examples (if applicable)

> [!IMPORTANT]
> If you notice any security vulnerabilities, please do NOT report them through GitHub issues. Instead, follow the instructions in our [Security Policy](https://github.com/akita-international-university/ir-color-guide/blob/main/.github/SECURITY.md) to report them responsibly.

### Development Environment Setup

For detailed information on setting up the development environment, running build commands, and understanding the repository structure, please refer to our [GitHub Copilot Custom Instructions](./copilot-instructions.md).

Key points to remember:

- **Never manually edit auto-generated files**: `tableau/Preferences.tps` and `r_script/ir_color_palettes.R` are automatically generated from `palettes.yml`
- **Always run `poetry run test`** before committing changes to ensure all tests pass
- **Follow the existing code style**: The repository uses Prettier, Black, isort, mypy, and pylint

## Understanding `palettes.yml`

The `palettes.yml` file is the **single source of truth** for all color palettes in this repository. All platform-specific files (Tableau, R) are automatically generated from this file.

### File Structure

```yaml
organization:
  name: 'Division of Institutional Research, Office of Academic Affairs, AIU'
  name_ja: '国際教養大学教務課教学IRチーム'
  email: 'ir.div@aiu.ac.jp'
palettes:
  - name: 'Palette Name'
    type: 'categorical' # categorical, sequential, or diverging
    description: 'Description of the palette'
    credit: 'Optional credit/source information'
    colors:
      - key: 'Label'
        value: '#hexcolor'
    aliases:
      - name: 'alias-name'
        keys: ['Alternative Label 1', 'Alternative Label 2']
```

### Field Specifications

#### Organization Section

- **`name`** (required): English name of the organization maintaining the color guidelines
- **`name_ja`** (required): Japanese name of the organization
- **`email`** (required): Contact email for the organization

#### Palettes Section

Each palette in the `palettes` array must include:

- **`name`** (required): Unique name for the palette (e.g., "AIU Grades", "4-Scale Likert")
  - Must be unique across all palettes
  - Should be descriptive and concise

- **`type`** (required): Type of the palette, must be one of:
  - `categorical`: For distinct categories with no inherent order (e.g., grades, regions)
  - `sequential`: For ordered data from low to high (e.g., levels, intensities)
  - `diverging`: For data with a meaningful midpoint (e.g., Likert scales)

- **`description`** (required): Clear description of what the palette represents and when to use it

- **`credit`** (optional): Attribution for palette source or inspiration (e.g., "Adapted from RColorBrewer 'PiYG' palette")

- **`colors`** (required): Array of color definitions, each with:
  - **`key`** (required): Label for the color (e.g., "A+", "Strongly Agree")
    - Must be unique within the palette
    - Can include spaces and special characters
  - **`value`** (required): Hex color code in lowercase format (e.g., `#24693d`)
    - Must be exactly 6 lowercase hexadecimal characters preceded by `#`
    - Examples: `#24693d`, `#ffc685`, `#1abc9c`

- **`aliases`** (optional): Array of alternative label sets for the same color sequence
  - **`name`** (required): Name of the alias set (e.g., "ja" for Japanese, "ja-full" for full Japanese terms)
    - Must be unique within the palette
  - **`keys`** (required): Array of alternative labels in the same order as the `colors` array
    - Must have the same number of items as the `colors` array
    - Each key must be unique within the alias set

### Validation Rules

The `palettes.yml` file is validated by the build script (`scripts/build.py`) with the following rules:

1. **Security constraints**:
   - String fields cannot contain double quotes (`"`) or angle brackets (`<`, `>`)
   - This prevents injection attacks and ensures safe XML/HTML generation

2. **Color format**:
   - All color values must be lowercase hexadecimal: `^#[a-f0-9]{6}$`
   - Examples of valid colors: `#24693d`, `#ffc685`, `#1abc9c`
   - Invalid examples: `#24693D` (uppercase), `#fff` (too short), `#gggggg` (invalid characters)

3. **Uniqueness**:
   - Palette names must be unique across all palettes
   - Color keys must be unique within each palette
   - Alias names must be unique within each palette

4. **Consistency**:
   - Alias key arrays must have the same number of items as the color array
   - Each alias set provides alternative labels for the same sequence of colors

### Example Palette

```yaml
palettes:
  - name: 'AIU Grades'
    type: 'categorical'
    description: 'Colors for AIU letter grades'
    colors:
      - key: 'A+'
        value: '#24693d'
      - key: 'A'
        value: '#519c51'
      - key: 'B+'
        value: '#2c5985'
```

### Making Changes to Palettes

When proposing changes to `palettes.yml`:

1. Ensure all color values follow the format `#[a-f0-9]{6}` (lowercase hex)
2. Verify that palette names and color keys are unique
3. Consider accessibility:
   - Prefer colorblind-friendly palettes from RColorBrewer when possible
   - Ensure sufficient contrast for readability
   - Test colors with colorblind simulation tools if available
4. Run `poetry run build` to generate the platform-specific files
5. Run `poetry run test` to ensure all tests pass
6. Submit your changes with a clear description of the rationale

## Code of Conduct

Please note that this project has a [Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## Questions?

If you have any questions about contributing, please:

- Open a [GitHub issue](../../issues/new) for technical questions or suggestions
- Contact the Division of Institutional Research at [ir.div@aiu.ac.jp](mailto:ir.div@aiu.ac.jp) for general inquiries

## License

By contributing to this repository, you agree that your contributions will be licensed under the same license as the project. See the [LICENSE](../LICENSE) file for details.

---

Thank you for helping us improve the IR Data Visualization Color Guidelines!
