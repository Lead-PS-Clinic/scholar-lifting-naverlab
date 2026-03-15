# STROBE Statement — Checklist of Items for Cross-Sectional Studies

**Study title:** From Early Adopters to Mainstream Market: The Maturation of Non-Surgical Lifting Search Interest Toward Older Demographics in South Korea — An Age-Stratified Infodemiology Study Using Naver DataLab, 2016–2025

| Item No | Recommendation | Reported on page/section |
|---------|---------------|------------------------|
| **Title and abstract** | | |
| 1 | (a) Indicate the study's design with a commonly used term in the title or the abstract | Title ("Age-Stratified Infodemiology Study"); Abstract/Methods ("cross-sectional time series analysis") |
| | (b) Provide in the abstract an informative and balanced summary of what was done and what was found | Abstract (Background, Objective, Methods, Results, Conclusions) |
| **Introduction** | | |
| 2 | Explain the scientific background and rationale for the investigation being reported | Introduction, P1–P4 |
| 3 | State specific objectives, including any prespecified hypotheses | Introduction, P5 (Study Aim) |
| **Methods** | | |
| 4 | Present key elements of study design early in the paper | Methods, Study Design ("cross-sectional time series analysis of age-stratified internet search behavior") |
| 5 | Describe the setting, locations, and relevant dates, including periods of recruitment, exposure, follow-up, and data collection | Methods, Data Sources ("January 2016 to December 2025, 120 months"); Data Collection ("180 primary API calls") |
| 6 | (a) Cross-sectional study — Give the eligibility criteria, and the sources and methods of selection of participants | Methods, Keyword Selection (6 keyword groups defined); Age Group Definitions (codes 3–11 included; 1–2 excluded) |
| 7 | Clearly define all outcomes, exposures, predictors, potential confounders, and effect modifiers | Methods, Statistical Analysis (RSV as outcome; Time, Young, Time×Young as predictors; monthly dummies for seasonality) |
| 8 | For each variable of interest, give sources of data and details of methods of assessment (measurement) | Methods, Data Sources (Naver DataLab API, Google Trends); Keyword Selection (Table 1) |
| 9 | Describe any efforts to address potential sources of bias | Methods, Statistical Analysis (Newey-West HAC SEs for autocorrelation; BH-FDR for multiple comparisons; Approach A designed to avoid cross-age normalization bias); Sensitivity Analyses (Prais-Winsten GLS, Fourier terms, platform migration correction) |
| 10 | Explain how the study size was arrived at | Methods, Data Collection ("180 primary API calls... 21,274 data points"; 120 months × 6 keywords × age/gender conditions) |
| 11 | Explain how quantitative variables were handled in the analyses | Methods, Statistical Analysis (RSV as continuous outcome; Time as months 1–120; Young as binary indicator; monthly dummies) |
| 12 | (a) Describe all statistical methods | Methods, Statistical Analysis (Approach A: OLS with HAC SEs; Approach B: proportional share and YTR; joinpoint regression; BH-FDR correction) |
| | (b) Describe any methods used to examine subgroups and interactions | Methods, Additional Analyses (gender stratification; procedure-specific β₃ comparison) |
| | (c) Explain how missing data were addressed | Methods, Data Collection ("All 180 Naver API calls succeeded; InMode had sparse data during its early period, 326 of 3600 expected data points missing") |
| | (d) Cross-sectional study — If applicable, describe analytical methods taking account of sampling strategy | Not applicable (aggregate population-level search data, not sampled) |
| | (e) Describe any sensitivity analyses | Methods, Sensitivity Analyses (Prais-Winsten GLS for AR(1) correction; Fourier terms for seasonal specification; platform migration adjustment at 3/5/7% annual attrition; monthly joinpoint analysis with n=120) |
| **Results** | | |
| 13 | (a) Report numbers of individuals at each stage of study | Results, first paragraph ("21,274 data points"; "120 months") |
| | (b) Give reasons for non-participation at each stage | Results (InMode: 326 missing data points due to pre-launch zero search volume, primarily 2016–2017) |
| | (c) Consider use of a flow diagram | Not applicable (aggregate search data, no participant flow) |
| 14 | (a) Give characteristics of study participants and information on exposures and potential confounders | Results, Overall Temporal Trends (6 keywords, growth rates); Table 1 (keyword definitions) |
| | (b) Indicate number of participants with missing data for each variable of interest | Results, Data Collection (InMode: 326 missing data points from early period) |
| 15 | Cross-sectional study — Report numbers of outcome events or summary measures | Results, Tables 2–4; YTR values; β₃ coefficients with CIs |
| 16 | (a) Give unadjusted estimates and, if applicable, confounder-adjusted estimates and their precision | Results, Tables 3–4 (β₃ with SE, 95% CI, P values); Model Diagnostics (DW, Ljung-Box Q) |
| | (b) Report category boundaries when continuous variables were categorized | Methods, Age Group Definitions (Young 19–34, Middle 35–44, Traditional 45+) |
| | (c) If relevant, consider translating estimates into meaningful clinical measures | Results, YTR interpretation ("young adults searched at 1.42 times the rate") |
| 17 | Report other analyses done — e.g., analyses of subgroups and interactions, and sensitivity analyses | Results: Gender Stratification (Table 4); Joinpoint Analysis (annual + monthly sensitivity); Sensitivity Analyses (Prais-Winsten, Fourier, platform migration); Google Trends Triangulation |
| **Discussion** | | |
| 18 | Summarise key results with reference to study objectives | Discussion, Principal Findings |
| 19 | Discuss limitations of the study, taking into account sources of potential bias or imprecision | Discussion, Limitations (7 limitations with platform migration as primary; sensitivity analysis results referenced) |
| 20 | Give a cautious overall interpretation of results considering objectives, limitations, multiplicity of analyses, results from similar studies, and other relevant evidence | Discussion, Innovation Diffusion section; Conclusions (balanced interpretation acknowledging platform migration confound; sensitivity analysis bounds) |
| 21 | Discuss the generalisability (external validity) of the study results | Discussion, Limitations ("single-country primary data... Korea's position as a global leader in aesthetic medicine provides external validity"); Methodological Contribution section |
| 22 | Give the source of funding and the role of the funders for the present study and, if applicable, for the original study on which the present article is based | Acknowledgments ("None"); no external funding |
