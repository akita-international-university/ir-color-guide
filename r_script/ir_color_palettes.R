# Color palettes based on the IR Data Visualization Color Guidelines
# This file is created automatically. Do NOT edit manually.
# See: https://github.com/akita-international-university/ir-color-guide

color_values_4_scale_likert <- c(
    # Type: Diverging
    # Description: 4-Scale Likert color palette from Strongly Agree to Strongly Disagree, using the diverging colors of the AIU Design System: green for the positive side and purple for the negative side. Use the 5-Scale Likert palette for scales with a neutral option.
    # Credit: AIU Design System diverging tokens (div-*)
    "Strongly Agree" = "#194e13",
    "Agree" = "#339028",
    "Disagree" = "#9b5bae",
    "Strongly Disagree" = "#5a2769"
)

color_values_4_scale_likert_ja <- c(
    # Type: Diverging
    # Description: 4-Scale Likert color palette from Strongly Agree to Strongly Disagree, using the diverging colors of the AIU Design System: green for the positive side and purple for the negative side. Use the 5-Scale Likert palette for scales with a neutral option.
    # Credit: AIU Design System diverging tokens (div-*)
    # Alias of color_values_4_scale_likert
    "とても思う" = "#194e13",
    "思う" = "#339028",
    "思わない" = "#9b5bae",
    "全く思わない" = "#5a2769"
)

color_values_5_scale_likert <- c(
    # Type: Diverging
    # Description: 5-Scale Likert color palette from Strongly Agree to Strongly Disagree with a neutral option in the middle, using the diverging colors of the AIU Design System: green for the positive side, a neutral gray in the middle, and purple for the negative side. The neutral color is a light gray close to the background; in stacked bar charts, separate the segments with 2px white gaps and add a value label to each segment.
    # Credit: AIU Design System diverging tokens (div-*)
    "Strongly Agree" = "#194e13",
    "Agree" = "#339028",
    "Neutral" = "#ebeeea",
    "Disagree" = "#9b5bae",
    "Strongly Disagree" = "#5a2769"
)

color_values_5_scale_likert_ja <- c(
    # Type: Diverging
    # Description: 5-Scale Likert color palette from Strongly Agree to Strongly Disagree with a neutral option in the middle, using the diverging colors of the AIU Design System: green for the positive side, a neutral gray in the middle, and purple for the negative side. The neutral color is a light gray close to the background; in stacked bar charts, separate the segments with 2px white gaps and add a value label to each segment.
    # Credit: AIU Design System diverging tokens (div-*)
    # Alias of color_values_5_scale_likert
    "とても思う" = "#194e13",
    "思う" = "#339028",
    "どちらともいえない" = "#ebeeea",
    "思わない" = "#9b5bae",
    "全く思わない" = "#5a2769"
)

color_values_4_scale_likert_piyg_legacy <- c(
    # Type: Diverging
    # Description: Legacy colors of the 4-Scale Likert palette up to v1.x, kept only for recreating existing materials with the same colors. Do not use it in new materials; use the 4-Scale Likert palette instead.
    # Credit: Adapted from the 'PiYG' diverging palette in RColorBrewer
    "Strongly Agree" = "#386325",
    "Agree" = "#8dbb54",
    "Disagree" = "#d17dac",
    "Strongly Disagree" = "#821851"
)

color_values_4_scale_likert_piyg_legacy_ja <- c(
    # Type: Diverging
    # Description: Legacy colors of the 4-Scale Likert palette up to v1.x, kept only for recreating existing materials with the same colors. Do not use it in new materials; use the 4-Scale Likert palette instead.
    # Credit: Adapted from the 'PiYG' diverging palette in RColorBrewer
    # Alias of color_values_4_scale_likert_piyg_legacy
    "とても思う" = "#386325",
    "思う" = "#8dbb54",
    "思わない" = "#d17dac",
    "全く思わない" = "#821851"
)

color_values_aiu_grades <- c(
    # Type: Categorical
    # Description: Colors for AIU letter grades
    "A+" = "#24693d",
    "A" = "#519c51",
    "A-" = "#b3e0a6",
    "B+" = "#2c5985",
    "B" = "#3b96b2",
    "B-" = "#bce4d8",
    "C+" = "#7c4d79",
    "C" = "#b27ba1",
    "C-" = "#eec9e5",
    "D+" = "#ca5422",
    "D" = "#ffc685",
    "F" = "#d3293d",
    "P" = "#5b8cb8",
    "F*" = "#ffbeb2",
    "AP" = "#4e79a7"
)

