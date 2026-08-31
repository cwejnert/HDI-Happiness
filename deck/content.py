"""
The commentary, structured in three acts.

Single source of truth for both outputs: build_artifact.py renders it as a
self-contained HTML page for the co-author team, build_pptx.py renders the
same content as a slide deck for presenting. Edit the argument here, rebuild
both.

Every number in this file traces back to make_figures.py / HappinessSDG.R;
figure filenames refer to deck/figures/.
"""
from __future__ import annotations

TITLE = "Measured Where It Varies"
SUBTITLE = (
    "A commentary in three acts, on why development predicts where wellbeing "
    "is high but not when it rises — and why health leads once it is measured "
    "somewhere it still moves"
)
DATELINE = "Working synthesis for the co-author team · August 2026"
SCOPE = (
    "SDG: 42 countries, 661 series · HDI × World Happiness Report: 151 "
    "countries, 2011–2023 · Subnational HDI: 239 regions · European Social "
    "Survey: 36 countries, 351,023 respondents, rounds 5–11 (2010–2023)"
)

# --------------------------------------------------------------------------
# Opening
# --------------------------------------------------------------------------
HOOK = {
    "kicker": "The setup",
    "heading": "Development rose almost everywhere. Wellbeing did not follow it.",
    "body": [
        "The SDG paper now under review makes a narrow, awkward claim: the "
        "association between development indicators and happiness is strong "
        "when countries are compared with one another, and close to absent "
        "when each country is compared with its own past. Thirty of the 42 "
        "countries with usable SDG coverage show a significant SDG–happiness "
        "association in levels. Two do in year-to-year changes.",
        "There is an obvious way to dismiss that result. The SDG framework is "
        "a sprawling, politically negotiated instrument of more than two "
        "hundred indicators with uneven coverage; a null finding inside it "
        "says as much about the framework as about the world. This commentary "
        "closes that escape route, and then asks the question the result "
        "actually raises: if development in the aggregate does not track "
        "wellbeing over time, which of its parts tracks wellbeing at all? "
        "Health, education, income, social connection — the frameworks "
        "disagree sharply about the answer, and the disagreement turns out to "
        "be about measurement rather than about the world.",
    ],
    "acts": [
        ("I", "We replicate the SDG result outside the SDGs.",
         "The same design on the HDI, against a second wellbeing survey, and "
         "one spatial scale down. It collapses every time."),
        ("II", "Health leads — once it is measured where it still varies.",
         "The domain rankings invert with the instrument. Education runs the "
         "same problem in reverse, and social trust cannot yet be checked."),
        ("III", "Which makes the policy question unavoidable.",
         "What this means for priorities, what kind of health and education "
         "it points at, and the question we are putting to the field."),
    ],
}

