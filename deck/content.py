"""
The commentary, structured in four acts.

Single source of truth for both outputs: build_artifact.py renders it as a
self-contained HTML page for the co-author team, build_pptx.py renders the
same content as a slide deck for presenting. Edit the argument here, rebuild
both.

Every number in this file traces back to make_figures.py / HappinessSDG.R;
figure filenames refer to deck/figures/.
"""
from __future__ import annotations

TITLE = "The Education Exception"
SUBTITLE = (
    "A commentary in four acts, on why development predicts where wellbeing "
    "is high but not when it rises — and on the one construct that behaves "
    "differently"
)
DATELINE = "Working synthesis for the co-author team · August 2026"
SCOPE = (
    "SDG: 151 countries · HDI &amp; SHDI × World Happiness Report: 150 countries, "
    "2011–2023 · European Social Survey: 36 countries, 351,023 respondents, "
    "rounds 5–11 (2010–2023)"
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
        "when each country is compared with its own past. Sixty-four of 151 "
        "countries show a significant SDG–happiness association in levels. "
        "Three do in year-to-year changes.",
        "There is an obvious way to dismiss that result. The SDG framework is "
        "a sprawling, politically negotiated instrument of more than two "
        "hundred indicators with uneven coverage; a null finding inside it "
        "says as much about the framework as about the world. This commentary "
        "closes that escape route, and then reports the one thing in the data "
        "that does not behave the way everything else does.",
    ],
    "acts": [
        ("I", "The collapse is not about the SDGs.",
         "Same design, three development frameworks, two spatial scales, two "
         "wellbeing instruments. It replicates every time."),
        ("II", "Something is different about education.",
         "But only when education is measured as attainment and access — not "
         "as parity, and not as measured learning."),
        ("III", "The lever changes when the scale changes.",
         "Between countries, development leads. Inside them, health and trust "
         "do the work and development flattens."),
        ("IV", "So we put a question to the field.",
         "The global education architecture is built around learning "
         "outcomes. The wellbeing evidence points at attainment."),
    ],
}

