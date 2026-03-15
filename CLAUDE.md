# From Early Adopters to Mainstream Market: The Maturation of Non-Surgical Lifting Search Interest Toward Older Demographics in South Korea — An Age-Stratified Infodemiology Study Using Naver DataLab, 2016–2025

## CLAUDE.md — Project Guide for Claude Code

---

## 1. Project Overview

This study uses the age-stratified search trend API uniquely available from Naver DataLab to characterize how the age composition of public search interest in non-surgical facial lifting procedures in South Korea shifted between 2016 and 2025. The data reveal a maturation pattern: young adults (20–34) were disproportionate early adopters of lifting-related search behavior, but the traditional 45+ demographic showed significantly faster sustained growth, overtaking the younger group by 2022 — consistent with an innovation diffusion trajectory rather than the popularly assumed "prejuvenation" broadening. No equivalent age-stratified search data exists from any other major search engine worldwide, including Google Trends, Baidu Index, or Yandex Wordstat.

**PI:** Joonho Lim, MD — ORCID 0000-0002-4556-1536
**Target journal:** JMIR Dermatology (IF 3.7)

---

## 2. IMRD

### INTRODUCTION

#### P1: The rise of non-surgical lifting

Non-surgical facial lifting has become one of the fastest-growing segments of the global aesthetic medicine market. High-intensity focused ultrasound (HIFU), radiofrequency (RF) devices, and absorbable thread lifting offer facial tightening and contouring without surgical incision. The International Society of Aesthetic Plastic Surgery (ISAPS) reported that nonsurgical skin tightening procedures increased globally by over 40% between 2019 and 2023. South Korea, one of the world's largest markets for aesthetic procedures, has been at the forefront of this expansion, with multiple domestically developed devices (Shurink, InMode, Oligio) achieving widespread adoption alongside international brands (Ultherapy, Thermage).

#### P2: Who drives non-surgical lifting demand? — Competing hypotheses

Traditionally, non-surgical lifting was sought primarily by patients aged 45 and older as an alternative to surgical facelift. However, practitioners and industry observers have proposed competing narratives about how the demographic composition of demand is evolving. One hypothesis — "prejuvenation" or "preventive aesthetics" (in Korean consumer culture, "슬로우에이징" / slow aging) — posits that younger consumers in their late 20s and 30s are increasingly entering the market, broadening the consumer base downward in age. An alternative hypothesis, grounded in innovation diffusion theory, suggests that young adults may have been early adopters who drove initial awareness, while the traditional 45+ patient base — representing the core clinical indication for skin laxity — subsequently expanded as market awareness matured. Understanding which pattern prevails has implications for clinical practice (patient expectations and risk profiles differ by age), for the aesthetic device market (pricing and marketing strategy), and for infodemiology methodology (whether aggregate search trends accurately reflect demographic shifts). Neither pattern has been quantified at the population level using age-stratified data.

#### P3: The limitation of existing infodemiology tools

Infodemiology — the study of online health information-seeking behavior — has become a standard method for tracking public interest in aesthetic procedures. Google Trends (GT) has been used extensively to analyze temporal patterns in searches for botulinum toxin, dermal fillers, blepharoplasty, and other procedures. However, GT does not provide age-stratified data: it is impossible to determine whether a rise in search volume for a lifting procedure is driven by younger or older consumers. This is a critical limitation for the present research question, which concerns age-specific shifts in information-seeking behavior — patterns invisible when only aggregate volume is observed. No other major global search engine trend tool provides public age-stratified search APIs.

#### P4: Naver DataLab — a unique data source

Naver, the dominant search engine in South Korea (~56% market share), provides a public Search Trend API through Naver DataLab that returns relative search volume (RSV) indices stratified by 11 age bins (0–12 through 60+), gender (male/female), and device type (PC/mobile). This makes Naver DataLab the only major search trend platform worldwide that enables population-level, age-stratified analysis of health information-seeking behavior. Meanwhile, GT data for global English-language keywords can document the emergence of prejuvenation-related terminology — such as "prejuvenation" and "preventive botox" — a narrative that can be tested against the age-stratified Korean search data.