color_values_aiu_abbreviated_exam_types <- c(
    # Type: Categorical
    # Description: Colors for the abbreviated exam types at AIU
    "A" = "#2a5783",
    "B" = "#5b8cb8",
    "C" = "#b9ddf1",
    "GS" = "#24693d",
    "GW" = "#b3e0a6",
    "Sougou" = "#9e3d22",
    "Recommendation" = "#e36420",
    "International" = "#f59c3c",
    "Gap" = "#ffc685",
    "Other Undergrad Exams" = "#9f3632",
    "Transfer (2nd yr) Sp. Non Degree" = "#59504e",
    "Transfer (2nd yr)" = "#948c88",
    "Transfer (Others)" = "#dcd4d0"
)

color_values_aiu_abbreviated_exam_types_ja_full <- c(
    # Type: Categorical
    # Description: Colors for the abbreviated exam types at AIU
    # Alias of color_values_aiu_abbreviated_exam_types
    "A" = "#2a5783",
    "B" = "#5b8cb8",
    "C" = "#b9ddf1",
    "グローバル・セミナー" = "#24693d",
    "グローバル・ワークショップ" = "#b3e0a6",
    "総合選抜型" = "#9e3d22",
    "学校推薦型" = "#e36420",
    "外国人留学生" = "#f59c3c",
    "ギャップイヤー" = "#ffc685",
    "その他の学部入試" = "#9f3632",
    "編入学 (2年次特科)" = "#59504e",
    "編入学 (2年次)" = "#948c88",
    "編入学 (その他)" = "#dcd4d0"
)

color_values_aiu_student_status <- c(
    # Type: Categorical
    # Description: Colors for the student status (現況区分) at AIU
    "In School" = "#4e7fac",
    "On leave" = "#ffc685",
    "Graduated" = "#24693d",
    "Completed" = "#59a253",
    "Withdrawn" = "#9f3632",
    "Expelled" = "#49525e"
)

color_values_aiu_student_status_ja <- c(
    # Type: Categorical
    # Description: Colors for the student status (現況区分) at AIU
    # Alias of color_values_aiu_student_status
    "通常" = "#4e7fac",
    "休学" = "#ffc685",
    "卒業" = "#24693d",
    "修了" = "#59a253",
    "退学" = "#9f3632",
    "除籍" = "#49525e"
)

color_values_aiu_program_affiliation <- c(
    # Type: Categorical
    # Description: Colors for program affiliations for students, courses, and faculty members at AIU
    # Credit: Derived from built-in 'Automatic' palette in Tableau
    "GB" = "#4e79a7",
    "GS" = "#f28e2b",
    "GC" = "#e15759"
)

color_values_aiu_eap_level_at_enrollment <- c(
    # Type: Categorical
    # Description: Colors for the EAP level at enrollment for undergraduate students at AIU
    # Credit: Derived primarily from the built-in 'Green-Gold' palette in Tableau
    "EAP I" = "#f4d166",
    "EAP II" = "#a7bf5a",
    "EAP III" = "#60a656",
    "EAP Bridge" = "#39894c",
    "NA" = "#49525e"
)

color_values_aiu_in_school_semesters <- c(
    # Type: Categorical
    # Description: Colors for the in-school semesters at AIU
    # Credit: Derived primarily from the built-in 'Hue Circle' palette in Tableau
    "0" = "#1ba3c6",
    "1" = "#2db7c0",
    "2" = "#2fbaa9",
    "3" = "#1fae81",
    "4" = "#38a452",
    "5" = "#6ca932",
    "6" = "#bcbd22",
    "7" = "#e4ba21",
    "8" = "#f8a61c",
    "9" = "#f88113",
    "10" = "#e74b21",
    "11" = "#e6343b",
    "12" = "#f43c63",
    "13" = "#fa6692",
    "14" = "#f075b0",
    "15" = "#d669be",
    "16" = "#a76dc2",
    "Exchange" = "#9f3632",
    "Other" = "#59504e"
)

color_values_aiu_course_levels <- c(
    # Type: Categorical
    # Description: Colors for the course levels at AIU
    # Credit: Derived primarily from built-in 'Summer' palette in Tableau
    "700" = "#b9ca5d",
    "600" = "#f1788d",
    "500" = "#8fb202",
    "400" = "#cf3e53",
    "300" = "#f3a546",
    "200" = "#b9ddf1",
    "100" = "#5b8cb8",
    "0" = "#2a5783"
)

color_values_aiu_exchange_region <- c(
    # Type: Categorical
    # Description: Colors for regions for inbound exchange student origin or outbound student destination at AIU
    # Credit: Derived from 'PowerBI Default' Tableau palette by Ken Flerlage  available at https://public.tableau.com/app/profile/ken.flerlage/viz/DatafamColors/
    "North America" = "#3599b8",
    "South America" = "#8ad4eb",
    "Europe" = "#01b8aa",
    "Asia" = "#fe9666",
    "Oceania" = "#dfbdbf",
    "Africa" = "#a66999",
    "※Other" = "#5f6b6d"
)