# --------------------------------------------------------------------------
# Acts
# --------------------------------------------------------------------------
ACTS = [
    {
        "numeral": "I",
        "title": "The collapse is a property, not an artifact",
        "key_numbers": [
            ("67 → 6", "of 150 countries significant, HDI levels → differences"),
            ("66 → 6", "of 148, subnational HDI"),
            ("3 × 2", "spatial scales × wellbeing instruments"),
        ],
        "thesis": (
            "Run the original design on three unrelated development "
            "frameworks, at two spatial scales, against two independent "
            "wellbeing instruments. The levels-to-differences collapse "
            "appears in all of them."
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
                    "gives 67 of 150 countries FDR-significant in levels and 6 of "
                    "150 in first differences.",
                    "The original SDG result was 64 of 151 and 3 of 151. Whatever "
                    "produces the asymmetry, it is not the design of the SDG "
                    "indicator set.",
                ],
                "figure": "collapse_hdi_shdi_whr.png",
                "caption": "Countries with an FDR-significant development–happiness "
                           "association, levels versus first differences, for the HDI "
                           "and for the Global Data Lab's subnational HDI aggregated "
                           "to the national level.",
            },
            {
                "label": "Replication 2 · a second producer",
                "heading": "A different institution's index, built differently, gives the same numbers",
                "body": [
                    "The Global Data Lab constructs its subnational HDI from "
                    "household surveys rather than from the national accounts "
                    "and administrative series the UNDP uses. Aggregated back to "
                    "the national level it gives 66 of 148 in levels and 6 of 148 "
                    "in differences — within sampling noise of both the HDI and "
                    "the SDG results.",
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
            "The commentary can therefore state the asymmetry as a property of "
            "the development–wellbeing relationship rather than of any "
            "particular index, and move on to the question that actually "
            "matters: given that almost nothing survives the move to "
            "within-country change, what carries the level signal?"
        ),
    },
    {
        "numeral": "II",
        "title": "Education is the odd one out — under one specific measurement",
        "key_numbers": [
            ("12.7%", "SDG4 access &amp; participation, un-pooled from 3.3%"),
            ("40.9%", "of countries, HDI mean years of schooling"),
            ("32 / 36", "countries, ESS respondents' own attainment"),
        ],
        "thesis": (
            "Ranked indicator by indicator, what predicts happiness in levels "
            "is survival and basic infrastructure. Education looks like the "
            "SDG framework's weakest domain and the HDI's strongest. Both "
            "readings are correct, because the two frameworks are not "
            "measuring the same thing."
        ),
        "beats": [
            {
                "label": "The autopsy",
                "heading": "What survives in levels is the raw development gradient",
                "body": [
                    "Ranking all 609 SDG series by the share of countries in "
                    "which they are FDR-significant puts child mortality, "
                    "stunting, water and sanitation, and access to financial "
                    "services at the top. These are survival and basic "
                    "infrastructure — the steep part of the development curve, "
                    "not the 2030 Agenda's institutional superstructure.",
                    "The best-performing education indicator ranks about "
                    "hundredth. In first differences, only 9 of 609 series have "
                    "even one significant country, which is why there is no "
                    "differences ranking to report at all.",
                ],
                "figure": "sdg_indicator_top20.png",
                "caption": "The 20 highest-ranking SDG series of 609, by share of "
                           "countries FDR-significant in levels.",
            },
            {
                "label": "The contradiction",
                "heading": "Yet inside the HDI, education is the strongest domain",
                "body": [
                    "Mean years of schooling is FDR-significant against World "
                    "Happiness Report happiness in 40.9% of countries and "
                    "expected years of schooling in 33.6%, against 40.0% for GNI "
                    "per capita and 19.3% for life expectancy. Education "
                    "supplies two of the HDI's three strongest components; "
                    "pooled SDG4 sits at 3.3%. This is the sharpest disagreement "
                    "between the two frameworks anywhere in the project.",
                ],
                "figure": "hdi_vs_sdg_frameworks.png",
                "caption": "The same domains under both frameworks. Absolute levels "
                           "are not directly comparable across frameworks; the "
                           "within-framework rankings are the safer read.",
            },
            {
                "label": "The resolution",
                "heading": "SDG4's 3.3% describes no construct that exists",
                "body": [
                    "SDG4's 35 official series do not measure one thing. "
                    "Eighteen of them are equity or parity ratios — gender, "
                    "location, or wealth parity indices — which is a different "
                    "quantity from the level of access. Six measure learning "
                    "outcomes, seven measure infrastructure and inputs, and only "
                    "two measure access and participation directly.",
                    "Split by construct, access and participation reaches 12.7%, "
                    "comparable to SDG3 health at 11.5%, while learning outcomes "
                    "sit at 0.9% and parity ratios at 2.5%. The pooled 3.3% is an "
                    "average across constructs that point in different "
                    "directions, and it describes none of them. That is a "
                    "methodological finding in its own right: pooling within a "
                    "goal can manufacture a null.",
                ],
                "figure": "sdg4_unpooled.png",
                "caption": "SDG4 split by what each indicator actually measures, "
                           "with the pooled figure marked.",
            },
            {
                "label": "All the way down",
                "heading": "The signal survives to the individual respondent",
                "body": [
                    "ESS respondents' own educational attainment predicts their "
                    "own life satisfaction in 32 to 34 of 36 countries, depending "
                    "on whether attainment is measured as the harmonised ISCED "
                    "category or as years completed. The effects are small — "
                    "median R² around 0.01 — but nothing else in this project is "
                    "that consistent across countries.",
                ],
                "figure": "ess_individual_education.png",
                "caption": "Per-country tests of respondents' own attainment against "
                           "their own life satisfaction, 36 ESS countries.",
            },
            {
                "label": "Triangulation",
                "heading": "Two surveys, two outcomes, one answer",
                "body": [
                    "Aggregating ESS respondents' reported years of schooling to "
                    "the country level and regressing World Happiness Report "
                    "happiness on it gives R² = 0.308, against 0.326 for the "
                    "HDI's own mean-years-of-schooling series. Changing both the "
                    "education source and the wellbeing outcome leaves the "
                    "relationship essentially where it was.",
                ],
                "figure": "ess_triangulation.png",
                "caption": "Country-aggregated ESS schooling against WHR happiness, "
                           "beside the HDI's own schooling component.",
            },
            {
                "label": "The composite",
                "heading": "The three panels the commentary needs",
                "body": [
                    "Commentaries carry one or two display items, so the three "
                    "results that carry the argument have to share a figure: the "
                    "replicated collapse, SDG4 un-pooled, and education's signal "
                    "as the unit of measurement moves from pooled indicators "
                    "down to individual respondents.",
                    "One caution to keep in the caption: panel c's rows do not "
                    "share a denominator. It shows that the construct holds at "
                    "every level of aggregation, not that the effect grows.",
                ],
                "figure": "Figure1_commentary.png",
                "caption": "Proposed Figure 1 for submission. Draft — panel c's "
                           "denominators differ by row and are labelled at right.",
                "feature": True,
            },
        ],
        "close": (
            "The precise claim, and the one the commentary must not overstate: "
            "education is not an exception to the differences collapse. Almost "
            "nothing is. Education is the exception in consistency — the one "
            "construct whose level signal holds across frameworks, producers, "
            "wellbeing instruments, and units of observation all the way down "
            "to the individual, and it holds only when education is measured "
            "as attainment and access."
        ),
    },
    {
        "numeral": "III",
        "title": "Scale changes which lever matters",
        "key_numbers": [
            ("+0.89 → +0.15", "development, between countries → within them"),
            ("+0.51", "self-rated health, within countries"),
            ("3 / 16", "countries with a significant regional gradient"),
        ],
        "thesis": (
            "Everything above compares countries. Inside countries the "
            "ordering of predictors is different — which matters, because "
            "most education and health policy is made at the subnational "
            "scale."
        ),
        "beats": [
            {
                "label": "Dispersion",
                "heading": "Below the top tier, countries contain multitudes",
                "body": [
                    "Germany's regions span 0.05 of subnational HDI. China's "
                    "span 0.30 and India's 0.19 — several development tiers' "
                    "worth of variation inside single countries. National "
                    "averages hide most of the development story precisely where "
                    "development varies most.",
                ],
                "figure": "shdi_within_country_spread.png",
                "caption": "Every region a dot, two countries per UNDP development "
                           "tier, 2022.",
            },
            {
                "label": "The non-result",
                "heading": "Development inequality mostly does not become wellbeing inequality",
                "body": [
                    "Holding country fixed and regressing region-mean life "
                    "satisfaction on regional subnational HDI gives a "
                    "significantly positive gradient in only 3 of 16 ESS "
                    "countries — France, Belgium, and Germany — and the gradient "
                    "is not steeper in countries with larger internal "
                    "inequality. Which country's ladder you are on matters more "
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
                    "a median regional correlation of +0.15, significant in 3 of "
                    "16 countries, while self-rated health holds at +0.51 "
                    "(8 of 16) and social trust at +0.49 (6 of 16). The World "
                    "Happiness Report cannot see this at all — it has no "
                    "subnational values. It is the specific thing the ESS adds.",
                ],
                "figure": "ranking_flip.png",
                "caption": "Candidate Figure 2. National correlations beside "
                           "within-country regional correlations, for development, "
                           "health, and trust.",
                "feature": True,
            },
            {
                "label": "The limitation",
                "heading": "This part of the argument is Europe-only, and has to say so",
                "body": [
                    "The ESS is the only regional wellbeing source with the "
                    "coverage this design needs; Gallup's subnational files are "
                    "paywalled. Act III therefore generalises across 16 European "
                    "countries and not beyond them. It should be stated as a "
                    "scope condition in the text rather than buried in a "
                    "limitations paragraph, because the flip is the most "
                    "policy-relevant result in the commentary and will be the "
                    "most contested.",
                ],
            },
        ],
        "close": (
            "Two different policy readings follow depending on scale, and the "
            "commentary should say both. Between countries, raising human "
            "development is where wellbeing differences live. Inside a "
            "country, equalising regional development is not obviously a "
            "wellbeing lever, while health and social connection are."
        ),
    },
    {
        "numeral": "IV",
        "title": "The question we are putting to the field",
        "key_numbers": [
            ("12.7%", "access &amp; participation"),
            ("2.5%", "equity / parity ratios"),
            ("0.9%", "measured learning outcomes"),
        ],
        "thesis": (
            "If the wellbeing return to education runs through attainment and "
            "access rather than through measured learning, then either the "
            "post-2030 education architecture is optimising for the wrong "
            "outcome, or wellbeing is the wrong outcome to hold it to. The "
            "field should have to say which."
        ),
        "beats": [
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
                    "way. Attainment and access carry the wellbeing signal — "
                    "12.7% for SDG4 access, 33.6% and 40.9% for the HDI's "
                    "schooling components, 32 of 36 countries at the individual "
                    "level — while measured learning outcomes sit at 0.9% and "
                    "parity ratios at 2.5%.",
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
                "heading": "Should wellbeing be a criterion for education targets after 2030?",
                "body": [
                    "That is the question the commentary exists to pose, and it "
                    "has a sharp form: we have built a global education "
                    "monitoring architecture around measured learning outcomes, "
                    "and the wellbeing evidence points at years attained. If "
                    "both are to be kept, someone has to say what the education "
                    "system is being optimised for.",
                    "A commentary cannot settle that. It can put the "
                    "disagreement on the record with the evidence attached, "
                    "which is what the four acts are for.",
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
    ("Scope of Act III",
     "Does the within-country material belong in this commentary or in a "
     "third paper? It is the most policy-relevant and the most contested, "
     "and it is Europe-only."),
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
    ("sdg_by_goal.png", "SDG significance by goal, pooled",
     "The leading goal (Energy, 16.0%) clears FDR significance in barely one "
     "country-test in six; pooled Education ranks 11th of 16."),
    ("shdi_vs_hdi_validation.png", "Subnational HDI validated against the UNDP HDI",
     "National aggregates agree closely, which is what licenses the "
     "region-level analysis."),
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
     "filled markers are p &lt; .05. Sweden is the odd one out, negative on "
     "all three."),
]