#### P5: Study aim

This study aimed to (1) characterize the direction and magnitude of age-demographic shifts in public search interest for non-surgical lifting procedures in South Korea between 2016 and 2025, testing whether the traditional patient demographic (45+) or the younger demographic (20–34) showed faster relative growth in search interest, (2) identify procedure-specific and gender-specific patterns of age-demographic change, and (3) contextualize the findings against the global emergence of "prejuvenation" as a consumer category, testing whether Korean age-stratified data support or contradict this narrative.

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

where RSV_it is the monthly RSV for a given keyword; Time is months 1–120; Young is 1 for the 20–34 age group and 0 for the 45+ group; Month_m are 11 seasonal dummies; and β₃ is the coefficient of interest. β₃ captures the differential growth rate of the younger group relative to the traditional group: positive indicates faster young growth, negative indicates faster traditional growth. The interpretation depends on the combination of β₁ (baseline trend for the Traditional group) and β₃:

| β₁ | β₃ | Pattern | Interpretation |
|----|-----|---------|----------------|
| > 0 | > 0 | Broadening | Both groups grow, young faster — market expands into youth |
| ≤ 0 | > 0 | Displacement | Young grows, traditional stagnates — zero-sum shift |
| > 0 | < 0 | Maturation | Both groups grow, traditional faster — market matures toward core indication |
| ≤ 0 | < 0 | Contraction | Both decline, young declines faster — overall market decline | Newey-West heteroscedasticity and autocorrelation consistent (HAC) standard errors with 12 lags were used. The model was fitted separately for each keyword group. Multiple comparisons across 6 keyword tests were controlled using the Benjamini-Hochberg false discovery rate (FDR) correction at q < 0.05.

**Approach B (secondary analysis) — Age-group proportional share:**

To estimate the relative contribution of each age group to total search interest, we computed the within-year proportional share:

Proportion(age_a, year_y) = mean_monthly_RSV(age_a, year_y) / Σ_all_ages mean_monthly_RSV(age, year_y)

The Young-to-Traditional Ratio (YTR = Proportion_Young / Proportion_Traditional) was computed annually and tested for linear trend using ordinary least squares regression on year.

Note: This approach assumes that RSV values from separately queried age groups can be meaningfully compared when averaged over a year. This assumption is acknowledged as a limitation, and Approach B results are interpreted as supportive rather than definitive.

**Additional analyses:**
1. Procedure-specific comparison: β₃ values across 6 keywords, visualized as a forest plot, to identify which modalities show the strongest age-demographic shift.
2. Gender stratification: Approach A fitted separately for female and male searchers to test whether the broadening into younger demographics is more pronounced in women.
3. Joinpoint regression: Segmented linear regression applied to the YTR time series to detect inflection points in the YTR trajectory (e.g., timing of market maturation, COVID-19 effects).
4. Google Trends triangulation: descriptive analysis of global GT trends for "prejuvenation", "preventive botox", and "baby botox" to compare the Korean age-shift findings against the global emergence of prejuvenation-related search terms.

**Model diagnostics:**
- Durbin-Watson test and Ljung-Box test (12 lags) for residual autocorrelation
- Prais-Winsten GLS as sensitivity analysis if DW < 1.5
- Fourier terms (2 sine-cosine pairs) as sensitivity alternative to monthly dummies

All analyses were performed using Python 3.11 (pandas, statsmodels, scipy). Two-sided P < 0.05 was considered significant unless otherwise specified.

---

### RESULTS

#### R1: Overall temporal trends
- **Figure 1:** Monthly all-age RSV for 6 Naver keyword groups (2016–2025), with GT global "prejuvenation" RSV overlaid on secondary axis
- All 6 keywords showed positive overall growth (β₁ > 0 for all), with 인모드 (+0.71/mo) and 리프팅시술 (+0.53/mo) showing the strongest aggregate trends