color_values_aiu_inbound_student_status <- c(
    # Type: Categorical
    # Description: Colors for inbound student status types at AIU
    "New" = "#1abc9c",
    "Continuing" = "#607d8b"
)

color_values_aiu_inbound_student_status_per_semester <- c(
    # Type: Categorical
    # Description: Colors for inbound student status types per semester at AIU
    "New - Spring" = "#d1f2eb",
    "New - Summer" = "#a3e4d7",
    "New - Fall" = "#76d7c4",
    "New - Winter" = "#48c9b0",
    "Continuing - Spring" = "#cfd8dc",
    "Continuing - Summer" = "#b0bec5",
    "Continuing - Fall" = "#90a4ae",
    "Continuing - Winter" = "#78909c"
)

color_values_aiu_inbound_student_length_of_stay <- c(
    # Type: Categorical
    # Description: Colors for inbound student length of stay category at AIU
    # Credit: Derived from 'Pantone Color of the Year' Tableau palette by Rodrigo Calloni  available at https://public.tableau.com/app/profile/ken.flerlage/viz/DatafamColors/
    "Intensive" = "#f5df4d",
    "1 Semester" = "#fa7268",
    "1 Year" = "#0f4c81",
    "Multi Year" = "#5f4b8b"
)

color_values_aiu_outbound_study_abroad_program <- c(
    # Type: Categorical
    # Description: Colors for study abroad program category at AIU
    # Credit: Derived from built-in 'Automatic' palette in Tableau
    "EX" = "#59a14f",
    "EX (SP-B)" = "#4e79a7",
    "EX-Opt" = "#a0cbe8",
    "EX-V" = "#86bcb6",
    "FP" = "#b07aa1",
    "FP(SP-A)" = "#d4a6c8",
    "※IS" = "#ff9d9a"
)

color_values_aiu_categorical <- c(
    # Type: Categorical
    # Description: Base categorical palette of the AIU Design System, starting with the school color. Use it for variables without a domain-specific palette. Assign the colors in this fixed order and never skip or reorder them, since the order itself keeps adjacent colors distinguishable for color vision deficiencies. Group the ninth and subsequent categories into 'Other'. In charts where any two colors may be adjacent, such as scatter plots and maps, use only the first three colors.
    # Credit: AIU Design System (chart-1 to chart-8)
    "Green" = "#339028",
    "Blue" = "#2863ab",
    "Magenta" = "#a53c75",
    "Ochre" = "#aa821e",
    "Violet" = "#5d4099",
    "Orange" = "#cb6620",
    "Teal" = "#059393",
    "Brick" = "#96372b"
)

color_values_aiu_sequential_green <- c(
    # Type: Sequential
    # Description: Base sequential palette of the AIU Design System, from light (small values) to dark (large values). Use it for quantities such as heat maps and choropleth maps. The lightest steps are close to the background; for ordered categories, use the five steps from 3 to 7.
    # Credit: AIU Design System (seq-1 to seq-7)
    "1" = "#e2f5df",
    "2" = "#b5e3af",
    "3" = "#73c169",
    "4" = "#52aa47",
    "5" = "#339028",
    "6" = "#24691c",
    "7" = "#154310"
)

color_values_aiu_diverging_purple_green <- c(
    # Type: Diverging
    # Description: Base diverging palette of the AIU Design System, with purple for the negative side, a neutral gray in the middle, and green for the positive side. Use it for values on both sides of a reference point, such as year-over-year changes or positive and negative ratings.
    # Credit: AIU Design System (div-neg-3 to div-mid to div-pos-3)
    "Negative 3" = "#5a2769",
    "Negative 2" = "#9b5bae",
    "Negative 1" = "#d8b6e2",
    "Neutral" = "#ebeeea",
    "Positive 1" = "#9bd693",
    "Positive 2" = "#339028",
    "Positive 3" = "#194e13"
)

color_values_aiu_status <- c(
    # Type: Categorical
    # Description: Status palette of the AIU Design System, only for series that imply good or bad, such as achieved and not achieved. Success is a blue-green so that it is not distinguished from the school color green or the danger red by hue alone. Never rely on color alone; always add labels or icons. Info is placed between Warning and Danger so that the two are not adjacent.
    # Credit: AIU Design System (success, warning, danger, info)
    "Success" = "#056965",
    "Warning" = "#8a560c",
    "Info" = "#285e9f",
    "Danger" = "#b02b27"
)