# --------------------------------------------------------------------------
# Acts
# --------------------------------------------------------------------------
ACTS = [
    {
        "numeral": "I",
        "title": "Replicating the collapse beyond the SDGs",
        "key_numbers": [
            ("71% → 5%", "of countries significant, SDG levels → differences"),
            ("42% → 2%", "the same collapse under the HDI composite"),
            ("15% → 9%", "of cells, against a second wellbeing survey (ESS)"),
        ],
        "thesis": (
            "Run the original design on a second development framework, "
            "against a second wellbeing instrument, and one spatial scale "
            "down. The levels-to-differences collapse appears every time. The "
            "subnational HDI plays a different role: it asks whether the "
            "national pattern survives disaggregation."
        ),
        "beats": [
            {
                "label": "Replication 1 · the HDI",
                "heading": "A deliberately parsimonious index behaves exactly like the sprawling one",
                "body": [
                    "The Human Development Index is the opposite of the SDG "
                    "framework in every way that the dismissal relies on: three "
                    "dimensions rather than seventeen goals, a single custodian, "
                    "a stable definition, near-universal coverage. Substituting "
                    "it for the SDG indicators and holding everything else fixed "
                    "gives 64 of 151 countries FDR-significant in levels and 3 of "
                    "151 in first differences — 42% down to 2%.",
                    "The SDG framework collapsed from 71% of countries to 5%. The "
                    "two rates are not directly comparable, because the SDG test "
                    "asks whether <em>any</em> of a country's several hundred "
                    "series is significant while the HDI test asks about one "
                    "composite; that difference is exactly why the SDG levels "
                    "rate is higher. What compares is the collapse itself, and it "
                    "is an order of magnitude in both. Whatever produces the "
                    "asymmetry, it is not the design of the SDG indicator set.",
                ],
                "figure": "collapse_hdi_shdi_whr.png",
                "caption": "Countries with an FDR-significant development–happiness "
                           "association, levels versus first differences, under the SDG "
                           "framework and under the HDI composite.",
            },
            {
                "label": "The structure underneath",
                "heading": "The composite is not the whole result — the five indicators behave differently",
                "body": [
                    "HappinessHDI.R reports the composite alongside its four "
                    "sub-components in both specifications, and the "
                    "sub-components do not simply track the composite. Mean "
                    "years of schooling has the highest median R² of the five "
                    "in levels (0.326) and in differences (0.069) — above the "
                    "composite HDI itself (0.322 and 0.063). Income is level "
                    "with it in levels and below it in differences; life "
                    "expectancy is clearly weakest in levels (0.160, 30 of 151 "
                    "countries).",
                    "The result worth carrying forward is in the differences "
                    "column. Expected years of schooling is significant in 7 of "
                    "150 countries — more than the composite's 3, and more than "
                    "any other indicator. Seven countries is a small number and "
                    "the collapse is still severe, so this is not a survival "
                    "story. But it does mean the education pair leads under "
                    "both specifications rather than only in the "
                    "cross-section — and that life expectancy, the HDI's proxy "
                    "for health, is last in levels. Act II shows why that "
                    "ordering is a property of the HDI's measurement choices "
                    "rather than of the domains.",
                ],
                "figure": "hdi_full_structure.png",
                "caption": "The HDI composite and its four sub-components, levels and "
                           "first differences. Benjamini–Hochberg corrected across the "
                           "five indicators within each country.",
            },
            {
                "label": "What the subnational HDI is for",
                "heading": "Not a second producer — a test of whether the national pattern holds inside countries",
                "body": [
                    "The Global Data Lab's SHDI cannot serve as an independent "
                    "replication, and the commentary should not present it as "
                    "one. At national level it is numerically identical to the "
                    "UNDP HDI: all 1,696 overlapping country-years agree exactly, "
                    "because GDL derives the national figure from the UNDP "
                    "series. Running the collapse design on it reproduces the "
                    "HDI result by construction rather than by corroboration.",
                    "Its actual value is disaggregation. GDL's region-level "
                    "values are its own — only 655 of 58,224 region-years "
                    "coincide with their country's national figure — so the SHDI "
                    "is what lets us ask whether the national development–"
                    "wellbeing relationship holds at subnational level, and "
                    "where it does not. That question is the subject of Act III, "
                    "and the answer turns out to be the most policy-relevant "
                    "result in the commentary.",
                ],
            },
            {
                "label": "Replication 3 · a second wellbeing instrument",
                "heading": "It is not an artifact of the Cantril ladder either",
                "body": [
                    "The World Happiness Report's ladder is a single "
                    "self-anchoring item asked by one survey house. Replacing it "
                    "with the European Social Survey's own life-satisfaction and "
                    "happiness items — 36 countries, 351,023 respondents, seven "
                    "roughly biennial waves from 2010 to 2023 — preserves the "
                    "asymmetry.",
                    "Statistical power is much lower here: seven biennial waves "
                    "against twelve or more annual World Happiness Report years, "
                    "so individual country tests are fragile and the ESS "
                    "replication should be read as corroboration rather than as "
                    "independent confirmation at the same strength.",
                ],
                "figure": "collapse_hdi_ess.png",
                "caption": "The same design with ESS life satisfaction in place of "
                           "the Cantril ladder. 15% of levels cells and 9% of "
                           "differences cells are FDR-significant.",
            },
            {
                "label": "Replication 4 · one scale down",
                "heading": "And it holds across 239 European regions",
                "body": [
                    "Region-level subnational HDI against region-mean life "
                    "satisfaction reproduces the same levels-over-differences "
                    "pattern, noisier as expected. The result is now documented "
                    "at three scales — SDG-national, HDI-national, SHDI-regional "
                    "— and against two wellbeing instruments.",
                ],
                "figure": "collapse_shdi_ess_regional.png",
                "caption": "Regional subnational HDI against region-mean ESS life "
                           "satisfaction, 239 European regions.",
            },
        ],
        "close": (
            "Two independent replications and one scale test. "
            "The commentary can therefore state the asymmetry as a property of "
            "the development–wellbeing relationship rather than of any "
            "particular index, and move on to the question that actually "
            "matters: given that almost nothing survives the move to "
            "within-country change, what carries the level signal?"
        ),
    },
    {
        "numeral": "II",
        "title": "What matters is decided by how you measure it",
        "key_numbers": [
            ("11.2% vs 1.2%", "health vs education, SDG data, high-income countries"),
            ("36 / 36", "countries where self-rated health predicts life satisfaction"),
            ("19.9%", "life expectancy — the HDI's weakest component"),
        ],
        "thesis": (
            "Rank the domains and the answer inverts depending on the "
            "instrument. Health is the HDI's weakest component and the "
            "strongest thing in both the SDG ranking and the ESS. Education is "
            "the HDI's strongest and the SDG framework's weakest. Neither "
            "disagreement is about the world; both are about how the domain "
            "was operationalised."
        ),
        "beats": [
            {
                "label": "The autopsy",
                "heading": "What survives in levels is survival",
                "body": [
                    "Ranking the 609 SDG series measured in at least 8 countries "
                    "by the share of countries in which they are FDR-significant "
                    "puts safely managed sanitation first, then infant deaths, "
                    "under-five deaths, child stunting, and safely managed "
                    "drinking water. Sixteen of the top 25 series are "
                    "health-domain, and none of them is self-reported.",
                    "This is the steep part of the development curve — staying "
                    "alive and not being sick — rather than the 2030 Agenda's "
                    "institutional superstructure. Goal 3 ranks 4th of 17 goals "
                    "at 11.5%. Goal 16, the closest thing the framework has to "
                    "social trust, ranks 15th at 1.5%.",
                ],
                "figure": "sdg_indicator_top20.png",
                "caption": "The 20 highest-ranking SDG series of 609, by share of "
                           "countries FDR-significant in levels.",
            },
            {
                "label": "The horse race",
                "heading": "Run the domains against each other in one survey and health wins at every level",
                "body": [
                    "The ESS measures health, education, income and trust on the "
                    "same respondents as life satisfaction, so the domains can "
                    "compete on equal terms. Self-rated health is significant in "
                    "36 of 36 countries with a median R² of 0.091 — roughly nine "
                    "times education's 0.0098, which is the smallest effect of "
                    "any domain tested. Within countries, across regions, health "
                    "holds at +0.51 while development falls to +0.12.",
                    "The HDI leads between countries, at R² = 0.760, but that is "
                    "the one comparison where a composite index is expected to "
                    "win: it proxies every domain at once. It falls to fourth "
                    "once you look inside countries.",
                ],
                "figure": "domain_horse_race.png",
                "caption": "Domains competing within one instrument, at three levels "
                           "of aggregation. Health and trust are self-reported "
                           "alongside the outcome — see the next beat.",
            },
            {
                "label": "The method check",
                "heading": "Health survives the obvious objection; social trust does not",
                "body": [
                    "Self-rated health and social trust are reported by the same "
                    "respondent, in the same survey, as life satisfaction, so "
                    "shared method variance is the first thing a reader will "
                    "raise. The UN SDG database is administrative and shares no "
                    "method with any wellbeing instrument, which makes it the "
                    "natural check.",
                    "Health passes it. Restricted to high-income countries — the "
                    "same development stratum the ESS covers — the SDG data puts "
                    "health at 11.2% of country-indicator pairs against "
                    "education's 1.2%, the same ordering the ESS gives from "
                    "entirely different measurement. Social trust fails it: "
                    "there is no interpersonal-trust indicator anywhere in the "
                    "SDG framework, and Goal 16's best series ranks 125th of "
                    "609. Trust is the strongest ESS predictor and has no "
                    "independent corroboration available. It should enter the "
                    "commentary as an open question, not a result.",
                ],
                "figure": "health_trust_corroboration.png",
                "caption": "The same three domains under an administrative source and "
                           "a self-report source.",
                "feature": True,
            },
            {
                "label": "The saturation problem",
                "heading": "Why the HDI says health barely matters",
                "body": [
                    "Inside the HDI, life expectancy is the weakest of the five "
                    "indicators by a wide margin — significant in 30 of 151 "
                    "countries (19.9%), against 40.7% for mean schooling. Read "
                    "naively, the HDI says health is the least important thing "
                    "about development.",
                    "It says nothing of the kind. Life expectancy is close to "
                    "saturated across the countries where it is tested: the "
                    "variance that would let it predict anything has largely "
                    "gone. The SDG series that do carry health's signal are "
                    "survival measures — child and neonatal mortality, stunting "
                    "— which still vary enormously, and self-rated health "
                    "captures morbidity that life expectancy cannot see at all. "
                    "A domain disappears from a framework when that framework "
                    "measures it with a variable that has run out of room.",
                ],
            },
            {
                "label": "Sub-highlight · education",
                "heading": "Education is the same problem running in the opposite direction",
                "body": [
                    "Education inverts the health story exactly. It is the HDI's "
                    "strongest domain — mean years of schooling has the highest "
                    "median R² of all five indicators, 0.326, above the "
                    "composite itself — and the SDG framework's weakest, at 3.3% "
                    "pooled, with its best series ranking 100th of 609.",
                    "The disagreement is again construct choice. Eighteen of "
                    "SDG4's 35 official series are equity or parity ratios, six "
                    "measure learning outcomes, seven measure school "
                    "infrastructure, and only two measure access and "
                    "participation directly. Split apart, access reaches 12.7% "
                    "— comparable to health's 11.5% — while learning outcomes "
                    "sit at 0.9% and parity ratios at 2.5%. The pooled 3.3% is "
                    "an average across constructs pointing in different "
                    "directions and describes none of them. Pooling within a "
                    "goal can manufacture a null.",
                ],
                "figure": "sdg4_unpooled.png",
                "caption": "SDG4 split by what each indicator actually measures, with "
                           "the pooled figure marked.",
            },
            {
                "label": "Sub-highlight · education",
                "heading": "And it is the one domain that is significant almost everywhere, if barely",
                "body": [
                    "Respondents' own attainment predicts their own life "
                    "satisfaction in 32 to 34 of 36 ESS countries — more "
                    "consistent across countries than anything except health "
                    "itself. Aggregated to the country level, ESS-measured years "
                    "of schooling predicts World Happiness Report happiness at "
                    "R² = 0.308, against 0.161 for the HDI's own schooling "
                    "series on the same cells: an independently measured "
                    "education variable roughly doubles the HDI's.",
                    "What it does not have is size. The median individual R² is "
                    "0.0098, the smallest of any domain in the horse race, and "
                    "within countries education sits at +0.13 with 2 of 16 "
                    "countries significant. Education is the most universal "
                    "signal and the smallest one, which is a genuinely odd "
                    "combination and worth stating as such rather than "
                    "resolving prematurely.",
                ],
                "figure": "ess_individual_education.png",
                "caption": "Per-country tests of respondents' own attainment against "
                           "their own life satisfaction, 36 ESS countries.",
            },
            {
                "label": "The composite",
                "heading": "The three panels the commentary needs",
                "body": [
                    "Commentaries carry one or two display items, so the "
                    "argument has to fit in a single figure: the replicated "
                    "collapse, the inversion of the health–education ranking "
                    "across instruments, and the method check that only health "
                    "passes.",
                    "One caution for the caption. Panels b and c both put "
                    "measures with different units on a shared axis — panel b "
                    "normalises to the health-plus-education pair, panel c to "
                    "the leading domain within each source. Both are there to "
                    "make an <em>ordering</em> readable, not a magnitude, and "
                    "the raw values are printed on the bars so a reader can "
                    "check that.",
                ],
                "figure": "Figure1_commentary.png",
                "caption": "Proposed Figure 1 for submission. Draft — see the caution "
                           "above on panels b and c.",
                "feature": True,
            },
        ],
        "close": (
            "Two domains, two frameworks, two opposite verdicts, and in both "
            "cases the disagreement is about measurement rather than about the "
            "world. Health leads once it is measured somewhere it still varies; "
            "education leads once it is measured as attainment rather than "
            "parity. The commentary's contribution is not a ranking of domains "
            "but the demonstration that the ranking is an artefact of "
            "operationalisation — and that both domains survive when measured "
            "properly, while trust cannot yet be checked at all."
        ),
    },
    {
        "numeral": "III",
        "title": "Priorities, and what kind of health and education",
        "key_numbers": [
            ("+0.87 → +0.12", "development, between countries → within them"),
            ("+0.51", "self-rated health, within countries"),
            ("11.2% vs 1.2%", "health vs education, SDG data, high-income countries"),
        ],
        "thesis": (
            "Two questions follow. Where should the lever be pulled — which "
            "turns on scale, because the ordering of predictors inverts "
            "inside countries. And what kind of health and education, because "
            "in both domains the wellbeing signal sits with one "
            "operationalisation and vanishes under another."
        ),
        "beats": [
            {
                "label": "Where the lever is",
                "heading": "Development inequality inside countries mostly does not become wellbeing inequality",
                "body": [
                    "Below the Very High tier, countries contain multitudes. "
                    "Germany's regions span 0.05 of subnational HDI; China's "
                    "span 0.30 and India's 0.19 — several development tiers' "
                    "worth of variation inside single countries. If regional "
                    "development drove regional wellbeing, this is where it "
                    "would show.",
                    "It mostly doesn't. Holding country fixed and regressing "
                    "region-mean life satisfaction on regional subnational HDI "
                    "gives a significantly positive gradient in only 3 of 16 "
                    "ESS countries — France, Belgium, and Germany — and the "
                    "gradient is not steeper where internal inequality is "
                    "larger. Which country's ladder you are on matters more "
                    "than which rung you occupy within it.",
                ],
                "figure": "within_country_gradient.png",
                "caption": "Within-country gradients of region-mean life satisfaction "
                           "on regional SHDI, 16 ESS countries ordered by national HDI.",
            },
            {
                "label": "The flip",
                "heading": "Health and social trust do inside countries what development does between them",
                "body": [
                    "Between countries, development leads and the two wellbeing "
                    "instruments agree almost exactly: the HDI correlates at "
                    "r = +0.89 with World Happiness Report happiness and +0.87 "
                    "with ESS life satisfaction, with trust and health close "
                    "behind and all three positive.",
                    "Within countries the ranking inverts. Development falls to "
                    "a median regional correlation of +0.12, significant in 3 of "
                    "16 countries, while self-rated health holds at +0.51 "
                    "(8 of 16) and social trust at +0.49 (6 of 16). The World "
                    "Happiness Report cannot see this at all — it has no "
                    "subnational values. It is the specific thing the ESS adds.",
                    "Two cautions on the detail. The health-versus-trust "
                    "ordering is not stable: aggregating region means across "
                    "waves rather than within them reverses it, putting trust "
                    "at +0.57 and health at +0.50. What is stable, under every "
                    "specification we tried, is that both sit near +0.5 while "
                    "development sits near zero. And per-country coverage "
                    "varies sharply — Italy matches only 30% of respondents to "
                    "a region, Sweden 57%, Croatia 69%, against 91–100% "
                    "elsewhere. Dropping those three, or dropping regions built "
                    "on fewer than 200 respondents, leaves the flip intact.",
                ],
                "figure": "ranking_flip.png",
                "caption": "Candidate Figure 2. National correlations beside "
                           "within-country regional correlations, for development, "
                           "health, and trust.",
                "feature": True,
            },
            {
                "label": "On priorities",
                "heading": "Indicator dashboards are not wellbeing instruments",
                "body": [
                    "Development indicators tell you reliably where wellbeing is "
                    "high. They tell you almost nothing about when it will rise. "
                    "Across every framework tested here, year-on-year indicator "
                    "movement carries essentially no wellbeing information within "
                    "the measurement window — a decade or so.",
                    "The implication is about horizon and instrument, not about "
                    "whether development matters. A monitoring architecture "
                    "designed to reward annual indicator movement should not be "
                    "read as tracking wellbeing, and a government that improves "
                    "its dashboard position in a given year should not expect a "
                    "wellbeing dividend inside the same electoral cycle.",
                ],
            },
            {
                "label": "On what kind of health",
                "heading": "Monitor health where it still varies, not where it has already converged",
                "body": [
                    "Life expectancy is the standard summary of population "
                    "health and the HDI's only health input, and it is the "
                    "weakest of the HDI's five indicators against wellbeing. "
                    "That is a measurement failure rather than a substantive "
                    "one. What carries health's signal is survival at the "
                    "margin — child, infant and neonatal mortality, stunting, "
                    "sanitation and safe water — and, in rich countries, "
                    "self-rated health, which picks up morbidity and "
                    "functional limitation that life expectancy cannot see.",
                    "For monitoring, that argues for retiring life expectancy "
                    "as the headline wellbeing-relevant health measure in "
                    "high-income settings and pairing survival indicators with "
                    "a subjective health item. The ESS already fields one; most "
                    "national statistical systems do too. It is close to free.",
                ],
            },
            {
                "label": "On what kind of education",
                "heading": "The consensus moved to learning; the wellbeing evidence points at attainment",
                "body": [
                    "Global education policy has shifted decisively over the "
                    "past decade from schooling to learning — the learning-crisis "
                    "framing, learning-poverty targets, and an indicator "
                    "architecture built around measured proficiency. The premise "
                    "is that years in school without demonstrated learning are "
                    "an empty metric.",
                    "Every level of aggregation we can test points the other "
                    "way. Attainment and access carry the signal — 12.7% for "
                    "SDG4 access, 40.7% and 34.0% for the HDI's schooling "
                    "components, 32 of 36 countries at the individual level — "
                    "while measured learning outcomes sit at 0.9% and parity "
                    "ratios at 2.5%. The caution from Act II applies: education "
                    "is the most consistent signal and the smallest one.",
                ],
            },
            {
                "label": "What we cannot say",
                "heading": "Three limits that keep this a question rather than a recommendation",
                "body": [
                    "None of this is causal. The design is correlational "
                    "throughout, and the levels results in particular are "
                    "cross-sectional comparisons between countries.",
                    "Schooling cannot be separated from what schooling stands "
                    "in for. Years attained proxy labour-market position, "
                    "economic security, autonomy, and social standing, and this "
                    "design cannot pull them apart. Individual effects are "
                    "small: a median R² near 0.01.",
                    "The within-country results are Europe-only. The ESS is "
                    "the only regional wellbeing source with the coverage this "
                    "design needs — Gallup's subnational files are paywalled — "
                    "so the priorities argument generalises across 16 European "
                    "countries and not beyond them. That belongs in the text as "
                    "a scope condition, not buried in a limitations paragraph, "
                    "because the ranking flip is the most policy-relevant "
                    "result here and will be the most contested.",
                    "Some of the parity and learning indicators' weakness is "
                    "coverage rather than construct — they are the youngest and "
                    "thinnest series in the SDG database, and thin series fail "
                    "significance tests for uninteresting reasons. The "
                    "commentary should concede this explicitly and say what "
                    "would settle it.",
                ],
            },
            {
                "label": "The ask",
                "heading": "Should wellbeing be a criterion for how we measure development after 2030?",
                "body": [
                    "That is the question the commentary exists to pose, and it "
                    "has a sharp form. Two of the most consequential domains in "
                    "development are monitored through variables that have "
                    "either run out of variance or measure a different "
                    "construct from the one the policy debate is about: health "
                    "through life expectancy, education through parity and "
                    "proficiency. If wellbeing is to be a criterion for the "
                    "post-2030 architecture at all, the first question is not "
                    "which domain to prioritise but whether each domain is "
                    "being measured somewhere it can still move.",
                    "A commentary cannot settle that. It can put the "
                    "disagreement on the record with the evidence attached, "
                    "which is what the three acts are for.",
                ],
            },
        ],
        "close": (
            "The recommended framing for submission: lead with the education "
            "exception as the positive finding, use the generalised collapse "
            "as the backdrop that makes it surprising, and close on the "
            "target-setting question. That ordering makes Act I load-bearing "
            "without making it the story."
        ),
    },
]

