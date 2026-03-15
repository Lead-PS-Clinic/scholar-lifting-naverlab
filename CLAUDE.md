# Non-Surgical Lifting Goes Younger: The Broadening of Public Interest into Younger Demographics in South Korea — An Age-Stratified Infodemiology Study, 2016–2025

## CLAUDE.md — Project Guide for Claude Code

---

## 1. Project Overview

This study uses the age-stratified search trend API uniquely available from Naver DataLab to determine whether public interest in non-surgical facial lifting procedures in South Korea has broadened into younger age groups between 2016 and 2025 — that is, whether younger demographics have increasingly entered a market traditionally dominated by older consumers, rather than a zero-sum shift from old to young. No equivalent age-stratified search data exists from any other major search engine worldwide, including Google Trends, Baidu Index, or Yandex Wordstat.

**PI:** Joonho Lim, MD — ORCID 0000-0002-4556-1536
**Target journal:** JMIR Dermatology (IF 3.7)

---

## 2. IMRD

### INTRODUCTION

#### P1: The rise of non-surgical lifting

Non-surgical facial lifting has become one of the fastest-growing segments of the global aesthetic medicine market. High-intensity focused ultrasound (HIFU), radiofrequency (RF) devices, and absorbable thread lifting offer facial tightening and contouring without surgical incision. The International Society of Aesthetic Plastic Surgery (ISAPS) reported that nonsurgical skin tightening procedures increased globally by over 40% between 2019 and 2023. South Korea, one of the world's largest markets for aesthetic procedures, has been at the forefront of this expansion, with multiple domestically developed devices (Shurink, InMode, Oligio) achieving widespread adoption alongside international brands (Ultherapy, Thermage).

#### P2: The prejuvenation phenomenon — anecdotal but unquantified

Traditionally, non-surgical lifting was sought primarily by patients aged 45 and older as an alternative to surgical facelift. However, practitioners and industry observers have noted a demographic broadening: patients in their late 20s and 30s are increasingly entering this market as new consumers seeking preventive interventions — a trend variously termed "prejuvenation," "preventive aesthetics," or, in Korean consumer culture, "슬로우에이징" (slow aging). Importantly, this appears to represent an expansion of the consumer base into younger demographics rather than a displacement of older patients, who continue to seek these procedures. This broadening carries important implications for clinical practice (younger patients have different motivations, expectations, and risk profiles), for the aesthetic device market (pricing, marketing, device design for a wider age range), and for public health (younger patients accumulating longer exposure histories to repeated energy-based treatments). Despite its significance, this demographic broadening has not been quantified at the population level.

#### P3: The limitation of existing infodemiology tools

Infodemiology — the study of online health information-seeking behavior — has become a standard method for tracking public interest in aesthetic procedures. Google Trends (GT) has been used extensively to analyze temporal patterns in searches for botulinum toxin, dermal fillers, blepharoplasty, and other procedures. However, GT does not provide age-stratified data: it is impossible to determine whether a rise in search volume for a lifting procedure is driven by younger or older consumers. This is a critical limitation for the present research question, which concerns a broadening of interest into younger demographics — a pattern invisible when only aggregate volume is observed. No other major global search engine trend tool provides public age-stratified search APIs.

#### P4: Naver DataLab — a unique data source

Naver, the dominant search engine in South Korea (~56% market share), provides a public Search Trend API through Naver DataLab that returns relative search volume (RSV) indices stratified by 11 age bins (0–12 through 60+), gender (male/female), and device type (PC/mobile). This makes Naver DataLab the only major search trend platform worldwide that enables population-level, age-stratified analysis of health information-seeking behavior. Meanwhile, GT data for global English-language keywords can provide contextual evidence of a parallel worldwide trend — specifically, the emergence of terms such as "prejuvenation" and "preventive botox" — that cannot be age-stratified but that corroborate the hypothesized broadening of aesthetic interest into younger demographics.

#### P5: Study aim

This study aimed to (1) determine whether public search interest in non-surgical lifting procedures in South Korea has broadened into younger age groups between 2016 and 2025, distinguishing between expansion of the consumer base and displacement of traditional demographics, (2) characterize procedure-specific and gender-specific patterns of this demographic broadening, and (3) contextualize the findings within the global prejuvenation trend using Google Trends data.

---

### METHODS

#### Study design

Cross-sectional time series analysis of age-stratified internet search behavior, reported following STROBE guidelines. As the study used publicly available, aggregate, anonymized search data with no individual-level information, institutional review board review was not required.

#### Data sources

