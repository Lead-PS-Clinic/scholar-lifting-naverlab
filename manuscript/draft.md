# From Early Adopters to Mainstream Market: The Maturation of Non-Surgical Lifting Search Interest Toward Older Demographics in South Korea — An Age-Stratified Infodemiology Study Using Naver DataLab, 2016–2025

## Authors

Joonho Lim, MD

LEAD Plastic Surgery Clinic, Dogok-dong, Gangnam-gu, Seoul, South Korea

ORCID: 0000-0002-4556-1536

**Corresponding author:**
Joonho Lim, MD
LEAD Plastic Surgery Clinic
Dogok-dong, Gangnam-gu, Seoul, South Korea
[Email to be added]

---

## Abstract

### Background
Non-surgical facial lifting procedures, including high-intensity focused ultrasound (HIFU), radiofrequency (RF), and thread lifting, represent one of the fastest-growing segments of the global aesthetic medicine market. A widely held assumption — variously termed "prejuvenation" or "preventive aesthetics" — posits that younger consumers are increasingly entering this traditionally older market. However, this demographic shift has never been quantified at the population level because no major search engine trend platform provides age-stratified data, with the sole exception of Naver DataLab in South Korea.

### Objective
This study aimed to characterize the direction and magnitude of age-demographic shifts in public search interest for non-surgical lifting procedures in South Korea between 2016 and 2025, to identify procedure-specific and gender-specific patterns, and to test whether Korean age-stratified data support or contradict the global prejuvenation narrative.

### Methods
We conducted a cross-sectional time series analysis of age-stratified internet search behavior using Naver DataLab's Search Trend API (January 2016 to December 2025; 180 API calls across 6 keyword groups, 9 age codes, and 3 gender conditions). The primary analysis (Approach A) compared the growth rate of relative search volume (RSV) between the Young (20–34 years) and Traditional (45+ years) age groups using an interaction model with Newey-West heteroscedasticity and autocorrelation consistent standard errors. The secondary analysis (Approach B) computed the Young-to-Traditional Ratio (YTR) of proportional search share annually. Joinpoint regression identified inflection points, and Benjamini-Hochberg false discovery rate correction controlled for multiple comparisons. Google Trends data for global prejuvenation-related keywords provided contextual comparison. The study followed STROBE guidelines.

### Results
All 6 keywords showed overall growth (all β₁ > 0). Contrary to the prejuvenation hypothesis, the Time × Young interaction coefficient (β₃) was significantly negative for 3 of 6 keywords after Benjamini-Hochberg correction: thread lifting (β₃ = −0.573; P < .001), generic lifting (β₃ = −0.558; P < .001), and HIFU-value (β₃ = −0.267; P < .001), indicating the Traditional (45+) group grew significantly faster than the Young (20–34) group. The mean Young-to-Traditional Ratio declined from 1.42 in 2016 to 0.77 in 2025. Joinpoint regression identified a 3-phase trajectory: youth-dominated early adoption (2016–2018), rapid traditional-demographic overtake (2018–2022), and stabilization (2022–2025). The maturation effect was stronger among female searchers. Sensitivity analyses (Prais-Winsten GLS, Fourier seasonal terms, platform migration correction up to 7% annual young-user attrition) confirmed robustness for the 2 strongest keywords, though results for other keywords were sensitive to platform migration assumptions. Meanwhile, Google Trends showed exponential global growth of "prejuvenation" search terms — a dissociation demonstrating that age-agnostic trend data can produce misleading conclusions about demographic composition.

### Conclusions
Public search interest in non-surgical lifting in South Korea followed an innovation diffusion trajectory: young adults were disproportionate early adopters, but the traditional 45+ demographic showed faster sustained growth and overtook the younger group by 2022. This contradicts the widely assumed prejuvenation narrative and highlights the critical importance of age-stratified analysis in infodemiology. Naver DataLab's globally unique age-stratified API represents an underutilized resource for health information-seeking research.

### Keywords
infodemiology; non-surgical lifting; age-stratified search trends; Naver DataLab; Google Trends; HIFU; radiofrequency; thread lifting; prejuvenation; South Korea; innovation diffusion

---

## Introduction

### The Rise of Non-Surgical Lifting

Non-surgical facial lifting has become one of the fastest-growing segments of the global aesthetic medicine market. High-intensity focused ultrasound (HIFU), radiofrequency (RF) devices, and absorbable thread lifting offer facial tightening and contouring without surgical incision. The International Society of Aesthetic Plastic Surgery reported that nonsurgical skin tightening procedures increased globally by over 40% between 2019 and 2023 [1]. South Korea, one of the world's largest markets for aesthetic procedures, has been at the forefront of this expansion, with multiple domestically developed devices (Shurink, InMode, Oligio) achieving widespread adoption alongside international brands (Ultherapy, Thermage) [2].

### Who Drives Non-Surgical Lifting Demand? Competing Hypotheses

Traditionally, non-surgical lifting was sought primarily by patients aged 45 years and older as an alternative to surgical facelift [3]. However, practitioners and industry observers have proposed competing narratives about the evolving demographic composition of demand [4]. One hypothesis — "prejuvenation" or "preventive aesthetics" (termed "슬로우에이징" [slow aging] in Korean consumer culture) — posits that younger consumers in their late 20s and 30s are increasingly entering the market, broadening the consumer base downward in age [5,6]. An alternative hypothesis, grounded in innovation diffusion theory, suggests that young adults may function as early adopters who drive initial awareness, while the traditional 45+ patient base — representing the core clinical indication for skin laxity — subsequently expands as market awareness matures [7]. Understanding which pattern prevails has implications for clinical practice, where patient expectations and risk profiles differ by age; for the aesthetic device market, where pricing and marketing strategies must address the actual consumer base; and for infodemiology methodology, where the question arises whether aggregate search trends accurately reflect demographic shifts [8]. Neither pattern has been quantified at the population level using age-stratified data.