#### R2: Age composition shift — the key finding
- **Figure 2 (key figure):** Annual age-group proportional share, stacked area chart — all keywords combined. The Traditional (45+) share expanded from approximately 25% (2016) to 38% (2025), while the Young (20–34) share contracted from approximately 37% to 28%. The Middle (35–44) group remained the largest share throughout.
- **Table 1:** YTR declined from 1.42 (2016) to 0.77 (2025), combined slope = −0.155/yr (P = 0.004). In 2016, young adults searched at 1.42× the rate of the traditional group; by 2025, the traditional group searched at 1.30× the rate of the young group. Five of six keywords showed negative YTR slope; only 인모드 showed a non-significant positive trend (+0.025/yr, P = 0.56).

#### R3: Interaction model results
- **Table 2:** β₃ was significantly negative for 3 of 6 keywords after BH-FDR correction: 실리프팅 (β₃ = −0.573, 95% CI [−0.750, −0.396], P_BH < 0.001), 리프팅시술 (β₃ = −0.558, 95% CI [−0.767, −0.349], P_BH < 0.001), and 슈링크 (β₃ = −0.267, 95% CI [−0.416, −0.117], P_BH = 0.001). All three showed the "Maturation" pattern (positive β₁, negative β₃): both age groups grew, but the traditional group grew significantly faster.
- The remaining 3 keywords (써마지, 울쎄라, 인모드) showed non-significant β₃, indicating no statistically detectable age-differential growth rate.
- **Figure 3:** Forest plot — all 6 β₃ point estimates lie to the left of zero, with the 3 significant keywords clearly separated. No keyword showed significant youth acceleration.

#### R4: Gender stratification
- **Table 3:** The maturation pattern was present in both genders but more pronounced among female searchers. For 실리프팅: female β₃ = −0.652 (P_BH < 0.001) vs. male β₃ = −0.161 (P_BH = 0.018). For 리프팅시술: female β₃ = −0.573 (P_BH < 0.001) vs. male β₃ = −0.303 (P_BH = 0.002). The traditional-demographic acceleration was driven more strongly by women aged 45+.

#### R5: Joinpoint analysis
- **Figure 4:** Two-joinpoint model selected by BIC (BIC = −11.9 vs. 1.5 for 1-joinpoint and 10.3 for no-joinpoint). R² = 0.977.
- Phase 1 (2016–2018): YTR rose from 1.42 to 2.24 — young adults initially dominated search interest growth.
- Phase 2 (2018–2022): YTR fell sharply from 2.24 to 0.85 — the traditional demographic accelerated its search growth, overtaking the young group. YTR crossed parity (1.0) between 2021 and 2022.
- Phase 3 (2022–2025): YTR stabilized at 0.77–0.88 — the age composition reached a new equilibrium with the traditional group holding a larger relative share.
- The 2018 inflection predates COVID-19, suggesting the maturation process was already underway before the pandemic.

#### R6: Google Trends global context — a dissociation
- GT "prejuvenation" RSV shows exponential growth from near-zero before 2019 to global prominence by 2025. "Preventive botox" and "baby botox" show similar emergence.
- However, the Korean Naver age-stratified data show the opposite of what the prejuvenation narrative would predict: the traditional 45+ demographic, not the young, showed the dominant growth trajectory.
- This **dissociation** between the global prejuvenation narrative (visible in GT) and actual age-stratified search behavior (visible only in Naver) demonstrates that age-agnostic search trend data can produce misleading conclusions about demographic composition.

---

### DISCUSSION

