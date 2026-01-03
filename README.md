<!-- markdownlint-disable MD013 -->

# IR Data Visualization Color Guidelines

[日本語版はこちら](./README-ja.md)

> [!IMPORTANT]
> This repository is a work in progress. The contents herein are NOT final and do NOT represent the official policies and practices of the Division of Institutional Research at Akita International University. Please do NOT cite or distribute the contents herein without explicit permission from the Division of Institutional Research.

## Purpose

The purpose of this document is to ensure consistency, visibility, and accessibility for the output produced by the Division of Institutional Research (IR Team) in the Office of Academic Affairs at the Akita International University (AIU) by defining a clear set of policies and practices for the palettes, i.e., set of colors, that are used in data visualizations produced by the team.

## Scope

All visualized data produced by the IR Team, including, but not limited to dashboards, reports, plots, and presentation materials.

## Policy

Palettes should be set in adherence with AIU's web accessibility policy at [AIUウェブアクセシビリティ方針](https://web.aiu.ac.jp/web-accessibility-policy/). Moreover, since AIU's web accessibility policies are set in line with the latest stable version of the Web Content Accessibility Guidelines (WCAG), the latter should be referenced for any aspects not explicitly covered by the former.

Whenever applicable, all new palettes should be chosen from the colorblind-friendly palettes of the [`RColorBrewer` package](https://cran.r-project.org/web/packages/RColorBrewer/index.html) in R to ensure that materials produced by the IR Team can be comprehensible regardless of the recipients' color blindness.

> [!NOTE]
> While we strive to ensure that all visualizations produced by the IR Team are accessible to people with color vision deficiencies, we acknowledge that under our current resources available, it was only practical to migrate the majority of our color palettes from existing visualizations that are not fully colorblind-friendly. We will continue to work towards improving the accessibility of our visualizations over time. Any suggestions and feedback, particularly those that help us automate the process of ensuring colorblind-friendliness, are highly appreciated.

## Basic Color Palette Definitions

Basic color palettes typically used in many visualizations are preset in a settings file at the root of this repository: `./palettes.yml`

Based on this YAML file, a Python script in this repository `./scripts/build.py` will generate a Tableau preference file `./tableau/Preferences.tps` and an R script `./r_script/ir_color_palettes.R` that can be used for the respective tools to color the visualizations.

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