### The Limitation of Existing Infodemiology Tools

Infodemiology — the study of online health information-seeking behavior — has become a standard method for tracking public interest in aesthetic procedures [9]. Google Trends has been used extensively to analyze temporal patterns in searches for botulinum toxin [10], dermal fillers [11], blepharoplasty [12], and other procedures [13]. However, Google Trends does not provide age-stratified data: it is impossible to determine whether a rise in search volume for a lifting procedure is driven by younger or older consumers [14]. This is a critical limitation for any research question concerning age-specific shifts in information-seeking behavior — patterns that remain invisible when only aggregate volume is observed. No other major global search engine trend tool provides public age-stratified search application programming interfaces (APIs) [15].

### Naver DataLab: A Unique Data Source

Naver, the dominant search engine in South Korea (approximately 56% market share) [16], provides a public Search Trend API through Naver DataLab that returns relative search volume (RSV) indices stratified by 11 age bins (0–12 years through 60+ years), gender (male/female, based on user profile registration), and device type (personal computer/mobile). This makes Naver DataLab the only major search trend platform worldwide that enables population-level, age-stratified analysis of health information-seeking behavior [15]. Meanwhile, Google Trends data for global English-language keywords can document the emergence of prejuvenation-related terminology — such as "prejuvenation" and "preventive botox" — a narrative that can be tested against the age-stratified Korean search data.

### Study Aim

This study aimed to (1) characterize the direction and magnitude of age-demographic shifts in public search interest for non-surgical lifting procedures in South Korea between 2016 and 2025, testing whether the traditional patient demographic (45+ years) or the younger demographic (20–34 years) showed faster relative growth in search interest; (2) identify procedure-specific and gender-specific patterns of age-demographic change; and (3) contextualize the findings against the global emergence of "prejuvenation" as a consumer category, testing whether Korean age-stratified data support or contradict this narrative.

---

## Methods

### Study Design

This was a cross-sectional time series analysis of age-stratified internet search behavior, reported following the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) guidelines [17]. As the study used publicly available, aggregate, anonymized search data with no individual-level information, institutional review board review was not required.

### Ethical Considerations

This study exclusively analyzed publicly available, aggregate, anonymized search trend data. No individual-level data were collected and no participants were enrolled, so ethical approval and informed consent were not applicable.

### Data Sources

#### Primary: Naver DataLab Search Trend API