**Primary — Naver DataLab Search Trend API:**
- Endpoint: https://openapi.naver.com/v1/datalab/search
- Authentication: Naver Developers application (Client ID + Client Secret)
- Period: January 2016 to December 2025 (120 months)
- Time unit: monthly
- Stratification: age group (codes 3–11, i.e. ages 19–60+), gender (all/female/male), device (all)
- Output: relative search volume (RSV) index, 0–100, independently normalized within each query's parameter set (period × age × gender)

**Secondary — Google Trends:**
- Region: Worldwide (not filtered to Korea)
- Period: January 2016 to December 2025
- Keywords: "prejuvenation", "preventive botox", "baby botox"
- Purpose: contextual triangulation — demonstrating a parallel global trend toward younger-demographic aesthetic interest. GT cannot provide age stratification but can show the temporal emergence of prejuvenation-related search terms globally.

#### Keyword selection

Six keyword groups were defined based on the major non-surgical lifting modalities available in South Korea, validated against Naver autocomplete suggestions and clinical terminology:

| Group | groupName | Keywords array | Modality |
|-------|-----------|---------------|----------|
| 1 | 실리프팅 | 실리프팅, 실리프팅시술 | Thread lifting |
| 2 | 울쎄라 | 울쎄라, 울쎄라피프라임 | HIFU (premium) |
| 3 | 슈링크 | 슈링크, 슈링크유니버스 | HIFU (value) |
| 4 | 써마지 | 써마지, 써마지FLX | RF (premium) |
| 5 | 인모드 | 인모드, 인모드포마 | RF (value) |
| 6 | 리프팅시술 | 리프팅시술 | Generic category |

Within each group, keywords sharing the same brand/procedure were combined using the Naver API's keyword array feature, which returns a single aggregated RSV for the group.

#### Age group definitions

Naver API age codes and analytic grouping:

| API code | Age range | Analytic group |
|----------|-----------|---------------|
| 1 | 0–12 | Excluded |
| 2 | 13–18 | Excluded |
| 3 | 19–24 | Young (20–34) |
| 4 | 25–29 | Young (20–34) |
| 5 | 30–34 | Young (20–34) |
| 6 | 35–39 | Middle (35–44) |
| 7 | 40–44 | Middle (35–44) |
| 8 | 45–49 | Traditional (45+) |
| 9 | 50–54 | Traditional (45+) |
| 10 | 55–59 | Traditional (45+) |
| 11 | 60+ | Traditional (45+) |

#### Data collection

For each of the 6 keyword groups, API calls were made for each of 10 conditions (all-age + 9 individual age codes) × 3 gender conditions (all/female/male), yielding 180 primary API calls. An additional 3 calls retrieved GT data for the global prejuvenation keywords. Requests were rate-limited to ≥1.2 seconds between calls.

#### Statistical analysis

**Approach A (primary analysis) — Age-group growth rate comparison:**

Because Naver RSV is independently normalized within each query's age parameter, direct cross-age comparison of absolute RSV values is not valid. Instead, we compared the rate of change (slope) of RSV over time between age groups using an interaction model:

RSV_it = β₀ + β₁·Time + β₂·Young + β₃·(Time × Young) + Σγ_m·Month_m + ε_it

where RSV_it is the monthly RSV for a given keyword; Time is months 1–120; Young is 1 for the 20–34 age group and 0 for the 45+ group; Month_m are 11 seasonal dummies; and β₃ is the coefficient of interest. A positive β₃ indicates that search interest grew faster in the younger group. Critically, the interpretation depends on the combination of β₁ (baseline trend for the Traditional group) and β₃: if both β₁ > 0 and β₃ > 0, this constitutes a broadening of interest — both age groups grew, but younger consumers entered the market at a faster rate. If β₁ ≤ 0 and β₃ > 0, this would indicate a displacement pattern where younger interest grew while older interest stagnated or declined. Newey-West heteroscedasticity and autocorrelation consistent (HAC) standard errors with 12 lags were used. The model was fitted separately for each keyword group. Multiple comparisons across 6 keyword tests were controlled using the Benjamini-Hochberg false discovery rate (FDR) correction at q < 0.05.

**Approach B (secondary analysis) — Age-group proportional share:**

To estimate the relative contribution of each age group to total search interest, we computed the within-year proportional share:

Proportion(age_a, year_y) = mean_monthly_RSV(age_a, year_y) / Σ_all_ages mean_monthly_RSV(age, year_y)

The Young-to-Traditional Ratio (YTR = Proportion_Young / Proportion_Traditional) was computed annually and tested for linear trend using ordinary least squares regression on year.

Note: This approach assumes that RSV values from separately queried age groups can be meaningfully compared when averaged over a year. This assumption is acknowledged as a limitation, and Approach B results are interpreted as supportive rather than definitive.

