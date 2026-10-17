<!-- markdownlint-disable MD013 -->
<!-- This file is created automatically by `poetry run validate`. Do NOT edit manually. -->

# Palette Validation Report

Results of checking each palette in [`palettes.yml`](../palettes.yml) against the [quantitative criteria](../README.md#quantitative-criteria) of the IR Data Visualization Color Guidelines.

- Background: `#ffffff`
- Color vision deficiencies: protanopia and deuteranopia simulated with Machado et al. (2009), severity 1.0
- Color difference: Euclidean distance in OKLab multiplied by 100
- `FAIL` is treated as an error only for palettes marked `compliance: validated`; otherwise it is reported as a warning.

## Summary

| Palette                                 | Type        | Compliance | Result              |
| --------------------------------------- | ----------- | ---------- | ------------------- |
| 4-Scale Likert                          | diverging   | not set    | WARN                |
| AIU Grades                              | categorical | not set    | WARN                |
| AIU Abbreviated Exam Types              | categorical | not set    | FAIL (warning only) |
| AIU Student Status                      | categorical | not set    | WARN                |
| AIU Program Affiliation                 | categorical | not set    | FAIL (warning only) |
| AIU EAP Level at Enrollment             | categorical | not set    | FAIL (warning only) |
| AIU In-School Semesters                 | categorical | not set    | FAIL (warning only) |
| AIU Course Levels                       | categorical | not set    | WARN                |
| AIU Exchange Region                     | categorical | not set    | FAIL (warning only) |
| AIU Inbound Student Status              | categorical | not set    | WARN                |
| AIU Inbound Student Status per Semester | categorical | not set    | FAIL (warning only) |
| AIU Inbound Student Length of Stay      | categorical | not set    | FAIL (warning only) |
| AIU Outbound Study Abroad Program       | categorical | not set    | FAIL (warning only) |

## 4-Scale Likert

| Check           | Result | Details                                                                                       |
| --------------- | ------ | --------------------------------------------------------------------------------------------- |
| Contrast        | WARN   | Below 3:1 (use labels or a data table): Agree (`#8dbb54`) 2.24:1, Disagree (`#d17dac`) 2.90:1 |
| Lightness steps | PASS   | OKLCH L from the center: first side 0.737 → 0.453; second side 0.694 → 0.411                  |

| Key               | Color     | Contrast against `#ffffff` | OKLCH L |
| ----------------- | --------- | -------------------------- | ------- |
| Strongly Agree    | `#386325` | 7.05:1                     | 0.453   |
| Agree             | `#8dbb54` | 2.24:1                     | 0.737   |
| Disagree          | `#d17dac` | 2.90:1                     | 0.694   |
| Strongly Disagree | `#821851` | 9.55:1                     | 0.411   |

## AIU Grades

| Check                     | Result | Details                                                                                                                                                   |
| ------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): A- (`#b3e0a6`) 1.49:1, B- (`#bce4d8`) 1.38:1, C- (`#eec9e5`) 1.49:1, D (`#ffc685`) 1.54:1, F\* (`#ffbeb2`) 1.58:1 |
| Color vision deficiencies | PASS   | Adjacent minimum 15.9 at C+ (`#7c4d79`) / C (`#b27ba1`); all pairs minimum 1.1 (reference)                                                                |
| Typical color vision      | PASS   | Adjacent minimum 16.2 at C+ (`#7c4d79`) / C (`#b27ba1`)                                                                                                   |
| Number of colors          | WARN   | 15 colors; group the categories after the 8th into 'Other'                                                                                                |

| Key | Color     | Contrast against `#ffffff` | OKLCH L |
| --- | --------- | -------------------------- | ------- |
| A+  | `#24693d` | 6.64:1                     | 0.465   |
| A   | `#519c51` | 3.37:1                     | 0.626   |
| A-  | `#b3e0a6` | 1.49:1                     | 0.860   |
| B+  | `#2c5985` | 7.31:1                     | 0.453   |
| B   | `#3b96b2` | 3.39:1                     | 0.631   |
| B-  | `#bce4d8` | 1.38:1                     | 0.887   |
| C+  | `#7c4d79` | 6.57:1                     | 0.490   |
| C   | `#b27ba1` | 3.36:1                     | 0.651   |
| C-  | `#eec9e5` | 1.49:1                     | 0.876   |
| D+  | `#ca5422` | 4.37:1                     | 0.592   |
| D   | `#ffc685` | 1.54:1                     | 0.864   |
| F   | `#d3293d` | 5.05:1                     | 0.565   |
| P   | `#5b8cb8` | 3.57:1                     | 0.623   |
| F\* | `#ffbeb2` | 1.58:1                     | 0.858   |
| AP  | `#4e79a7` | 4.55:1                     | 0.564   |

