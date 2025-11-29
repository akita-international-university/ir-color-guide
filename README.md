# IR Data Visualization Color Guidelines

> [!IMPORTANT]
> This repository is a work in progress. The contents herein are NOT final and do NOT represent the official policies and practices of the Division of Institutional Research at Akita International University. Please do NOT cite or distribute the contents herein without explicit permission from the Division of Institutional Research.

## Purpose

The purpose of this document is to ensure consistency, visibility, and accessibility for the output produced by the Division of Institutional Research (IR) in the Office of Academic Affairs at the Akita International University (AIU) by defining a clear set of policies and practices for the palettes, i.e., set of colors, that are used in data visualizations produced by the team.

## Scope

All visualized data produced by the IR team, including, but not limited to dashboards, reports, plots, and presentation materials.

## Policy

Palettes should be set in adherence with AIU's web accessibility policy at [ウェブアクセシビリティ方針 | 公立大学法人 国際教養大学 | Akita International University](https://web.aiu.ac.jp/web-accessibility-policy/). In essence, AIU's web accessibility policies are set in line with the latest stable version of the Web Content Accessibility Guidelines (WCAG).

Whenever applicable, palettes should be chosen from the colorblind-friendly palettes of the [`RColorBrewer` package](https://cran.r-project.org/web/packages/RColorBrewer/index.html) in R to ensure that materials produced by the IR team can be comprehensible regardless of the recipients' color blindness.

## Technical Note

> [!NOTE]
> Installing [R, the free and open-sourced software environment for statistical computing and graphics](https://www.r-project.org/), is a prerequisite for this section.

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
> You do not need to explicity load `RColorBrewer` if you are using the [`tidyverse` packages](https://tidyverse.org/). Simply load `tidyverse` via `library(tidyverse)` to make `RColorBrewer` available within that session.

## Basic Color Palette Definitions

Basic color palettes typically used in many visualizations are preset in a settings file at the root of this repository: `./palettes.yml`

Based on this YAML file, a Python script in this repository `./scripts/build.py` will generate a Tableau preference file `./tableau/Preferences.tps` and an R script `./r_script/ir_color_palettes.R` that can be used for the respective tools to color the visualizations.

This set of a single settings YAML file and the automatically generated files for the respective tools ensures consistency between multiple tools used by the IR team. All revisions to the predefined color palettes should be made to the YAML file and not the individual files.

### How to use the palettes