**Additional analyses:**
1. Procedure-specific comparison: β₃ values across 6 keywords, visualized as a forest plot, to identify which modalities show the strongest demographic broadening.
2. Gender stratification: Approach A fitted separately for female and male searchers to test whether the broadening into younger demographics is more pronounced in women.
3. Joinpoint regression: Segmented linear regression applied to the YTR time series to detect inflection points (e.g., COVID-19-related acceleration).
4. Google Trends triangulation: descriptive analysis of global GT trends for "prejuvenation", "preventive botox", and "baby botox" to contextualize the Korean findings within a global generational shift.

**Model diagnostics:**
- Durbin-Watson test and Ljung-Box test (12 lags) for residual autocorrelation
- Prais-Winsten GLS as sensitivity analysis if DW < 1.5
- Fourier terms (2 sine-cosine pairs) as sensitivity alternative to monthly dummies

All analyses were performed using Python 3.11 (pandas, statsmodels, scipy). Two-sided P < 0.05 was considered significant unless otherwise specified.

---

### RESULTS (anticipated structure)

#### R1: Overall temporal trends
- **Figure 1:** Monthly all-age RSV for 6 Naver keyword groups (2016–2025), with GT global "prejuvenation" RSV overlaid on secondary axis
- Descriptive: which procedures grew, which declined, overall market trajectory

#### R2: Age composition shift — the key finding
- **Figure 2 (key figure):** Annual age-group proportional share, stacked area chart — all keywords combined
- **Table 1:** Young-to-Traditional Ratio (YTR) by year and keyword, with linear trend P

#### R3: Interaction model results
- **Table 2:** β₃ (Time × Young interaction) for each keyword, with SE, 95% CI, P, and BH-adjusted P
- **Figure 3:** Forest plot of β₃ across 6 keywords
- Interpretation: which procedures show statistically significant faster growth in the young group?

#### R4: Gender stratification
- **Table 3:** β₃ by gender (female vs male) for each keyword
- Is the age shift more pronounced in women?

#### R5: Joinpoint analysis
- **Figure 4:** YTR time series with joinpoint regression
- Did the demographic shift accelerate after a specific time point (COVID-19, 2020)?

#### R6: Google Trends global context
- GT "prejuvenation" RSV shows [expected: near-zero before 2019, exponential growth 2020–2025]
- GT "preventive botox" and "baby botox" show similar emergence
- Temporal alignment with the Korean Naver age shift → supports interpretation as part of a global generational trend

---

### DISCUSSION (anticipated structure)

#### D1: Principal findings
- "Between 2016 and 2025, search interest in non-surgical lifting grew across all age groups, but significantly faster among the 20–34 age group than the 45+ group (β₁ = X [Traditional trend], β₃ = Y [additional Young growth], P = Z)."
- The positive β₁ confirms that the traditional patient base (45+) continued to grow, while the positive β₃ demonstrates that younger consumers entered the market at a disproportionately faster rate — a broadening of the consumer base rather than a zero-sum displacement.
- This quantifies, for the first time, a demographic expansion that has been widely observed clinically but never measured at the population level.

#### D2: The prejuvenation phenomenon in global context
- GT data show that "prejuvenation" emerged as a global search term around 2019–2020, with exponential growth since
- The Korean Naver data demonstrate that this is not merely a Western phenomenon but is measurable in the world's most active aesthetic market
- Cultural drivers in Korea: normalization of aesthetic procedures at younger ages, "슬로우에이징" as a lifestyle category, social media influence, and competitive appearance culture

#### D3: Procedure-specific patterns — clinical implications
- If thread lifting shows the strongest broadening into younger demographics: consistent with lower cost, shorter downtime, and Instagram-friendly immediate results appealing to a younger consumer profile
- If HIFU retains a predominantly older demographic: consistent with clinical indication for established laxity rather than prevention
- If RF devices show intermediate broadening: consistent with "maintenance" positioning that appeals across age ranges
- Implications for practitioners: consultation approach, expectation management, and long-term treatment planning should account for the expanding age range of patients, with younger patients requiring different education about realistic expectations, maintenance protocols, and long-term safety

#### D4: Methodological contribution
- Naver DataLab's age-stratified API is globally unique — this is the first academic study to exploit this capability for health research
- The method is transferable to any health topic where age-specific information-seeking is relevant (fertility, chronic disease, mental health, substance use)
- Demonstrates that non-English, non-Google search data can fill critical methodological gaps in infodemiology

#### D5: COVID-19 as an accelerator
- If joinpoint detects inflection at 2020–2021: consistent with "Zoom face" effect, lockdown introspection, and deferred social spending redirected to self-improvement
- Published GT studies have shown post-COVID acceleration in aesthetic procedure interest; our age-stratified data add the novel finding that this acceleration was differentially concentrated in younger demographics, suggesting that the pandemic may have accelerated the broadening of the non-surgical lifting market into a younger consumer base