## AIU Abbreviated Exam Types

| Check                     | Result | Details                                                                                                                                                                             |
| ------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): C (`#b9ddf1`) 1.43:1, GW (`#b3e0a6`) 1.49:1, International (`#f59c3c`) 2.16:1, Gap (`#ffc685`) 1.54:1, Transfer (Others) (`#dcd4d0`) 1.46:1 |
| Color vision deficiencies | FAIL   | Adjacent minimum 4.2 at Other Undergrad Exams (`#9f3632`) / Transfer (2nd yr) Sp. Non Degree (`#59504e`); all pairs minimum 1.8 (reference)                                         |
| Typical color vision      | FAIL   | Adjacent minimum 10.7 at International (`#f59c3c`) / Gap (`#ffc685`)                                                                                                                |
| Number of colors          | WARN   | 13 colors; group the categories after the 8th into 'Other'                                                                                                                          |

| Key                              | Color     | Contrast against `#ffffff` | OKLCH L |
| -------------------------------- | --------- | -------------------------- | ------- |
| A                                | `#2a5783` | 7.53:1                     | 0.446   |
| B                                | `#5b8cb8` | 3.57:1                     | 0.623   |
| C                                | `#b9ddf1` | 1.43:1                     | 0.878   |
| GS                               | `#24693d` | 6.64:1                     | 0.465   |
| GW                               | `#b3e0a6` | 1.49:1                     | 0.860   |
| Sougou                           | `#9e3d22` | 6.68:1                     | 0.490   |
| Recommendation                   | `#e36420` | 3.44:1                     | 0.652   |
| International                    | `#f59c3c` | 2.16:1                     | 0.767   |
| Gap                              | `#ffc685` | 1.54:1                     | 0.864   |
| Other Undergrad Exams            | `#9f3632` | 6.89:1                     | 0.484   |
| Transfer (2nd yr) Sp. Non Degree | `#59504e` | 7.83:1                     | 0.439   |
| Transfer (2nd yr)                | `#948c88` | 3.30:1                     | 0.646   |
| Transfer (Others)                | `#dcd4d0` | 1.46:1                     | 0.875   |

## AIU Student Status

| Check                     | Result | Details                                                                                                                              |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): On leave (`#ffc685`) 1.54:1                                                                  |
| Color vision deficiencies | WARN   | Adjacent minimum 6.8 at Withdrawn (`#9f3632`) / Expelled (`#49525e`); all pairs minimum 4.4 (reference); supplementary cues required |
| Typical color vision      | PASS   | Adjacent minimum 16.4 at Withdrawn (`#9f3632`) / Expelled (`#49525e`)                                                                |
| Number of colors          | PASS   | 6 colors                                                                                                                             |

| Key       | Color     | Contrast against `#ffffff` | OKLCH L |
| --------- | --------- | -------------------------- | ------- |
| In School | `#4e7fac` | 4.24:1                     | 0.581   |
| On leave  | `#ffc685` | 1.54:1                     | 0.864   |
| Graduated | `#24693d` | 6.64:1                     | 0.465   |
| Completed | `#59a253` | 3.13:1                     | 0.645   |
| Withdrawn | `#9f3632` | 6.89:1                     | 0.484   |
| Expelled  | `#49525e` | 7.92:1                     | 0.435   |

## AIU Program Affiliation

| Check                     | Result | Details                                                                                      |
| ------------------------- | ------ | -------------------------------------------------------------------------------------------- |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): GS (`#f28e2b`) 2.42:1                                |
| Color vision deficiencies | PASS   | Adjacent minimum 11.9 at GS (`#f28e2b`) / GC (`#e15759`); all pairs minimum 11.9 (reference) |
| Typical color vision      | FAIL   | Adjacent minimum 14.6 at GS (`#f28e2b`) / GC (`#e15759`)                                     |
| Number of colors          | PASS   | 3 colors                                                                                     |