#### D1: Principal findings
- Between 2016 and 2025, search interest in non-surgical lifting grew across all age groups, but significantly faster among the traditional 45+ demographic than the young 20–34 group for 3 of 6 procedure keywords (β₃ range: −0.27 to −0.57, all P_BH < 0.001).
- The positive β₁ for all keywords confirms that both age groups showed increasing search interest. The negative β₃ demonstrates that the traditional demographic grew at a faster rate — a pattern we term "Maturation," consistent with innovation diffusion from early-adopter youth to mainstream older consumers.
- The YTR declined from 1.42 to 0.77, meaning young adults represented a disproportionate share of early interest (2016–2018) but were overtaken by the traditional demographic by 2021. This is the first population-level quantification of age-demographic dynamics in non-surgical lifting interest, and it contradicts the widely assumed "prejuvenation" narrative.

#### D2: Innovation diffusion — from early adopters to mainstream market
- The three-phase trajectory detected by joinpoint analysis (rise 2016–2018, decline 2018–2022, stabilization 2022–2025) is consistent with Rogers' Diffusion of Innovations framework.
- Young adults (20–34), as digital-native, appearance-conscious early adopters, drove initial search interest when non-surgical lifting awareness was expanding. As awareness diffused to the broader population, the traditional patient base (45+ — the demographic with the strongest clinical indication for skin laxity) expanded its search behavior, reflecting movement from the "early majority" to the "late majority" adoption phase.
- The question is not whether lifting "went younger" but whether the market followed a typical innovation diffusion curve where early youth interest was a leading indicator of subsequent mainstream adoption by the clinically indicated population.

#### D3: Procedure-specific patterns — clinical implications
- Thread lifting (실리프팅) showed the strongest maturation effect (β₃ = −0.573), suggesting it was an early "trend" procedure among young adults that subsequently diffused to the traditional demographic.
- The generic search term (리프팅시술) showed a similarly strong maturation effect (β₃ = −0.558), reflecting the overall market dynamic.
- HIFU value (슈링크) showed moderate maturation (β₃ = −0.267), possibly reflecting its positioning as an accessible entry point that eventually reached older consumers.
- RF premium (써마지), HIFU premium (울쎄라), and RF value (인모드) showed no significant age differential, suggesting these brands may have had a more age-stable consumer profile from the outset — or that their marketing reached older demographics earlier in the cycle.
- Clinical implication: the data support the interpretation that non-surgical lifting has matured from a "trend" market driven by younger consumers into a "clinical need" market dominated by the demographic with the greatest physiological indication. Practitioners should recognize that while younger patients may drive initial awareness, the sustained demand base is the traditional 45+ population.

#### D4: Methodological contribution
- Naver DataLab's age-stratified API is globally unique — this is the first academic study to exploit this capability for health research
- The method is transferable to any health topic where age-specific information-seeking is relevant (fertility, chronic disease, mental health, substance use)
- Demonstrates that non-English, non-Google search data can fill critical methodological gaps in infodemiology
- The dissociation between GT global data (supporting the prejuvenation narrative) and Naver age-stratified data (contradicting it) demonstrates that age-stratified search analysis can reveal dynamics invisible to aggregate trend tools — validating the unique methodological contribution of Naver DataLab

#### D5: The role of COVID-19 and platform migration
- The joinpoint at 2018 predates COVID-19, indicating the maturation process was endogenous to the lifting market, not pandemic-driven.
- The sharp YTR decline between 2020–2022 may have been amplified by COVID-19 effects, consistent with the "Zoom face" phenomenon disproportionately motivating older adults (who were more visible in video calls for professional settings) to seek lifting procedures.
- **Platform migration caveat:** A significant alternative explanation for the declining YTR is differential platform migration by age. During 2018–2025, younger Korean internet users increasingly migrated aesthetic information-seeking from Naver to Google, YouTube, Instagram, and TikTok. If younger users preferentially left the Naver search ecosystem, their search interest would be undercounted while the traditional demographic — which has higher Naver loyalty — would appear to grow relatively faster. This confound cannot be fully resolved with Naver data alone. However, Naver remains the dominant platform for clinic-related commercial searches in Korea, so the age shift in Naver search behavior directly reflects the age shift in the patient population that clinics encounter through search-driven patient acquisition.