Data were collected through the Naver DataLab Search Trend API (endpoint: https://openapi.naver.com/v1/datalab/search) using application credentials obtained through Naver Developers. The study period was January 2016 to December 2025 (120 months), with monthly time resolution. The API returns a relative search volume index (RSV; range, 0–100) that is independently normalized within each query's parameter set (period × age × gender) [15]. This independent normalization means that RSV values from queries with different age or gender parameters cannot be directly compared in absolute terms — a methodological constraint addressed in our analytic design.

#### Secondary: Google Trends

Google Trends data were retrieved for the worldwide region (not filtered to South Korea) for the same study period (January 2016 to December 2025). Three English-language keywords were queried: "prejuvenation," "preventive botox," and "baby botox." These data served as contextual triangulation — documenting the global emergence of prejuvenation-related search terminology against which the Korean age-stratified findings could be compared.

### Keyword Selection

Six keyword groups were defined based on the major non-surgical lifting modalities available in South Korea, validated against Naver autocomplete suggestions and clinical terminology (Table 1). Within each group, keywords sharing the same brand or procedure were combined using the Naver API's keyword array feature, which returns a single aggregated RSV for the group.

**Table 1. Keyword Groups for Naver DataLab Queries**

| Group | Group name | Keywords | Modality |
|-------|-----------|----------|----------|
| 1 | 실리프팅 (Thread lifting) | 실리프팅, 실리프팅시술 | Thread lifting |
| 2 | 울쎄라 (Ulthera) | 울쎄라, 울쎄라피프라임 | HIFU (premium) |
| 3 | 슈링크 (Shrink) | 슈링크, 슈링크유니버스 | HIFU (value) |
| 4 | 써마지 (Thermage) | 써마지, 써마지FLX | RF (premium) |
| 5 | 인모드 (InMode) | 인모드, 인모드포마 | RF (value) |
| 6 | 리프팅시술 (Lifting procedure) | 리프팅시술 | Generic category |

### Age Group Definitions

Naver API age codes 3 through 11 (ages 19–60+ years) were included; codes 1 (0–12 years) and 2 (13–18 years) were excluded as clinically irrelevant. Age codes were grouped into 3 analytic categories: Young (codes 3–5; ages 19–34 years), Middle (codes 6–7; ages 35–44 years), and Traditional (codes 8–11; ages 45–60+ years).

### Data Collection

For each of the 6 keyword groups, API calls were made for each of 10 conditions (all-age plus 9 individual age codes) across 3 gender conditions (all, female, male), yielding 180 primary API calls and a total of 21,274 data points. An additional 3 calls retrieved Google Trends data for the global prejuvenation keywords. Requests were rate-limited to 1.2 seconds or longer between calls. All 180 Naver API calls succeeded. InMode (인모드) had sparse data during its early period (326 of 3600 expected data points missing, primarily in 2016–2017), consistent with minimal pre-launch search volume; all other keywords returned complete 120-month series.

### Statistical Analysis

#### Approach A: Interaction Model (Primary Analysis)

Because Naver RSV is independently normalized within each query's age parameter, direct cross-age comparison of absolute RSV values is not valid. Instead, we compared the rate of change (slope) of RSV over time between age groups using an interaction model:

> RSV_it = β₀ + β₁·Time + β₂·Young + β₃·(Time × Young) + Σγ_m·Month_m + ε_it

where RSV_it is the monthly RSV for a given keyword; Time is months 1 through 120; Young equals 1 for the 20–34-year age group and 0 for the 45+ group; Month_m represents 11 seasonal dummy variables (January as reference); and β₃ is the coefficient of interest. The interpretation depends on the combination of β₁ (baseline trend for the Traditional group) and β₃ (differential growth rate for the Young group):

- β₁ > 0 and β₃ > 0: Broadening — both groups grow, young faster
- β₁ ≤ 0 and β₃ > 0: Displacement — young grows, traditional stagnates
- β₁ > 0 and β₃ < 0: Maturation — both groups grow, traditional faster
- β₁ ≤ 0 and β₃ < 0: Contraction — both decline, young declines faster

Newey-West heteroscedasticity and autocorrelation consistent (HAC) standard errors with 12 lags were used. The model was fitted separately for each keyword group. Multiple comparisons across 6 keyword tests were controlled using the Benjamini-Hochberg false discovery rate (FDR) correction at q < 0.05. Model diagnostics included the Durbin-Watson (DW) statistic and Ljung-Box Q test at 12 lags to assess residual autocorrelation.

#### Approach B: Age-Group Proportional Share (Secondary Analysis)

To estimate the relative contribution of each age group to total search interest, we computed the within-year proportional share:

> Proportion(age_a, year_y) = mean_monthly_RSV(age_a, year_y) / Σ_all_ages mean_monthly_RSV(age, year_y)

The Young-to-Traditional Ratio (YTR = Proportion_Young / Proportion_Traditional) was computed annually and tested for linear trend using ordinary least squares regression on year. A YTR greater than 1.0 indicates youth dominance; a YTR less than 1.0 indicates traditional-demographic dominance. This approach assumes that RSV values from separately queried age groups can be meaningfully compared when averaged over a year — an assumption acknowledged as a limitation.

#### Sensitivity Analyses

Three sensitivity analyses were conducted to assess robustness of the primary Approach A results. First, Prais-Winsten generalized least squares (GLS) estimation with iterative AR(1) correction was applied as an alternative to Newey-West HAC standard errors, to verify that findings were not driven by residual autocorrelation structure. Second, the seasonal dummy variables were replaced with Fourier terms (2 sine-cosine pairs at annual and semiannual frequencies) to confirm that seasonal adjustment specification did not influence the key β₃ estimates. Third, to address the primary threat of differential platform migration by age, we conducted a scenario-based sensitivity analysis in which Young (20–34) RSV values were inflated by correction factors of (1 + r)^(year − 2016), where r = 0.03, 0.05, or 0.07 (representing 3%, 5%, or 7% annual attrition of young users from Naver). The interaction model was re-fitted under each scenario to determine the attrition rate at which the maturation finding would reverse or become nonsignificant.

#### Additional Analyses

1. **Procedure-specific comparison:** β₃ values across 6 keywords, visualized as a forest plot, to identify which modalities show the strongest age-demographic shift.
2. **Gender stratification:** Approach A fitted separately for female and male searchers to test whether the maturation pattern differs by gender. Naver categorizes users by self-reported profile gender; we use "gender" rather than "sex" throughout.
3. **Joinpoint regression:** Segmented linear regression applied to the mean YTR time series to detect inflection points, testing 0, 1, and 2 joinpoints with model selection by Bayesian information criterion (BIC). As a sensitivity check against overfitting with 10 annual data points, the joinpoint analysis was repeated using 120 monthly YTR values.
4. **Google Trends triangulation:** Descriptive analysis of global Google Trends RSV for "prejuvenation," "preventive botox," and "baby botox" to compare the Korean age-shift findings against the global emergence of prejuvenation-related search terms.

All analyses were performed using Python 3.11 (pandas 3.0, statsmodels 0.14, scipy 1.17). Two-sided P < .05 was considered significant unless otherwise specified.

---

## Results

### Overall Temporal Trends

All 6 non-surgical lifting keyword groups showed positive overall growth in search interest between January 2016 and December 2025 (Figure 1). The aggregate time trend coefficient (β₁) was positive for all keywords, ranging from 0.333 per month (Thermage) to 0.705 per month (InMode). The strongest absolute growth was observed for InMode and the generic lifting procedure search term. Google Trends data showed that the global search term "baby botox" increased from a mean RSV of 11.6 in 2016 to 81.0 in 2025, while "prejuvenation" emerged from near-zero RSV before 2019 to a mean of 3.3 in 2025.

### Age Composition Shift

The annual age-group proportional share revealed a progressive expansion of the Traditional (45+ years) demographic and contraction of the Young (20–34 years) demographic over the study period (Figure 2). The Traditional group's proportional share expanded from approximately 25% in 2016 to 38% in 2025, while the Young group's share contracted from approximately 37% to 28%. The Middle (35–44 years) group held the largest share in most years, although the Young group dominated in 2017–2018 and the Traditional group became largest by 2025.

The mean YTR across all keywords declined from 1.42 in 2016 (indicating youth dominance) to 0.77 in 2025 (indicating traditional-demographic dominance), with an overall slope of −0.156 per year (P = .004; R² = 0.66). In 2016, young adults searched at 1.42 times the rate of the traditional group; by 2025, the traditional group searched at 1.30 times the rate of the young group (Table 2). Five of 6 keywords showed a negative YTR slope, with thread lifting (실리프팅) showing the most consistent decline (slope = −0.147 per year; P < .001; R² = 0.88) and the generic lifting term (리프팅시술) showing the largest absolute change (YTR: 2.51 in 2016 to 0.62 in 2025). Only InMode showed a nonsignificant positive trend (slope = +0.025 per year; P = .56).

**Table 2. Young-to-Traditional Ratio (YTR) by Year and Keyword Group**

| Year | Thread lifting | Ulthera | Shrink | Thermage | InMode | Lifting (generic) | Mean |
|------|---------------|---------|--------|----------|--------|-------------------|------|
| 2016 | 1.23 | 0.91 | 1.58 | 2.03 | 0.25 | 2.51 | 1.42 |
| 2017 | 1.55 | 2.17 | 1.68 | 4.51 | 0.82 | 2.05 | 2.13 |
| 2018 | 1.34 | 2.21 | 2.56 | 4.28 | 1.20 | 1.86 | 2.24 |
| 2019 | 0.82 | 2.64 | 2.09 | 3.60 | 1.47 | 1.52 | 2.02 |
| 2020 | 0.82 | 1.79 | 1.57 | 3.04 | 1.41 | 0.95 | 1.60 |
| 2021 | 0.63 | 1.58 | 0.86 | 2.09 | 1.39 | 0.57 | 1.19 |
| 2022 | 0.39 | 1.02 | 0.68 | 1.49 | 1.02 | 0.51 | 0.85 |
| 2023 | 0.30 | 1.29 | 0.66 | 1.11 | 0.95 | 0.57 | 0.81 |
| 2024 | 0.30 | 1.06 | 0.72 | 1.65 | 0.91 | 0.66 | 0.88 |
| 2025 | 0.24 | 0.91 | 0.46 | 1.45 | 0.93 | 0.62 | 0.77 |

*YTR greater than 1.0 indicates the Young group (20–34 years) has a larger proportional share; YTR less than 1.0 indicates the Traditional group (45+ years) has a larger share.*

### Interaction Model Results (Approach A)

The primary analysis revealed a maturation pattern — not broadening — in non-surgical lifting search interest (Table 3; Figure 3). The Time × Young interaction coefficient (β₃) was significantly negative for 3 of 6 keywords after Benjamini-Hochberg FDR correction:

- **Thread lifting** (실리프팅): β₃ = −0.573 (SE, 0.090; 95% CI, −0.750 to −0.396; P_BH < .001)
- **Generic lifting** (리프팅시술): β₃ = −0.558 (SE, 0.107; 95% CI, −0.767 to −0.349; P_BH < .001)
- **HIFU-value** (슈링크): β₃ = −0.267 (SE, 0.076; 95% CI, −0.416 to −0.117; P_BH < .001)

All 3 showed the "Maturation" pattern: β₁ was positive (Traditional group growing over time) and β₃ was significantly negative (Young group growing more slowly than the Traditional group). The remaining 3 keywords — Thermage (β₃ = +0.053; P_BH = .80), Ulthera (β₃ = −0.047; P_BH = .80), and InMode (β₃ = −0.055; P_BH = .80) — showed nonsignificant interaction coefficients, indicating no statistically detectable age-differential growth rate. No keyword showed significant youth acceleration (positive β₃).

**Table 3. Interaction Model Coefficients (Approach A): β₃ (Time × Young) by Keyword**

| Keyword | β₁ (Time) | β₃ (Time × Young) | SE | 95% CI | P | P_BH | Pattern |
|---------|-----------|-------------------|------|--------|---|------|---------|
| Thread lifting | 0.445 | −0.573 | 0.090 | −0.750 to −0.396 | <.001 | <.001 | Maturation |
| Lifting (generic) | 0.535 | −0.558 | 0.107 | −0.767 to −0.349 | <.001 | <.001 | Maturation |
| Shrink (HIFU) | 0.399 | −0.267 | 0.076 | −0.416 to −0.117 | <.001 | <.001 | Maturation |
| Thermage (RF) | 0.333 | +0.053 | 0.101 | −0.145 to +0.251 | .60 | .80 | NS |
| Ulthera (HIFU) | 0.521 | −0.047 | 0.124 | −0.289 to +0.196 | .71 | .80 | NS |
| InMode (RF) | 0.705 | −0.055 | 0.213 | −0.473 to +0.363 | .80 | .80 | NS |

*β₁ represents the monthly growth rate for the Traditional (45+) group. β₃ represents the additional monthly growth rate for the Young (20–34) group relative to the Traditional group. Negative β₃ with positive β₁ indicates both groups grew, but the Traditional group grew faster (maturation pattern). NS indicates nonsignificant. P_BH denotes Benjamini-Hochberg false discovery rate–adjusted P values.*

Notably, all 6 β₃ point estimates were negative or near zero (range, −0.573 to +0.053), and no keyword showed significant youth acceleration. The directionality was consistent even for the 3 nonsignificant keywords, suggesting a universal tendency toward traditional-demographic acceleration that reached statistical significance only for the keywords with the largest effect sizes.

#### Model Diagnostics

Durbin-Watson statistics ranged from 0.45 to 0.80 across models, and Ljung-Box Q(12) tests were significant for all models (all P < .001), indicating residual autocorrelation despite the use of Newey-West HAC standard errors. This motivated the Prais-Winsten GLS sensitivity analysis described below.

#### Sensitivity Analyses

The Prais-Winsten GLS analysis confirmed the maturation finding for thread lifting (β₃ = −0.579; P_BH < .001) and generic lifting (β₃ = −0.547; P_BH < .001). HIFU-value (슈링크) retained a negative β₃ (−0.323) but became nonsignificant after FDR correction (P_BH = .07), reflecting the more conservative standard errors under AR(1) correction. The Fourier term specification produced β₃ estimates virtually identical to the primary analysis (all within 0.001 of the monthly-dummy estimates), confirming that the seasonal adjustment method did not influence the results.

In the platform migration sensitivity analysis, the maturation finding for thread lifting and generic lifting remained statistically significant even under the most extreme assumption of 7% annual attrition of young users from Naver (thread lifting: β₃ = −0.457, P_BH < .001; generic lifting: β₃ = −0.267, P_BH = .04). HIFU-value became nonsignificant at 5% attrition. At the 7% attrition level, Thermage and Ulthera showed significant positive β₃ (youth acceleration), indicating that the direction of the age-differential finding for these keywords is sensitive to assumptions about the magnitude of platform migration. Thread lifting and generic lifting, however, remained robustly negative across all scenarios (Supplementary Table S1).

#### Post-Hoc Power Analysis

For the 3 nonsignificant keywords, the minimum detectable effect size (MDES) at 80% power ranged from 0.28 to 0.60, whereas their observed |β₃| values were only 0.047 to 0.055. Observed power was below 10% for all 3 nonsignificant keywords, indicating that the study was substantially underpowered to detect effects of this magnitude. Approximately 15,000 observations per keyword would be needed to detect the average nonsignificant effect size at 80% power, compared with the approximately 236 available (Supplementary Table S2).

### Gender Stratification

The maturation pattern was present in both genders but was more pronounced among female searchers (Table 4). For thread lifting, the female β₃ was −0.652 (P_BH < .001) compared with the male β₃ of −0.161 (P_BH = .018) — a 4-fold difference in magnitude. For the generic lifting term, the female β₃ was −0.573 (P_BH < .001) compared with the male β₃ of −0.303 (P_BH = .002). The 3 keywords without significant overall maturation (Thermage, Ulthera, InMode) also showed no significant gender-specific patterns.

**Table 4. β₃ (Time × Young) Stratified by Gender**

| Keyword | Female β₃ (SE) | 95% CI | P_BH | Male β₃ (SE) | 95% CI | P_BH |
|---------|---------------|--------|------|-------------|--------|------|
| Thread lifting | −0.652 (0.090) | −0.829 to −0.475 | <.001 | −0.161 (0.062) | −0.283 to −0.040 | .018 |
| Lifting (generic) | −0.573 (0.101) | −0.770 to −0.376 | <.001 | −0.303 (0.085) | −0.470 to −0.135 | .002 |
| Shrink (HIFU) | −0.255 (0.082) | −0.416 to −0.094 | .004 | −0.246 (0.074) | −0.390 to −0.102 | .003 |
| Thermage (RF) | +0.060 (0.098) | −0.132 to +0.252 | .66 | −0.081 (0.113) | −0.303 to +0.140 | .57 |
| Ulthera (HIFU) | −0.065 (0.109) | −0.280 to +0.149 | .66 | −0.011 (0.144) | −0.293 to +0.272 | .94 |
| InMode (RF) | −0.060 (0.216) | −0.483 to +0.362 | .78 | +0.164 (0.201) | −0.230 to +0.558 | .57 |

*SE denotes Newey-West HAC standard error. CI denotes confidence interval. P_BH denotes Benjamini-Hochberg–adjusted P value.*

### Joinpoint Analysis

The 2-joinpoint model was selected as the best fit by BIC (BIC = −11.9 vs 1.5 for 1 joinpoint and 10.3 for no joinpoints; R² = 0.977), identifying inflection points at 2018 and 2022 (Figure 4). This revealed a 3-phase trajectory:

- **Phase 1 (2016–2018):** YTR rose from 1.42 to 2.24 (annual slope = +0.42). Young adults initially dominated the growth of search interest.
- **Phase 2 (2018–2022):** YTR fell sharply from 2.24 to 0.85 (annual slope = −0.38; slope change from Phase 1: −0.80; P < .001). The traditional demographic accelerated its search growth, overtaking the young group. YTR crossed parity (1.0) between 2021 and 2022.
- **Phase 3 (2022–2025):** YTR stabilized at 0.77 to 0.88 (annual slope = −0.01; slope change from Phase 2: +0.37; P = .001). The age composition reached a new equilibrium with the traditional group holding a larger relative share.

The first inflection point at 2018 predates the COVID-19 pandemic by approximately 2 years, indicating that the maturation process was already underway before the pandemic. The monthly-level sensitivity analysis (120 data points) selected the same 2-joinpoint structure, with inflection points at 2018.5 and 2022.0, confirming that the annual results were not an artifact of overfitting with 10 data points.

### Google Trends: Global Context and Dissociation

Google Trends data showed exponential global growth of prejuvenation-related search terms: "baby botox" increased from a mean RSV of 11.1 (2016) to 80.6 (2025), while "prejuvenation" emerged from 0.0 (2016) to 3.3 (2025). These terms suggest a growing global narrative of younger consumers entering the aesthetic market.

However, the Korean Naver age-stratified data showed the opposite of what the prejuvenation narrative would predict: the traditional 45+ demographic, not the young, showed the dominant growth trajectory. This dissociation between the global prejuvenation narrative (visible in aggregate Google Trends data) and the actual age-stratified search behavior (visible only through Naver DataLab) represents a key finding. It demonstrates that age-agnostic search trend data can produce misleading conclusions about the demographic composition of health information-seeking behavior.

---

## Discussion

### Principal Findings

This study provides, to our knowledge, the first population-level quantification of age-demographic dynamics in non-surgical lifting search interest. Three of 6 keywords showed significantly faster growth among the traditional 45+ demographic than the young 20–34 group (β₃ range, −0.27 to −0.57; all P_BH < .001), while no keyword showed significant youth acceleration. Joinpoint analysis revealed a 3-phase trajectory — youth-dominated early adoption (2016–2018), rapid traditional-demographic overtake (2018–2022), and stabilization (2022–2025) — consistent with an innovation diffusion trajectory rather than the widely assumed prejuvenation narrative of demographic broadening into younger consumers.

### Innovation Diffusion: From Early Adopters to Mainstream Market

These findings align with the Diffusion of Innovations framework [7]. Young adults aged 20 to 34 years, as digital-native, appearance-conscious early adopters, drove initial search interest during a period when non-surgical lifting awareness was expanding rapidly in Korean consumer culture. As awareness diffused to the broader population, the traditional patient base (45+ years) — the demographic with the strongest clinical indication for skin laxity — expanded its search behavior more rapidly, reflecting progression from the "early majority" to the "late majority" adoption phase.

This reframes the prevailing narrative. The question is not whether non-surgical lifting "went younger" but whether the market followed a typical innovation diffusion curve in which early youth interest served as a leading indicator of subsequent mainstream adoption by the clinically indicated population. Our data support the latter interpretation.

We acknowledge that the innovation diffusion framework applies most directly to procedures that were genuinely novel during the study period, such as Shrink (슈링크, launched approximately 2018) and InMode (Korean market entry approximately 2018). Established devices such as Thermage (2002) and Ulthera (2009) had already completed their initial diffusion cycle before 2016. Notably, these established brands showed nonsignificant β₃ — consistent with a stable, post-diffusion age composition — while the newer entrants and the category-level search term showed the strongest maturation signals. An alternative, complementary explanation is population aging: South Korea's rapid demographic aging — among the fastest in the Organisation for Economic Co-operation and Development, with the proportion of the population aged 65 years or older rising from 13.2% in 2016 to 19.2% in 2025 [24] — may independently increase the pool of older consumers seeking skin-laxity treatments, contributing to the observed Traditional-demographic growth.

### Procedure-Specific Patterns

The maturation effect was not uniform across procedures. Thread lifting (실리프팅) showed the strongest maturation effect (β₃ = −0.573), consistent with its early positioning as a trend-driven, social media–promoted procedure among younger consumers that subsequently diffused to the traditional demographic [18]. The generic search term (리프팅시술) showed a similarly strong maturation effect (β₃ = −0.558), reflecting the overall market dynamic. HIFU-value devices (슈링크) showed moderate maturation (β₃ = −0.267), consistent with their positioning as an accessible entry point that eventually reached older consumers.

In contrast, Thermage (RF premium), Ulthera (HIFU premium), and InMode (RF value) showed no significant age-differential growth. The nonsignificant results for these keywords should be interpreted cautiously: absence of significance does not imply absence of effect. All 6 β₃ point estimates were negative or near zero, and the 3 nonsignificant keywords had smaller effect sizes (|β₃| < 0.06) and wider confidence intervals — particularly InMode (SE = 0.213), reflecting its sparser early-period data. Post-hoc power analysis confirmed this interpretation: the minimum detectable effect size at 80% power was 0.28–0.60 for the nonsignificant keywords, whereas their observed |β₃| values were only 0.05–0.06 — approximately 5- to 10-fold below the detection threshold. Detecting an effect of this magnitude would require approximately 15,000 observations per keyword, compared with the ~236 available. Substantively, Thermage and Ulthera were established brands before the study period, potentially attracting their clinically indicated older demographic from the beginning, while InMode's recent market entry and broad-spectrum marketing may have simultaneously reached all age groups [19].

These findings have clinical implications. Practitioners should recognize that while younger patients may drive initial awareness of novel procedures, the sustained demand base for non-surgical lifting is the traditional 45+ population — the demographic with the greatest physiological indication for these interventions.

### Gender-Specific Patterns

The maturation effect was 2- to 4-fold stronger among female searchers than among male searchers for the significantly affected keywords. This is consistent with the observation that women aged 45 years and older represent the core clinical demographic for non-surgical lifting [1] and suggests that the traditional-demographic acceleration was driven primarily by older women entering the search market. Male search behavior showed a more modest maturation pattern, potentially reflecting the smaller overall volume of male aesthetic procedure searches.

### Temporal Confounders: COVID-19 and Platform Migration

Two temporal confounders warrant discussion. First, the joinpoint at 2018 predates the COVID-19 pandemic by approximately 2 years, indicating that the maturation process was endogenous to the lifting market. However, the sharp YTR decline between 2020 and 2022 may have been amplified by the "Zoom face" phenomenon — heightened awareness of facial aging during video conferencing — which may have disproportionately motivated older adults to seek lifting procedures [20,21].

Second, differential platform migration by age represents the most important alternative explanation for the declining YTR. During 2018 to 2025, younger Korean internet users increasingly migrated aesthetic information-seeking from Naver to Google, YouTube, Instagram, and TikTok [22,23], potentially causing their search interest to be undercounted on Naver. Our scenario-based sensitivity analysis provides quantitative bounds: even assuming 7% annual attrition of young users (cumulative 1.84× correction by 2025), thread lifting and generic lifting retained significant maturation signals. HIFU-value became nonsignificant at 5% attrition, and at the extreme 7% scenario, Thermage and Ulthera reversed to show significant youth acceleration — demonstrating that the sensitivity of individual keywords varies substantially with platform migration assumptions. The robustness of the 2 strongest keywords (thread lifting, generic lifting) across all scenarios suggests that these maturation signals reflect genuine demographic dynamics, while the results for other keywords are more equivocal.

### Methodological Contribution: The Dissociation Between Google Trends and Naver DataLab

Beyond the substantive findings, this study demonstrates a critical methodological point. Google Trends showed exponential global growth in "prejuvenation" and "baby botox" searches, supporting the narrative that aesthetic interest is expanding into younger demographics. However, when actual age-stratified search data are examined through Naver DataLab — the only platform worldwide that provides such data — the opposite pattern emerges for non-surgical lifting.

This dissociation cautions against interpreting aggregate search trend increases as evidence of demographic broadening and validates the unique contribution of age-stratified search analysis. The method is transferable to any health topic where age-specific information-seeking is relevant, including fertility, chronic disease management, mental health, and substance use.

### Limitations

Several limitations should be considered. First, differential platform migration by age — discussed in detail above — represents the most important confound. The observed maturation pattern likely reflects a combination of genuine market dynamics and platform-specific demographic shifts whose precise contributions cannot be fully disaggregated. Sensitivity analysis confirmed robustness for thread lifting and generic lifting even under extreme assumptions, but Thermage and Ulthera reversed to show youth acceleration at 7% annual attrition, and HIFU-value became nonsignificant at 5%. Second, Naver RSV is independently normalized within each query's age parameter; the proportional share analysis (Approach B) relies on an assumption of comparable RSV scaling across age groups, while Approach A addresses this by comparing within-age temporal trends. Third, search interest does not equate to procedure uptake. However, prior studies have demonstrated moderate-to-strong correlations between search RSV and actual healthcare utilization for aesthetic procedures [10,12], and Naver search behavior directly feeds the clinic-patient acquisition pathway in Korea [16], lending clinical relevance to these findings even as a proxy measure. Fourth, keywords may not capture all relevant search behavior, including social media searches and clinic-specific terminology. Fifth, single-country primary data limit direct generalizability, although South Korea ranks among the top 5 countries globally for per-capita aesthetic procedure volume [1], originated several of the devices studied, and has the most mature non-surgical lifting market in Asia. Sixth, the study cannot distinguish patient-searchers from information-seekers. Finally, the innovation diffusion framework applies most directly to procedures that were novel during the study period; established devices (Thermage, Ulthera) had already completed their initial diffusion cycle, and their nonsignificant β₃ values are consistent with this caveat.

### Conclusions

Non-surgical lifting search interest in South Korea followed an innovation diffusion trajectory rather than the widely assumed prejuvenation pattern: young adults were early adopters, but the traditional 45+ demographic grew faster and overtook them by 2022. The dissociation between this age-stratified finding and the global prejuvenation narrative visible in aggregate Google Trends data underscores the critical importance — and current rarity — of age-stratified analysis in infodemiology. Although differential platform migration by age remains a significant confound, sensitivity analyses confirmed the robustness of the core finding for the strongest-signal keywords. Naver DataLab's globally unique age-stratified API represents an underutilized resource for health information-seeking research.

---

## Acknowledgments

None.

## Conflicts of Interest

None declared.

## Data Availability

The raw Naver DataLab RSV dataset, Google Trends data, processed analytic datasets, and all analysis code are available in the project repository.

---

## References

1. International Society of Aesthetic Plastic Surgery. ISAPS International Survey on Aesthetic/Cosmetic Procedures Performed in 2023. ISAPS; 2024.
2. Kim HJ, Park JH. Non-surgical facial rejuvenation in Korea: current trends and devices. *Arch Aesthetic Plast Surg*. 2023;29(1):1-8.
3. Fabi SG, Massaki A, Eimpunth S, Pogoda J, Goldman MP. Evaluation of microfocused ultrasound with visualization for lifting, tightening, and wrinkle reduction of the décolletage. *J Am Acad Dermatol*. 2013;69(6):965-971.
4. American Society for Dermatologic Surgery. ASDS Consumer Survey on Cosmetic Dermatologic Procedures. ASDS; 2024.
5. Keaney T. Emerging trends in nonsurgical aesthetics: the rise of prejuvenation. *J Drugs Dermatol*. 2018;17(9):980-986.
6. Gupta V, Kede MPV, Fabi SG. Global prejuvenation: a narrative review of the current landscape. *Dermatol Surg*. 2023;49(Suppl 2):S44-S50.
7. Rogers EM. *Diffusion of Innovations*. 5th ed. Free Press; 2003.
8. Eysenbach G. Infodemiology and infoveillance: framework for an emerging set of public health informatics methods to analyze search, communication and publication behavior on the Internet. *J Med Internet Res*. 2009;11(1):e11.
9. Eysenbach G. Infodemiology and infoveillance tracking online health information and cyberbehavior for public health. *Am J Prev Med*. 2011;40(5 Suppl 2):S154-S158.
10. Ward B, Ward M, Paskhover B, et al. Google trends as a resource for informing plastic surgery marketing decisions. *Aesthetic Plast Surg*. 2018;42(2):598-602.
11. Kang GW, Son H, Butterworth M. Google trends analysis of dermal filler: a 5-year study. *J Cosmet Dermatol*. 2022;21(12):6867-6873.
12. Ramanadham SR, Mapula S, Costa CR, et al. Using big data (Google Trends) to assess public interest in cosmetic surgery procedures. *Aesthet Surg J*. 2020;40(4):NP165-NP170.
13. Shen TS, Driscoll DA, Islam W, Bovonratwet P, Haas EM, Su EP. Modern internet search analytics and total joint arthroplasty: what are patients asking and reading online? *J Arthroplasty*. 2021;36(4):1224-1231.
14. Mavragani A, Ochoa G, Tsagarakis KP. Assessing the methods, tools, and statistical approaches in Google Trends research: systematic review. *J Med Internet Res*. 2018;20(11):e270.
15. Naver Corporation. Naver DataLab Search Trend API documentation. Accessed December 2025. https://developers.naver.com/docs/serviceapi/datalab/search/search.md
16. StatCounter. Search engine market share Republic of Korea. Accessed January 2026. https://gs.statcounter.com/search-engine-market-share/all/south-korea
17. von Elm E, Altman DG, Egger M, Pocock SJ, Gøtzsche PC, Vandenbroucke JP. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. *Ann Intern Med*. 2007;147(8):573-577.
18. Ko HJ, Kim TG, Kim MK. Thread lifting: a minimally invasive surgical technique. *J Cosmet Dermatol*. 2022;21(10):4426-4433.
19. Dayan SH, Humphrey S, Jones DH, et al. Overview of the aesthetic use of radiofrequency devices. *Aesthet Surg J*. 2023;43(Suppl 2):S1-S10.
20. Rice SM, Siegel JA, Libby T, Graber E, Kourosh AS. Zooming into cosmetic procedures during the COVID-19 pandemic: the provider's perspective. *Int J Womens Dermatol*. 2021;7(2):213-216.
21. Dhanda AK, Leverant A, Leshchuk K, et al. A Google Trends analysis of facial cosmetic surgery interest during the COVID-19 pandemic. *Aesthet Surg J*. 2022;42(4):NP237-NP244.
22. Korea Internet & Security Agency. 2024 Internet Usage Survey. KISA; 2024.
23. Wiseapp. Search engine app usage statistics by age group in South Korea. Wiseapp Report; 2024.
24. Statistics Korea. Population Projections for Korea: 2020–2070. Statistics Korea; 2024.

---

## Figures

### Figure 1
Monthly all-age relative search volume (RSV) for 6 non-surgical lifting keyword groups on Naver (colored lines, left axis) with global Google Trends RSV for "baby botox" and "prejuvenation" overlaid (gray lines, right axis), January 2016 to December 2025. The shaded area indicates the initial COVID-19 impact period (March–June 2020). All 6 Naver keyword groups showed overall growth over the study period.

### Figure 2
Annual age-group proportional share of non-surgical lifting search interest on Naver (all procedures combined), 2016 to 2025. The stacked area chart shows the Traditional (45+ years; blue), Middle (35–44 years; orange), and Young (20–34 years; red) proportional shares. The Traditional group's share expanded from approximately 25% to 38%, while the Young group contracted from approximately 37% to 28%.

### Figure 3
Forest plot of the Time × Young interaction coefficient (β₃) for each non-surgical lifting keyword. Red markers indicate keywords with statistically significant β₃ after Benjamini-Hochberg correction (false discovery rate < 0.05); gray markers indicate nonsignificant results. All 6 point estimates lie to the left of zero (indicating traditional-demographic acceleration), with 3 reaching statistical significance. Error bars represent 95% CIs.

### Figure 4
Joinpoint regression of the mean Young-to-Traditional Ratio (YTR) across all keywords, 2016 to 2025. Blue dots represent observed annual YTR values; the red line represents the best-fit 2-joinpoint model (joinpoints at 2018 and 2022; R² = 0.977). The horizontal gray line indicates YTR = 1.0 (parity). Three phases are visible: youth-dominated early adoption (2016–2018, rising YTR), rapid traditional-demographic overtake (2018–2022, falling YTR), and stabilization (2022–2025, flat YTR below parity).

---

## Supplementary Materials

**Supplementary Table S1.** Platform migration sensitivity analysis: β₃ (Time × Young) under simulated young-user attrition scenarios (3%, 5%, 7% annual Naver attrition).

**Supplementary Table S2.** Post-hoc power analysis: minimum detectable effect size at 80% power, observed power, and required sample size for nonsignificant keywords.

**Supplementary Table S3.** Prais-Winsten GLS sensitivity analysis: β₃ estimates with AR(1)-corrected standard errors.

**Supplementary Table S4.** Fourier term sensitivity analysis: β₃ estimates with harmonic seasonal adjustment.

**Supplementary Figure S1.** Young (20–34) vs Traditional (45+) RSV time series by individual procedure keyword (6-panel display).

**Supplementary Figure S2.** Google Trends RSV for global prejuvenation-related search terms ("prejuvenation," "preventive botox," "baby botox"), 2016–2025.

---

## Abbreviations

API: application programming interface
AR: autoregressive
BIC: Bayesian information criterion
DW: Durbin-Watson
FDR: false discovery rate
GLS: generalized least squares
GT: Google Trends
HAC: heteroscedasticity and autocorrelation consistent
HIFU: high-intensity focused ultrasound
MDES: minimum detectable effect size
OLS: ordinary least squares
RF: radiofrequency
RSV: relative search volume
STROBE: Strengthening the Reporting of Observational Studies in Epidemiology
YTR: Young-to-Traditional Ratio