# --------------------------------------------------------------------------
# Decisions for the co-author team
# --------------------------------------------------------------------------
DECISIONS = [
    ("Framing",
     "Lead with the education exception and use the generalised collapse as "
     "Act I backdrop — recommended — or lead with the robustness result and "
     "treat education as the coda. This decides title, abstract, and venue."),
    ("Display items",
     "Commentaries allow one or two. Proposed: the three-panel composite as "
     "Figure 1, the ranking flip as Figure 2. Everything else moves to "
     "supplementary."),
    ("Scope of the within-country work",
     "It now sits inside Act III as the evidence on priorities. Does it "
     "belong there, or in a third paper? It is the most policy-relevant and "
     "the most contested result we have, and it is Europe-only."),
    ("Data investment",
     "The Global Data Lab's separate Education &amp; Work dataset carries 43 "
     "subnational schooling indicators by cohort and sex. Pulling it would "
     "let us test the education finding subnationally. Before submission or "
     "after review?"),
    ("Methods note",
     "Pooled R² and significant-country share tell different stories at "
     "several points. Proposal: report both throughout and discuss the "
     "divergence explicitly as a secondary contribution."),
]

# --------------------------------------------------------------------------
# Evidence appendix — everything not carried in the acts
# --------------------------------------------------------------------------
APPENDIX = [
    ("hdi_vs_sdg_frameworks.png", "HDI against SDG, domain by domain",
     "Education is the HDI's strongest domain and the SDG framework's weakest, "
     "unless SDG4 is split into access versus the rest. Absolute levels are "
     "not comparable across frameworks; the within-framework rankings are."),
    ("ess_triangulation.png", "ESS-measured schooling against WHR happiness",
     "Country-aggregated ESS years of schooling predicts WHR happiness at "
     "R² = 0.308, against 0.161 for the HDI's own schooling series on the same "
     "cells — an independently measured education variable roughly doubles it."),
    ("shdi_within_country_spread.png", "Regional development spread within countries",
     "Every region a dot, two countries per UNDP development tier, 2022. "
     "Germany's regions span 0.05 of SHDI; China's span 0.30, India's 0.19."),
    ("sdg_by_goal.png", "SDG significance by goal, pooled",
     "The leading goal (Energy, 16.0%) clears FDR significance in barely one "
     "country-test in six; pooled Education ranks 12th of 17."),
    ("shdi_vs_hdi_validation.png", "GDL national SHDI against the UNDP HDI",
     "The two are the same series — R² = 1.000, every country-year identical, "
     "because GDL derives the national figure from the UNDP index. Retained to "
     "document the check, not as validation: agreement here says nothing about "
     "the subnational disaggregation, which is where GDL's own data begins."),
    ("shdi_whr_levels_scatter.png", "Subnational HDI against WHR happiness, levels",
     "The familiar development-tier gradient with SHDI in place of HDI."),
    ("ess_year_coverage.png", "ESS coverage by country and year",
     "A rotating panel: 36 countries, roughly biennial from 2010 to 2023, "
     "with 17 countries present in all seven waves. This is the power "
     "constraint behind every ESS significance test."),
    ("region_crosswalk_match.png", "ESS-to-SHDI region crosswalk",
     "62% of respondents, across 24 of 36 countries, matched to a subnational "
     "SHDI value through the NUTS-to-GDL crosswalk."),
    ("hdi_ess_heatmap.png", "Country × indicator significance, ESS",
     "15% of levels cells and 9% of differences cells FDR-significant; "
     "direction consistent with the WHR results, power much lower."),
    ("hdi_ess_collapse_scatter.png", "Per-country collapse, ESS",
     "More above-the-line exceptions than the WHR analysis shows — sparse "
     "waves cut both ways."),
    ("hdi_vs_lifesat_trends.png", "HDI progress against life-satisfaction trends, 2010–2023",
     "HDI rose nearly everywhere. ESS life satisfaction rose in 19 countries "
     "and fell in 8."),
    ("region_shdi_lifesat_pooled.png", "Region-level SHDI against life satisfaction, pooled",
     "1,313 region-years, pooled R² = 0.32 — this mixes between- and "
     "within-country variation, which the within-country panels separate."),
    ("within_country_small_multiples.png", "Within-country regional gradients, small multiples",
     "Holding country fixed, the regional development–wellbeing gradient is "
     "weak in most countries. France is the clearest exception."),
    ("european_regional_inequality.png", "Regional SHDI spread within ESS countries",
     "Italy and Poland carry several times the internal development "
     "inequality of Germany or the Nordics."),
    ("mechanisms_trust_health.png", "Trust and health as rival predictors, nationally",
     "Self-rated health out-predicts the HDI nationally on significant-country "
     "share, 37% against 19%."),
    ("mechanisms_percountry_detail.png", "Per-country detail behind the ranking flip",
     "Signed within-country regional correlations for all 16 countries; "
     "filled markers are p &lt; .05. Sweden reads negative on all three, but "
     "only 57% of Swedish respondents carry a usable region code, so that "
     "result should not be interpreted."),
]
