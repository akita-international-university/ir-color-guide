<!-- markdownlint-disable MD013 MD028 MD040 -->

# IR Data Visualization Color Guidelines

[日本語版はこちら](./README-ja.md)

## Purpose

The purpose of this document is to ensure consistency, visibility, and accessibility for the output produced by the Office of Strategic Planning ("the Office") at Akita International University (AIU) by defining a clear set of policies and practices for the palettes, i.e., set of colors, that are used in data visualizations produced by the office.

## Scope

All visualized data produced by the Office, including, but not limited to dashboards, reports, plots, and presentation materials.

## Policy

### Governing standard

Palettes follow the color standards of the AIU Design System, the Office's design standard for documents, web pages, dashboards, and charts. This repository is the implementation of those standards for data visualization tools: it manages and generates the palette files that make the same colors available in Tableau, R, and Exploratory Desktop.

The AIU Design System is based on AIU's web accessibility policy ([AIUウェブアクセシビリティ方針](https://web.aiu.ac.jp/web-accessibility-policy/)) and adopts Level AA of the Web Content Accessibility Guidelines (WCAG) 2.2 as its baseline. Since the AIU Design System is an internal resource, the key criteria for palettes are summarized below. For any aspects not covered here, refer to the web accessibility policy and WCAG 2.2.

### Quantitative criteria

Every palette in this repository should meet the following criteria. In these criteria, "adjacent colors" are colors placed next to each other in the order of a palette, and the OKLab distance is the Euclidean distance between two colors in the OKLab color space, multiplied by 100.

| Aspect                       | Criterion                                                                                                                                                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contrast with the background | Graphical elements in a chart should have a contrast ratio of at least 3:1 against the background (WCAG 2.2 SC 1.4.11). When using a color that does not meet this criterion, always provide direct labels or a data table alongside it.    |
| Color vision deficiencies    | In the protanopia and deuteranopia simulations of Machado et al. (2009), the OKLab distance between adjacent colors should be at least 8. A distance between 6 and 8 is acceptable only with supplementary cues such as labels or patterns. |
| Typical color vision         | The OKLab distance between adjacent colors should be at least 15.                                                                                                                                                                           |
| Number of categorical colors | Up to 8 colors, assigned in a fixed order. Group the ninth and subsequent categories into "Other".                                                                                                                                          |
| Ordered categories           | Use lightness steps of a single hue. The lightness difference (OKLCH L) between adjacent steps should be at least 0.06, and even the lightest step should have a contrast ratio of at least 2:1 against the background.                     |
| Diverging (two-sided) data   | Use two hues with a neutral gray in the middle: green for the positive side and purple for the negative side.                                                                                                                               |
| Categories implying good/bad | Do not rely on color alone; always add labels or icons.                                                                                                                                                                                     |
| Text                         | Do not color value labels or legend text with palette colors; use a dark (near-black) text color.                                                                                                                                           |

### How to choose a palette

Choose a palette in the following order of priority:

1. A domain-specific palette defined for the variable being visualized (e.g., grades, admission types).
2. The basic palettes of the AIU Design System, which start with the school color `#339028` (to be added in [#132](https://github.com/akita-international-university/ir-color-guide/issues/132)).
3. Only if neither of the above is available, a colorblind-friendly palette of the [`RColorBrewer` package](https://cran.r-project.org/web/packages/RColorBrewer/index.html) in R that meets the criteria above (see [Technical Note](#technical-note)).

### Existing palettes

Some palettes in this repository were migrated as-is from existing visualizations and do not fully meet the criteria above. Such palettes will be explicitly marked as "legacy" palettes, kept for compatibility with existing materials ([#138](https://github.com/akita-international-university/ir-color-guide/issues/138)). Legacy palettes should not be used in new materials. A migration guide from each legacy palette to its replacement will be provided ([#139](https://github.com/akita-international-university/ir-color-guide/issues/139)).

### Automated checks

Compliance with the criteria above will be checked automatically by `poetry run test` ([#137](https://github.com/akita-international-university/ir-color-guide/issues/137)). Any suggestions and feedback on improving the accessibility of our palettes are highly appreciated.

## Basic Color Palette Definitions

Basic color palettes typically used in many visualizations are preset in a settings file at the root of this repository: `./palettes.yml`

Based on this YAML file, a Python script in this repository `./scripts/build.py` will generate a Tableau preference file `./tableau/Preferences.tps`, an R script `./r_script/ir_color_palettes.R`, and Exploratory Desktop palette JSON files under `./exploratory/` that can be used for the respective tools to color the visualizations.

This set of a single settings YAML file and the automatically generated files for the respective tools ensures consistency between multiple tools used by the IR team. All revisions to the predefined color palettes should be made to the YAML file and not the individual files.

### How to use the palettes

> [!NOTE]
> Installing [R, the free and open-sourced software environment for statistical computing and graphics](https://www.r-project.org/), is a prerequisite for this section and below.

#### R

The simplest way to use the color palettes defined in this repository in R is to download and source the generated R script [`./r_script/ir_color_palettes.R`](./r_script/ir_color_palettes.R) in the R script or Quarto document that you are working on:

```r
# In the file you are working on, e.g., analysis.R or report.qmd
source("path/to/this/repository/r_script/ir_color_palettes.R")

# ggplot2 usage example:
df |>
  ggplot(aes(x = year, y = value, fill = category)) +
  geom_col() +
  scale_fill_manual(values = color_values_4scale_likert) # Using a predefined palette
```

If you need to refer dynamically to the latest version of the R script without downloading it manually, replace the source file path with the GitHub URL:

```r
source("https://raw.githubusercontent.com/akita-international-university/ir-color-guide/refs/heads/main/r_script/ir_color_palettes.R")
```

While the method above can incorporate any changes made to the color palette as soon as it enters the `main` branch, it is also prone to breaking changes. In a production environment, using the versioned URL (e.g., referring to a specific tag or commit hash) is always the best practice to ensure stability. For example, to refer to a specific version tag:

```r
# Example of sourcing a specific version (v1.2.3)
source("https://raw.githubusercontent.com/akita-international-university/ir-color-guide/refs/tags/v1.2.3/r_script/ir_color_palettes.R")
```

> [!TIP]
> If you are not sure which method to use to source the R script, use the last method with a specific version tag. It is generally the safest option.

#### Tableau

Custom color palettes in Tableau Desktop can be defined by modifying the `Preferences.tps` file created locally during the installation of the software. This section demonstrates how to use the generated `Preferences.tps` file from this repository to set up custom color palettes in Tableau Desktop on your Windows PC.

> [!IMPORTANT]
> The method below overwrites the existing `Preferences.tps` file in your Tableau repository. If you have any existing custom color palettes defined in your current `Preferences.tps`, please back up the file before proceeding.

> [!NOTE]
> For more details on how to create custom color palettes in Tableau, please refer to Tableau's official documentation: [Create Custom Color Palettes](https://help.tableau.com/current/pro/desktop/en-us/formatting_create_custom_colors.htm).

1. Locate your Tableau repository folder. By default, it is located at:
   ```
   C:\Users\<YourUsername>\Documents\My Tableau Repository
   ```
2. Inside the `My Tableau Repository` folder, find the existing `Preferences.tps` file. Make a backup copy of this file in case you need to restore it later.
3. Copy the generated `Preferences.tps` file from this repository ([`./tableau/Preferences.tps`](./tableau/Preferences.tps)) to the `My Tableau Repository` folder, replacing the existing file.
4. Restart Tableau Desktop if it is currently running.

#### Exploratory Desktop

Custom color palettes in [Exploratory Desktop](https://exploratory.io/) can be added by placing JSON files in the `palettes` directory of Exploratory Desktop's local repository. This section demonstrates how to use the generated JSON files from this repository to set up custom color palettes in Exploratory Desktop on your Windows PC.

> [!TIP]
> For more details on how to create custom color palettes in Exploratory Desktop, please refer to the official documentation: [How to Create Custom Color Palette](https://exploratory.io/note/exploratory/How-to-Create-Custom-Color-Palette-rQl5ciH6).

1. Locate the `palettes` directory of your Exploratory Desktop local repository. By default, it is located at:
   ```
   C:\Users\<YourUsername>\.exploratory\palettes
   ```
2. Copy the generated JSON files from [`./exploratory/`](./exploratory/) in this repository into the `palettes` directory above.
3. Restart Exploratory Desktop if it is currently running.

## Technical Note

Colorblind-friendly palettes of RColorBrewer can be retrieved by a simple command in the R Console:

```r
# install.packages("RColorBrewer")
# or
# renv::install("RColorBrewer")
# if you already haven't.
library(RColorBrewer)
RColorBrewer::display.brewer.all(colorblindFriendly = TRUE)
```

> [!TIP]
> You do not need to explicitly load `RColorBrewer` if you are using the [`tidyverse` packages](https://tidyverse.org/). Simply load `tidyverse` via `library(tidyverse)` to make `RColorBrewer` available within that session.

## Contributing

Please refer to the [Contributing Guidelines](./.github/CONTRIBUTING.md) if you are interested in contributing to this repository.