#### D6: Limitations
- Naver RSV is relative and independently normalized per query → cross-age absolute comparison is not directly valid (addressed by Approach A's within-age temporal comparison)
- Naver user demographics may not perfectly represent the general population by age; younger users may disproportionately use Google, Instagram, or TikTok for aesthetic information
- Search interest ≠ procedure uptake: searching does not confirm that the person underwent the procedure
- Keywords may not capture all relevant search behavior (e.g., social media searches, clinic-specific terms)
- The proportional share method (Approach B) relies on an assumption of comparable RSV scaling across age groups
- Single-country primary data: findings may not directly generalize, though GT global data provide supportive context and Korea's position as a global aesthetic leader provides external validity
- Cannot distinguish patient-searchers from information-seekers (journalists, students, practitioners)

#### D7: Conclusion
- Public interest in non-surgical lifting procedures in South Korea has broadened into younger demographics, with the 20–34 age group showing significantly faster growth in search interest than the traditional 45+ patient base, while interest among older consumers also continued to grow
- This represents an expansion of the consumer base rather than a displacement, quantified for the first time using Naver DataLab's globally unique age-stratified search API
- The trend parallels the global emergence of "prejuvenation" as a consumer category and has direct implications for clinical practice, patient education, and the aesthetic device market
- Naver DataLab represents an underutilized but powerful data source for infodemiology research that addresses a fundamental limitation of Google Trends

---

## 3. Data Collection Design

### 3.1 Naver API calls

6 keyword groups × (1 all-age + 9 age codes) × 3 genders = 180 calls

```python
KEYWORDS = [
    {"groupName": "실리프팅", "keywords": ["실리프팅", "실리프팅시술"]},
    {"groupName": "울쎄라", "keywords": ["울쎄라", "울쎄라피프라임"]},
    {"groupName": "슈링크", "keywords": ["슈링크", "슈링크유니버스"]},
    {"groupName": "써마지", "keywords": ["써마지", "써마지FLX"]},
    {"groupName": "인모드", "keywords": ["인모드", "인모드포마"]},
    {"groupName": "리프팅시술", "keywords": ["리프팅시술"]},
]
AGE_CODES = [None, '3','4','5','6','7','8','9','10','11']
GENDERS = [None, 'f', 'm']
```

### 3.2 Google Trends calls

**GT — Global prejuvenation trend (Worldwide):**
- "prejuvenation", "preventive botox", "baby botox"
- geo="" (Worldwide), timeframe="2016-01-01 2025-12-31"

---

## 4. Figures & Tables Summary

| Item | Content | Role |
|------|---------|------|
| Figure 1 | Naver all-age RSV by keyword + GT global "prejuvenation" overlay | Context |
| Figure 2 | Annual age-group proportional share, stacked area | **Key figure** |
| Figure 3 | β₃ forest plot by keyword | Procedure comparison |
| Figure 4 | Joinpoint regression on YTR | Inflection detection |
| Table 1 | YTR by year and keyword | Approach B summary |
| Table 2 | β₃ interaction coefficients by keyword | Primary result |
| Table 3 | β₃ by gender | Gender stratification |

Supplementary: full RSV dataset, individual keyword × age time series, Prais-Winsten sensitivity, Fourier sensitivity

---

## 5. File Structure

```
lifting-age-shift/
├── CLAUDE.md
├── data/
│   ├── raw/
│   │   ├── naver_rsv_all.csv
│   │   └── gt_global_prejuvenation.csv
│   └── processed/
│       ├── rsv_by_keyword_agegroup_month.csv
│       ├── annual_age_proportions.csv
│       └── ytr_timeseries.csv
├── analysis/
│   ├── 01_collect_naver.py
│   ├── 02_collect_gt.py
│   ├── 03_process.py
│   ├── 04_approach_a.py
│   ├── 05_approach_b.py
│   ├── 06_joinpoint.py
│   ├── 07_gender.py
│   └── 08_figures.py
├── output/
│   ├── figures/
│   └── tables/
└── manuscript/
    └── draft.md
```

---

## 6. Technical Notes

- Naver RSV: independently normalized per query (period × age × gender) → cross-age absolute comparison invalid → use Approach A (slope comparison)
- API daily limit: 1,000 calls, ≥1.2s between requests
- "슈링크유니버스" launched ~2022, "울쎄라피프라임" ~2023 → zero RSV before launch, handled by keyword array aggregation
- GT pytrends may require retries due to rate limiting
- All figures: 300 DPI, Korean font (NanumGothic or system fallback)
- Environment variables: NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