| Key | Color     | Contrast against `#ffffff` | OKLCH L |
| --- | --------- | -------------------------- | ------- |
| GB  | `#4e79a7` | 4.55:1                     | 0.564   |
| GS  | `#f28e2b` | 2.42:1                     | 0.738   |
| GC  | `#e15759` | 3.68:1                     | 0.638   |

## AIU EAP Level at Enrollment

| Check                     | Result | Details                                                                                                                        |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): EAP I (`#f4d166`) 1.48:1, EAP II (`#a7bf5a`) 2.05:1, EAP III (`#60a656`) 2.96:1        |
| Color vision deficiencies | WARN   | Adjacent minimum 7.8 at EAP I (`#f4d166`) / EAP II (`#a7bf5a`); all pairs minimum 7.8 (reference); supplementary cues required |
| Typical color vision      | FAIL   | Adjacent minimum 9.7 at EAP III (`#60a656`) / EAP Bridge (`#39894c`)                                                           |
| Number of colors          | PASS   | 5 colors                                                                                                                       |

| Key        | Color     | Contrast against `#ffffff` | OKLCH L |
| ---------- | --------- | -------------------------- | ------- |
| EAP I      | `#f4d166` | 1.48:1                     | 0.870   |
| EAP II     | `#a7bf5a` | 2.05:1                     | 0.765   |
| EAP III    | `#60a656` | 2.96:1                     | 0.660   |
| EAP Bridge | `#39894c` | 4.32:1                     | 0.565   |
| NA         | `#49525e` | 7.92:1                     | 0.435   |

## AIU In-School Semesters

| Check                     | Result | Details                                                                                                                                                                                                                                                                                    |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): 0 (`#1ba3c6`) 2.96:1, 1 (`#2db7c0`) 2.43:1, 2 (`#2fbaa9`) 2.41:1, 3 (`#1fae81`) 2.83:1, 5 (`#6ca932`) 2.85:1, 6 (`#bcbd22`) 2.01:1, 7 (`#e4ba21`) 1.85:1, 8 (`#f8a61c`) 2.01:1, 9 (`#f88113`) 2.58:1, 13 (`#fa6692`) 2.85:1, 14 (`#f075b0`) 2.67:1 |
| Color vision deficiencies | FAIL   | Adjacent minimum 1.0 at 6 (`#bcbd22`) / 7 (`#e4ba21`); all pairs minimum 1.0 (reference)                                                                                                                                                                                                   |
| Typical color vision      | FAIL   | Adjacent minimum 3.8 at 1 (`#2db7c0`) / 2 (`#2fbaa9`)                                                                                                                                                                                                                                      |
| Number of colors          | WARN   | 19 colors; group the categories after the 8th into 'Other'                                                                                                                                                                                                                                 |

| Key      | Color     | Contrast against `#ffffff` | OKLCH L |
| -------- | --------- | -------------------------- | ------- |
| 0        | `#1ba3c6` | 2.96:1                     | 0.664   |
| 1        | `#2db7c0` | 2.43:1                     | 0.714   |
| 2        | `#2fbaa9` | 2.41:1                     | 0.713   |
| 3        | `#1fae81` | 2.83:1                     | 0.669   |
| 4        | `#38a452` | 3.18:1                     | 0.638   |
| 5        | `#6ca932` | 2.85:1                     | 0.669   |
| 6        | `#bcbd22` | 2.01:1                     | 0.773   |
| 7        | `#e4ba21` | 1.85:1                     | 0.803   |
| 8        | `#f8a61c` | 2.01:1                     | 0.787   |
| 9        | `#f88113` | 2.58:1                     | 0.724   |
| 10       | `#e74b21` | 3.87:1                     | 0.627   |
| 11       | `#e6343b` | 4.27:1                     | 0.607   |
| 12       | `#f43c63` | 3.70:1                     | 0.644   |
| 13       | `#fa6692` | 2.85:1                     | 0.707   |
| 14       | `#f075b0` | 2.67:1                     | 0.722   |
| 15       | `#d669be` | 3.17:1                     | 0.677   |
| 16       | `#a76dc2` | 3.74:1                     | 0.629   |
| Exchange | `#9f3632` | 6.89:1                     | 0.484   |
| Other    | `#59504e` | 7.83:1                     | 0.439   |