#### D6: Limitations
- **Platform migration (primary limitation):** Younger Korean users have increasingly shifted to Google, YouTube, Instagram, and TikTok for aesthetic information. Naver's market share among the 20–34 demographic may have declined differentially compared to the 45+ demographic, creating an artificial maturation signal. The observed pattern likely reflects a combination of genuine market maturation and platform-specific demographic shifts.
- Naver RSV is relative and independently normalized per query → cross-age absolute comparison is not directly valid (addressed by Approach A's within-age temporal comparison)
- **RSV normalization artifact:** The independent normalization means that declining YTR could partially reflect changes in the internal reference point within each age query.
- Search interest ≠ procedure uptake: searching does not confirm that the person underwent the procedure
- Keywords may not capture all relevant search behavior (e.g., social media searches, clinic-specific terms)
- The proportional share method (Approach B) relies on an assumption of comparable RSV scaling across age groups
- Single-country primary data: findings may not directly generalize, though Korea's position as a global aesthetic leader provides external validity
- Cannot distinguish patient-searchers from information-seekers (journalists, students, practitioners)
- **Innovation diffusion framing assumes market novelty:** The diffusion framework assumes non-surgical lifting was novel in 2016. In practice, Thermage and Ulthera were already established, so the early-adopter framing may apply primarily to newer entrants (슈링크, 인모드).

#### D7: Conclusion
- Public interest in non-surgical lifting procedures in South Korea, as measured by Naver search behavior, showed a maturation pattern between 2016 and 2025: young adults (20–34) were disproportionate early adopters, but the traditional 45+ demographic showed significantly faster sustained growth, overtaking the younger group by 2022.
- This finding contradicts the widely assumed "prejuvenation" narrative of demographic broadening into younger consumers. Instead, the data are consistent with an innovation diffusion trajectory in which youth-driven early awareness preceded mainstream adoption by the clinically indicated older population.
- The dissociation between global prejuvenation discourse (visible in Google Trends) and age-stratified Korean search data (visible only in Naver DataLab) demonstrates the critical importance of age-stratified analysis in infodemiology.
- However, differential platform migration by age — younger Koreans increasingly searching on Google, YouTube, and Instagram rather than Naver — represents a significant confound that may partially explain the observed pattern.
- Naver DataLab remains a globally unique and underutilized resource for age-stratified health information-seeking research.

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
| Figure 2 | Annual age-group proportional share, stacked area — Traditional (45+) expansion and Young (20–34) contraction | **Key figure** |
| Figure 3 | β₃ forest plot — age-differential growth rate by procedure (β₃ < 0 = Traditional faster) | Procedure comparison |
| Figure 4 | Joinpoint regression on YTR — three-phase maturation trajectory | Inflection detection |
| Table 1 | YTR by year and keyword (YTR < 1 = Traditional dominance; parity crossed ~2021) | Approach B summary |
| Table 2 | β₃ interaction coefficients by keyword — "Maturation" pattern for 3/6 keywords | Primary result |
| Table 3 | β₃ by gender — maturation effect stronger among female searchers | Gender stratification |

| Table S1 | Platform migration sensitivity — β₃ under 3/5/7% annual young-user attrition | Robustness |

Supplementary: full RSV dataset, individual keyword × age time series, Prais-Winsten sensitivity, Fourier sensitivity, platform migration sensitivity, monthly joinpoint

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
│   ├── 04_approach_a.py              # + DW/LB diagnostics, Prais-Winsten, Fourier
│   ├── 04c_sensitivity_platform.py   # Platform migration sensitivity (3/5/7%)
│   ├── 05_approach_b.py
│   ├── 06_joinpoint.py               # + monthly-level sensitivity
│   └── 07_figures.py
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
