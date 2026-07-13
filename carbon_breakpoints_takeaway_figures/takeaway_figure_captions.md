# Reader-first "takeaway" figure set

Design rule: every figure is one sentence a non-expert could repeat, stated in the
title; one encoding beyond position; direct labels instead of legend decoding.
Built by `07_build_takeaway_figures.R` from the frozen pipeline outputs
(`outputs/final_master/derived`, `outputs/frozen_results_v1`,
`outputs/global_harmonization`, `outputs/global_mechanisms`). PNG (300 dpi) + SVG.

## Figure 1 — The world's carbon-intensity curve bent in the early 1970s, decades before Rio or Paris
Top: global C/GDP indexed to 1965 = 100 (log scale) with the two-segment fit and the
data-selected 1973 break; Rio and Paris marked 20–40 years to the right. Slope labels:
-0.1%/yr before, -0.8%/yr after. Bottom: the three Kaya-pathway break estimates with
moving-block bootstrap 95% intervals (C/GDP 1973 [1967–1989]; E/GDP 1974 [1972–1977];
C/E 1992 [1978–2011], annotated so the point estimate is not read as identifying Rio).

## Figure 2 — Why a significant treaty-year break is weak evidence on its own
Top: BIC improvement from placing the global C/E break at every candidate year
(aggregate reconstruction of the global series). 1992 fits well — and sits on a broad
plateau of years that fit comparably or better, which is why the bootstrap interval in
Figure 1 is wide. Bottom: the evidentiary funnel per treaty and component — share of
country-component series that are nominally significant at the treaty date vs. the
share that also beat nearby placebo years (Rio: 69→6% C/GDP, 57→14% C/E, 64→22% E/GDP;
Paris: 69→9%, 48→8%, 69→10%).

## Figure 3 — 97 national breakpoints across five decades: tracking economic history, not treaty dates
Top: one dot per country on a single time axis, stacked by year; shaded bands mark the
oil shocks, post-Cold-War upheaval, the Asian crisis, the global financial crisis, and
the cheap-renewables era; Rio and Paris are two thin dashed lines. Green triangles are
the 9 policy-enabled cases. Bottom: observed vs. restricted-random event alignment for
the 71 documented episodes (45% vs 17% within 2 years; 80% vs 37% within 5; 70% vs 33%
inside the episode).

## Figure 4 — What accompanied the 97 bends? Mostly markets, restructuring, disruption
Unit census (one square per country) of the primary mechanism: fuel & energy markets 22,
economic restructuring 18, political disruption 11, macroeconomic shock 9, development &
energy access 6, climate policy & low-carbon technology 9 (highlighted), unresolved 22.

## Figure 5 — A favorable bend is not yet a success: intensity often improves while emissions keep rising
Scatter of signed standardized improvement in the intensity slope (x) against the
post-break trend in absolute CO2 (y), with plain-language quadrant labels and counts:
improved & falling 19; improved but rising 55; worsened & rising 22; worsened & falling 1.
The 9 policy-enabled cases are green triangles, making visible which of them also achieve
falling absolute emissions (BTN and PRY do not).

## Figure 6 — Independent climate raters rank the policy-enabled cases high, but coverage is thin
Percentile strips of CAT (26 covered; policy median 64th vs others' 34th) and CCPI
(18 covered; 91st vs 44th) with every covered country shown as a dot, so the tiny
policy-enabled coverage (3 CAT, 2 CCPI) is visible rather than summarized away.

## Supplement S1 — Trade accounting moves the apparent start of national transitions
Dumbbell of production- vs consumption-based break years for the 17 jointly eligible
countries (6 of 17 within five years; median gap 12 years). Caveat stated on the figure:
consumption-based series begin in 1990, so very early production breaks cannot be
matched by construction — part of the gap is mechanical.

## Supplement S2 — Demand-side (E/GDP) breaks often align with recession or sectoral change
Available-case attribution for the 53 eligible E/GDP breaks.

---

## Analytical notes surfaced while building (worth a sentence in the paper)

1. **The 34 Rio-unique E/GDP cases are not post-Soviet economies** (only Mongolia is).
   They are dominated by small developing economies plus India, South Africa,
   New Zealand, and Finland — the early-1990s upheaval era (structural adjustment,
   conflicts, Indian liberalization, the Finnish depression driven by the Soviet trade
   collapse). Of the 23 with classified headline breaks, political disruption leads (7)
   and only 3 are policy-enabled: even date-unique treaty signals mostly dissolve into
   documented non-treaty events. Former Soviet states themselves are excluded by the
   10-year pre-break data requirement.
2. **Two different "nines":** policy-enabled mechanism (n = 9) and constructive
   persistent decarbonization (n = 9) are overlapping but not identical sets — e.g.
   Bhutan and Paraguay are policy-enabled with absolute emissions still rising.
   Figure 5 makes the distinction visible.
3. **Consumption-based break dates can only exist from 1990 onward**, so the median
   12-year production-consumption gap is partly mechanical for early production breaks.
4. Palette: the Kaya trio was adjusted to #3A66A5 / #2E8B57 / #C77F00 to pass
   lightness/chroma/contrast/CVD checks on white; all figures also carry direct labels
   so no information is color-alone.