## AIU Course Levels

| Check                     | Result | Details                                                                                                                                                        |
| ------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): 700 (`#b9ca5d`) 1.80:1, 600 (`#f1788d`) 2.69:1, 500 (`#8fb202`) 2.46:1, 300 (`#f3a546`) 2.04:1, 200 (`#b9ddf1`) 1.43:1 |
| Color vision deficiencies | PASS   | Adjacent minimum 10.0 at 600 (`#f1788d`) / 500 (`#8fb202`); all pairs minimum 2.3 (reference)                                                                  |
| Typical color vision      | PASS   | Adjacent minimum 17.7 at 100 (`#5b8cb8`) / 0 (`#2a5783`)                                                                                                       |
| Number of colors          | PASS   | 8 colors                                                                                                                                                       |

| Key | Color     | Contrast against `#ffffff` | OKLCH L |
| --- | --------- | -------------------------- | ------- |
| 700 | `#b9ca5d` | 1.80:1                     | 0.804   |
| 600 | `#f1788d` | 2.69:1                     | 0.717   |
| 500 | `#8fb202` | 2.46:1                     | 0.712   |
| 400 | `#cf3e53` | 4.70:1                     | 0.580   |
| 300 | `#f3a546` | 2.04:1                     | 0.782   |
| 200 | `#b9ddf1` | 1.43:1                     | 0.878   |
| 100 | `#5b8cb8` | 3.57:1                     | 0.623   |
| 0   | `#2a5783` | 7.53:1                     | 0.446   |

## AIU Exchange Region

| Check                     | Result | Details                                                                                                                                                  |
| ------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): South America (`#8ad4eb`) 1.65:1, Europe (`#01b8aa`) 2.49:1, Asia (`#fe9666`) 2.15:1, Oceania (`#dfbdbf`) 1.73:1 |
| Color vision deficiencies | WARN   | Adjacent minimum 7.1 at Africa (`#a66999`) / ※Other (`#5f6b6d`); all pairs minimum 4.9 (reference); supplementary cues required                          |
| Typical color vision      | FAIL   | Adjacent minimum 12.2 at Asia (`#fe9666`) / Oceania (`#dfbdbf`)                                                                                          |
| Number of colors          | PASS   | 7 colors                                                                                                                                                 |

| Key           | Color     | Contrast against `#ffffff` | OKLCH L |
| ------------- | --------- | -------------------------- | ------- |
| North America | `#3599b8` | 3.28:1                     | 0.639   |
| South America | `#8ad4eb` | 1.65:1                     | 0.830   |
| Europe        | `#01b8aa` | 2.49:1                     | 0.704   |
| Asia          | `#fe9666` | 2.15:1                     | 0.773   |
| Oceania       | `#dfbdbf` | 1.73:1                     | 0.828   |
| Africa        | `#a66999` | 4.12:1                     | 0.602   |
| ※Other        | `#5f6b6d` | 5.51:1                     | 0.518   |

## AIU Inbound Student Status

| Check                     | Result | Details                                                                                               |
| ------------------------- | ------ | ----------------------------------------------------------------------------------------------------- |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): New (`#1abc9c`) 2.41:1                                        |
| Color vision deficiencies | PASS   | Adjacent minimum 14.5 at New (`#1abc9c`) / Continuing (`#607d8b`); all pairs minimum 14.5 (reference) |
| Typical color vision      | PASS   | Adjacent minimum 17.9 at New (`#1abc9c`) / Continuing (`#607d8b`)                                     |
| Number of colors          | PASS   | 2 colors                                                                                              |

| Key        | Color     | Contrast against `#ffffff` | OKLCH L |
| ---------- | --------- | -------------------------- | ------- |
| New        | `#1abc9c` | 2.41:1                     | 0.712   |
| Continuing | `#607d8b` | 4.37:1                     | 0.572   |

## AIU Inbound Student Status per Semester

| Check                     | Result | Details                                                                                                                                                                                                                                                                                        |
| ------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): New - Spring (`#d1f2eb`) 1.19:1, New - Summer (`#a3e4d7`) 1.43:1, New - Fall (`#76d7c4`) 1.71:1, New - Winter (`#48c9b0`) 2.05:1, Continuing - Spring (`#cfd8dc`) 1.45:1, Continuing - Summer (`#b0bec5`) 1.91:1, Continuing - Fall (`#90a4ae`) 2.59:1 |
| Color vision deficiencies | FAIL   | Adjacent minimum 4.8 at New - Summer (`#a3e4d7`) / New - Fall (`#76d7c4`); all pairs minimum 0.7 (reference)                                                                                                                                                                                   |
| Typical color vision      | FAIL   | Adjacent minimum 6.0 at New - Fall (`#76d7c4`) / New - Winter (`#48c9b0`)                                                                                                                                                                                                                      |
| Number of colors          | PASS   | 8 colors                                                                                                                                                                                                                                                                                       |

| Key                 | Color     | Contrast against `#ffffff` | OKLCH L |
| ------------------- | --------- | -------------------------- | ------- |
| New - Spring        | `#d1f2eb` | 1.19:1                     | 0.935   |
| New - Summer        | `#a3e4d7` | 1.43:1                     | 0.872   |
| New - Fall          | `#76d7c4` | 1.71:1                     | 0.814   |
| New - Winter        | `#48c9b0` | 2.05:1                     | 0.759   |
| Continuing - Spring | `#cfd8dc` | 1.45:1                     | 0.877   |
| Continuing - Summer | `#b0bec5` | 1.91:1                     | 0.793   |
| Continuing - Fall   | `#90a4ae` | 2.59:1                     | 0.706   |
| Continuing - Winter | `#78909c` | 3.35:1                     | 0.639   |

## AIU Inbound Student Length of Stay

| Check                     | Result | Details                                                                                                |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------------------ |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): Intensive (`#f5df4d`) 1.35:1, 1 Semester (`#fa7268`) 2.74:1    |
| Color vision deficiencies | FAIL   | Adjacent minimum 2.6 at 1 Year (`#0f4c81`) / Multi Year (`#5f4b8b`); all pairs minimum 2.6 (reference) |
| Typical color vision      | FAIL   | Adjacent minimum 9.8 at 1 Year (`#0f4c81`) / Multi Year (`#5f4b8b`)                                    |
| Number of colors          | PASS   | 4 colors                                                                                               |

| Key        | Color     | Contrast against `#ffffff` | OKLCH L |
| ---------- | --------- | -------------------------- | ------- |
| Intensive  | `#f5df4d` | 1.35:1                     | 0.896   |
| 1 Semester | `#fa7268` | 2.74:1                     | 0.713   |
| 1 Year     | `#0f4c81` | 8.86:1                     | 0.409   |
| Multi Year | `#5f4b8b` | 7.33:1                     | 0.463   |

## AIU Outbound Study Abroad Program

| Check                     | Result | Details                                                                                                                                         |
| ------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Contrast                  | WARN   | Below 3:1 (use labels or a data table): EX-Opt (`#a0cbe8`) 1.72:1, EX-V (`#86bcb6`) 2.12:1, FP(SP-A) (`#d4a6c8`) 2.08:1, ※IS (`#ff9d9a`) 1.99:1 |
| Color vision deficiencies | WARN   | Adjacent minimum 6.6 at FP(SP-A) (`#d4a6c8`) / ※IS (`#ff9d9a`); all pairs minimum 2.7 (reference); supplementary cues required                  |
| Typical color vision      | FAIL   | Adjacent minimum 8.3 at EX-Opt (`#a0cbe8`) / EX-V (`#86bcb6`)                                                                                   |
| Number of colors          | PASS   | 7 colors                                                                                                                                        |

| Key       | Color     | Contrast against `#ffffff` | OKLCH L |
| --------- | --------- | -------------------------- | ------- |
| EX        | `#59a14f` | 3.16:1                     | 0.642   |
| EX (SP-B) | `#4e79a7` | 4.55:1                     | 0.564   |
| EX-Opt    | `#a0cbe8` | 1.72:1                     | 0.821   |
| EX-V      | `#86bcb6` | 2.12:1                     | 0.756   |
| FP        | `#b07aa1` | 3.42:1                     | 0.647   |
| FP(SP-A)  | `#d4a6c8` | 2.08:1                     | 0.777   |
| ※IS       | `#ff9d9a` | 1.99:1                     | 0.795   |
