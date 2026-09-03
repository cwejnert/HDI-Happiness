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
    "is high but not when it rises — on education and health, which each "
    "track lived experience once measured somewhere they still move, and on "
    "what changes when the question moves inside countries"
)
DATELINE = "Working synthesis for the co-author team · August 2026"
SCOPE = (
    "SDG: 42 countries, 661 series · HDI × World Happiness Report: 151 "
    "countries, 2011–2023 · Subnational HDI &amp; sub-indices: 239 regions · European Social "
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
        "when each is compared with its own past. Thirty of 42 countries are "
        "significant in levels. Two are in year-to-year changes.",
        "There is an obvious way to dismiss that. The SDG framework is a "
        "sprawling, negotiated instrument with uneven coverage; a null inside "
        "it says as much about the framework as about the world. This "
        "commentary closes that escape route, then asks what the result "
        "actually raises: which parts of development track lived experience "
        "at all?",
        "Where it lands is a disconnect rather than an indictment. These "
        "frameworks were built to track development and they do. But the "
        "components that look most consequential for how individuals "
        "experience their lives are the ones development measurement is "
        "currently least arranged to see.",
    ],
    "acts": [
        ("I", "We replicate the SDG result outside the SDGs.",
         "The same design on the HDI, against a second wellbeing survey, and "
         "one spatial scale down. It collapses every time."),
        ("II", "Education, health, and the blind spots.",
         "Education's rank swings on construct, health's on saturation, and "
         "the whole ranking turns over again once the question moves from "
         "between countries to inside them."),
        ("III", "Which points to a disconnect worth naming.",
         "Not that these frameworks should stay away from wellbeing, but that "
         "the components that track lived experience are ones they are not "
         "currently arranged to see."),
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
        "title": "Education, health, and what changes when you change the question",
        "key_numbers": [
            ("40.7% → 8 of 16", "education: leads the HDI between countries, inconsistent inside them"),
            ("12.7%", "SDG4 access alone — third of 17 goals if it were one"),
            ("19.9% → +0.51", "health: last of the HDI's five, first inside countries"),
            ("1 of 16", "SDG trust country-series testable at all, not 1 of 163"),
        ],
        "thesis": (
            "Two results and a discussion. Education leads the HDI and the "
            "access construct of SDG4 and is the smallest effect anywhere. "
            "Health leads the SDG framework and the individual data and is "
            "weak in exactly one place, for a reason we can name. Social trust "
            "leads wherever it is measured, which is almost nowhere. Every "
            "disagreement between the frameworks turns out to be about "
            "operationalisation — and the ranking changes again, in a "
            "consistent direction, when the question moves from between "
            "countries to inside them."
        ),
        "beats": [
            {
                "label": "Framework against framework",
                "heading": "Three comparisons, and they do not all point the same way",
                "body": [
                    "No single statistic settles which framework tracks "
                    "wellbeing better, so the commentary should report three "
                    "and nominate none. <strong>Detection</strong>: does any "
                    "indicator show a significant levels association in a given "
                    "country? The SDG framework reaches 30 of its 42 countries "
                    "(71%), the HDI 77 of its 150 (51%). Benjamini–Hochberg "
                    "under the complete null controls the error rate at the "
                    "same α whatever the family size, so the SDG lead is "
                    "genuine power bought with breadth and should be conceded "
                    "as such.",
                    "<strong>Budget-matched</strong>: give the SDG framework "
                    "the same five-indicator budget the HDI gets, drawn at "
                    "random, 4,000 times. Five random SDG series reach 30% of "
                    "countries (95% range 19–40%); the HDI’s chosen five reach "
                    "40% on the same countries — better than a random five, "
                    "but at the top <em>edge</em> of the random range rather "
                    "than outside it.",
                    "<strong>Per indicator</strong>: across the 609 SDG series "
                    "with usable coverage the median series is significant in "
                    "no country at all, and 54% never clear FDR anywhere. The "
                    "HDI composite, mean schooling and GNI per capita each beat "
                    "essentially the whole field; even life expectancy, the "
                    "HDI’s weakest component, beats 90% of it.",
                    "That is the frame for what follows. The three results come "
                    "in the order of how much the frameworks disagree about "
                    "them: education, where the disagreement is total and "
                    "entirely about construct; health, where it is large and "
                    "entirely about saturation; and social trust, where one "
                    "framework cannot see the domain at all.",
                ],
                "figure": "framework_three_comparisons.png",
                "caption": "Each framework on its own full country set against WHR "
                           "happiness, except panel b which restricts the HDI to the "
                           "42 SDG countries so the budgets are comparable.",
                "feature": True,
            },
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
                    "alive and not being sick — rather than the 2030 Agenda’s "
                    "institutional superstructure. It also sets up the puzzle "
                    "the next three beats resolve: the instrument that ranks "
                    "health first ranks education twelfth, and the instrument "
                    "that ranks education first ranks health last.",
                ],
                "figure": "sdg_indicator_top20.png",
                "caption": "The 20 highest-ranking SDG series of 609, by share of "
                           "countries FDR-significant in levels.",
            },

            # ---------------- Result 1: education ----------------
            {
                "label": "Result 1 · Education",
                "heading": "The strongest thing the HDI measures",
                "body": [
                    "Mean years of schooling has the highest median R² of the "
                    "HDI’s five indicators — 0.326, fractionally above the "
                    "composite’s own 0.322 — and is FDR-significant in 61 of "
                    "150 countries, 40.7%, the highest of the four "
                    "sub-components. Expected years of schooling follows at "
                    "34.0%. Income is level with schooling at 40.4%; life "
                    "expectancy is far behind at 19.9%.",
                    "A sub-component beating the composite it belongs to is "
                    "worth pausing on. The HDI aggregates health, education and "
                    "income into one number on the assumption that development "
                    "is a bundle. On this test the bundle adds nothing over its "
                    "education leg alone — which is the first hint that the "
                    "index is carried by one of its three domains rather than "
                    "by their combination.",
                ],
            },
            {
                "label": "Result 1 · Education",
                "heading": "In the SDG framework its rank depends entirely on which construct you read",
                "body": [
                    "Pooled, SDG4 is close to the bottom: 3.3% of "
                    "country-indicator pairs significant, twelfth of the "
                    "seventeen goals, with its best single series ranking 100th "
                    "of 609. Read naively the two frameworks flatly contradict "
                    "each other about education.",
                    "They do not, because SDG4 is not one construct. Eighteen of "
                    "its 35 official series are equity or parity ratios, seven "
                    "measure school infrastructure, six measure learning "
                    "outcomes, one measures financing, one attainment — and "
                    "only two measure access and participation directly. Split "
                    "apart, those two reach <strong>12.7%</strong>. Placed among "
                    "the seventeen goals that would rank third, above SDG3 "
                    "health at 11.5%. Meanwhile learning outcomes sit at 0.9% "
                    "and parity ratios at 2.5%, and it is the parity ratios — "
                    "half the goal by series count — that drag the pooled "
                    "figure down.",
                    "So the SDG framework does not disagree with the HDI about "
                    "education. It agrees with it, on the two series that "
                    "measure the same thing the HDI measures, and the "
                    "disagreement is manufactured by pooling six constructs "
                    "that point in different directions. State the caveat "
                    "plainly: access and participation is 2 series and 63 "
                    "country-indicator pairs, a small family, and the 12.7% "
                    "carries correspondingly wide uncertainty.",
                ],
                "figure": "sdg4_unpooled.png",
                "caption": "SDG4 split by what each indicator actually measures, with "
                           "the pooled figure marked.",
                "feature": True,
            },
            {
                "label": "Result 1 · Education",
                "heading": "And at the individual level it is significant almost everywhere, if barely",
                "body": [
                    "Respondents’ own attainment predicts their own life "
                    "satisfaction in 32 to 34 of 36 ESS countries — more "
                    "consistent across countries than anything except health. "
                    "Aggregated to the country level, ESS-measured years of "
                    "schooling predicts WHR happiness at R² = 0.308 against "
                    "0.161 for the HDI’s own schooling series on the same "
                    "cells, so an independently measured education variable "
                    "roughly doubles the HDI’s.",
                    "What it does not have is size. The median individual R² is "
                    "0.0098, the smallest of any domain tested. Education is "
                    "the most universal signal and the smallest one — an odd "
                    "combination, and one the third result explains.",
                ],
                "figure": "ess_individual_education.png",
                "caption": "Per-country tests of respondents’ own attainment against "
                           "their own life satisfaction, 36 ESS countries.",
            },

            # ---------------- Result 2: health ----------------
            {
                "label": "Result 2 · Health",
                "heading": "The strongest thing the SDG framework measures",
                "body": [
                    "Goal 3 reaches 11.5% of country-indicator pairs, fourth of "
                    "the seventeen goals and first among the goals with broad "
                    "coverage — the three above it are energy (5 series), "
                    "industry and infrastructure (23), and hunger and nutrition "
                    "(53), against Goal 3’s 45. Sixteen of the top 25 series in "
                    "the whole database are health.",
                    "The health series that carry the signal are survival "
                    "measures: child and neonatal mortality, stunting, safely "
                    "managed water and sanitation. None is self-reported, which "
                    "matters for the method check two beats on — this is the "
                    "one domain where an administrative source and a "
                    "self-report source can be set against each other.",
                ],
                "figure": "sdg_by_goal.png",
                "caption": "All 17 goals by share of country-indicator pairs "
                           "FDR-significant in levels.",
            },
            {
                "label": "Result 2 · Health",
                "heading": "Why the HDI says the opposite, and why the HDI is wrong about it",
                "body": [
                    "Inside the HDI, life expectancy is the weakest of the five "
                    "indicators by a wide margin — 30 of 151 countries, 19.9%, "
                    "against 40.7% for mean schooling. Read naively the HDI says "
                    "health is the least important thing about development, and "
                    "the SDG framework says it is the most important.",
                    "The reconciliation is saturation, and it is checkable "
                    "rather than rhetorical. Life expectancy has run out of "
                    "variance across the countries where it is tested; the "
                    "variance that would let it predict anything has largely "
                    "gone. The SDG series that do carry health’s signal are the "
                    "ones that still vary enormously — child mortality, "
                    "stunting — and self-rated health captures morbidity that "
                    "life expectancy cannot see at all.",
                    "This is the same failure mode as education’s, running in "
                    "the opposite direction. Education’s rank collapses when a "
                    "framework measures it as parity rather than attainment; "
                    "health’s collapses when a framework measures it with a "
                    "variable that has no room left to move. Neither is a fact "
                    "about the world.",
                ],
            },
            {
                "label": "Result 2 · Health",
                "heading": "It leads the individual data too, and it is the one domain that passes the method check",
                "body": [
                    "In the ESS, self-rated health is significant in 36 of 36 "
                    "countries with a median R² of 0.091 — roughly nine times "
                    "education’s 0.0098, and the largest effect of any domain "
                    "tested anywhere in this commentary.",
                    "Self-rated health is reported by the same respondent, in "
                    "the same survey, as life satisfaction, so shared method "
                    "variance is the first objection a reader will raise. "
                    "Health is the one domain that can answer it: the UN SDG "
                    "database is administrative and shares no method with any "
                    "wellbeing instrument. Restricted to high-income countries "
                    "— the same development stratum the ESS covers — the SDG "
                    "data puts health at 11.2% of pairs against education’s "
                    "1.2%, the same ordering the ESS gives from entirely "
                    "different measurement.",
                    "The regional test in the next beat adds a second external "
                    "check: GDL’s externally measured health index leads its "
                    "education and income indices within countries too. Health "
                    "therefore holds under administrative measurement at both "
                    "the national and the regional scale, which is more than "
                    "can be said for either of the other two domains.",
                ],
                "figure": "health_trust_corroboration.png",
                "caption": "The same domains under an administrative source and a "
                           "self-report source.",
                "feature": True,
            },

            # ---------------- The synthesis across specifications ----------------
            {
                "label": "The horse race",
                "heading": "Run the domains against each other inside one instrument",
                "body": [
                    "The ESS measures health, education, income and trust on the "
                    "same respondents as life satisfaction, so the domains can "
                    "compete on equal terms rather than through four separate "
                    "literatures. Health leads at every level of aggregation; "
                    "education is significant nearly everywhere and small "
                    "everywhere; trust sits between them.",
                    "The HDI leads between countries at R² = 0.760, but that is "
                    "the one comparison a composite index is expected to win — "
                    "it proxies every domain at once. It falls to fourth once "
                    "you look inside countries, and that fall is the subject of "
                    "the next beat.",
                ],
                "figure": "domain_horse_race.png",
                "caption": "Domains competing within one instrument, at three levels "
                           "of aggregation.",
            },
            {
                "label": "Levels, differences, and inside countries",
                "heading": "Three specifications, and the ranking changes twice",
                "body": [
                    "Three tests run through this commentary and the reader has "
                    "been left to join them up. They are not three attempts at "
                    "one question. <strong>Levels</strong> asks whether a "
                    "country with more of something is happier. "
                    "<strong>Differences</strong> asks whether a country that "
                    "gains it gets happier — the collapse of Act I. "
                    "<strong>Inside one country, across its regions</strong> "
                    "asks whether the places with more of it are the better "
                    "places to live, holding national institutions, history and "
                    "policy fixed.",
                    "Education leads the first and all but vanishes in the "
                    "third: 40.7% of countries, then no consistent regional "
                    "signal at all — 8 of 16 countries positive, a median "
                    "between −0.08 and +0.13 depending on how region values "
                    "are aggregated, and the significant countries pointing "
                    "both ways. Health and trust do the reverse — health "
                    "last of the HDI’s five between countries, first inside "
                    "them at +0.51; trust unmeasured between, second inside at "
                    "+0.49. The middle panel flattens everything: nothing "
                    "clears 3%.",
                    "The direction of that shift is the finding. What predicts "
                    "<em>where</em> wellbeing is high is structural — schooling "
                    "and income, which between countries proxy the whole "
                    "development bundle at once. What predicts it "
                    "<em>inside</em> a country is experiential: health and "
                    "trust. Education’s combination of near-universal "
                    "significance and tiny effect is exactly what a structural "
                    "variable looks like once the structure is held fixed.",
                ],
                "figure": "L1_three_specifications.png",
                "caption": "Panels (a) and (b) are the same HDI indicators on the same "
                           "150–151 countries, so the collapse between them is exact. "
                           "Panel (c) is a different instrument at a different scale — "
                           "16 ESS countries with ≥6 matched regions — so it is read "
                           "alongside (a) and (b), not subtracted from them. Within it, "
                           "external GDL sub-indices are drawn separately from "
                           "same-survey self-reports, since the shared-method objection "
                           "applies only to the latter; health leads on both.",
                "feature": True,
            },

            # ---------------- Result 3: social trust, in discussion ----------------
            {
                "label": "Discussion · Social trust",
                "heading": "The interesting case, and the one the measurement apparatus handles worst",
                "body": [
                    "Trust is not a headline result here and should not be "
                    "presented as one — it rests on a single instrument with a "
                    "live shared-method caveat. It is in the paper because the "
                    "reason it cannot be a headline is itself the "
                    "commentary’s subject.",
                    "Where it is measured it performs: significant in 34 of 36 "
                    "ESS countries individually, +0.49 within countries across "
                    "regions, second only to health on both and above education "
                    "on both. Neither the HDI nor the subnational HDI measures "
                    "it at all.",
                    "The SDG framework appears to: 13 trust- and "
                    "satisfaction-adjacent series, mostly Goal 16 — "
                    "satisfaction with public services, belief that "
                    "decision-making is inclusive, bribery prevalence. But their "
                    "median coverage is <em>one year</em> per country-series "
                    "against six database-wide. The design needs at least four "
                    "years; 147 of the 163 country-series fall short and are "
                    "never computed at all. Of the 16 that can be run, 1 is "
                    "significant.",
                    "Report that as “1 of 16 testable”, never “1 of 163”. The "
                    "latter reads as a null when it is overwhelmingly a "
                    "coverage gap — and reporting a coverage gap as a null "
                    "would repeat the exact error this commentary accuses the "
                    "frameworks of making.",
                ],
            },
            {
                "label": "Discussion · Social trust",
                "heading": "Tested the only way its coverage allows, and it still does not become a result",
                "body": [
                    "One year per country is useless longitudinally and "
                    "perfectly usable cross-sectionally, so we pulled the raw "
                    "values from the UN SDG database and ran the series against "
                    "the ladder across countries. Nine of the 13 clear a "
                    "12-country minimum and four are significant: bribery paid "
                    "by individuals (−0.55) and firms (−0.51), inclusive "
                    "decision-making (−0.42), satisfaction with healthcare "
                    "(+0.33).",
                    "Three things stop that being a rescue. Every one of the "
                    "four is weaker than what the frameworks already carry — on "
                    "the same 134 countries the HDI and its components sit at "
                    "|r| 0.71–0.83. The broadest series, satisfaction with "
                    "healthcare, is Gallup World Poll, the same survey that "
                    "produces the ladder. And none of the 13 measures "
                    "interpersonal trust: they measure institutional "
                    "confidence, a different construct.",
                    "Income control kills all nine — but it also kills the HDI "
                    "(+0.82 raw, +0.09 net). No cross-section of countries "
                    "separates anything from income, which is why the "
                    "levels-and-differences design exists, and the panel says so "
                    "to stop the null being read as trust-specific.",
                ],
                "figure": "K1_sdg_trust_cross_section.png",
                "caption": "Nine of the 13 SDG trust- and satisfaction-adjacent series, "
                           "one observation per country, against the WHR Cantril ladder. "
                           "Raw values pulled from the UN SDG Global Database API.",
            },

            # ---------------- Pulling it together ----------------
            {
                "label": "The synthesis",
                "heading": "The pattern of blind spots is the result",
                "body": [
                    "Laid out side by side, the three domains have three "
                    "signatures. Education leads the HDI and the access "
                    "construct of SDG4, is near-universal at the individual "
                    "level, and is the smallest effect anywhere — a structural "
                    "variable behaving exactly as one should. Health leads the "
                    "SDG framework, the individual data and the regional data, "
                    "and is weak in precisely one place, the HDI, for a reason "
                    "we can name. Trust leads nothing it is not the only "
                    "candidate for, and is invisible to every development "
                    "framework.",
                    "None of these disagreements is about the world. Every one "
                    "is about an operationalisation choice — which construct, "
                    "which variable, which specification — which is why the "
                    "contribution is not a ranking of domains but an account of "
                    "why the rankings differ.",
                ],
                "figure": "domain_scorecard.png",
                "caption": "The three domains against the five instruments. Metrics "
                           "differ by column and are given under each heading; the "
                           "colours encode whether the domain tracks wellbeing there, "
                           "shows little signal, or cannot be tested at all.",
                "feature": True,
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
            "Education leads once it is measured as attainment rather than "
            "parity; health leads once it is measured somewhere it still "
            "varies; trust leads wherever it is measured at all, which is "
            "almost nowhere. And the ranking turns over a second time when the "
            "question moves inside countries. The contribution is not a ranking "
            "of domains but the demonstration that the ranking depends on "
            "construct, on variable, and on specification — none of which the "
            "frameworks chose with wellbeing in mind, because that is not what "
            "they were built for. Which is what makes the third act a question "
            "about fit rather than a charge of failure."
        ),
    },
    {
        "numeral": "III",
        "title": "What this may imply for how development is measured",
        "key_numbers": [
            ("+0.87 → +0.12", "development, between countries → within them"),
            ("8 of 16 vs 12 of 16", "countries where education vs health tracks wellbeing regionally"),
            ("11.2% vs 1.2%", "health vs education, SDG data, high-income countries"),
        ],
        "thesis": (
            "These are implications, not recommendations. The frameworks were "
            "not built to track wellbeing and it is no criticism of them that "
            "they do not; measured against their own purposes they work. What "
            "the three results describe is a <em>disconnect</em> — between what "
            "development measurement currently captures and what turns out to "
            "track individual lived experience. If wellbeing is to be part of "
            "what these frameworks are for, education, health and social trust "
            "each say something specific about what capturing it would take."
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
                    "(8 of 16) and social trust at +0.49 (6 of 16). Education "
                    "falls with development, not with health and trust — and "
                    "further: its correlations are positive in only 8 of 16 "
                    "countries, and the three that reach significance point "
                    "both ways (Austria −0.81, France +0.50, the Netherlands "
                    "+0.60). The World Happiness Report cannot see any of this "
                    "— it has no subnational values. It is the specific thing "
                    "the ESS adds.",
                    "This is Act II's third panel at full detail: the domains "
                    "that lead between countries are the structural ones, and "
                    "they are not the domains that lead inside them.",
                    "Two cautions. The health-versus-trust ordering is not "
                    "stable — aggregating region means across waves rather "
                    "than within them reverses it (trust +0.57, health +0.50). "
                    "What is stable is that both sit near +0.5 while "
                    "development and education sit at zero. And coverage varies "
                    "sharply: Italy matches 30% of respondents to a region, "
                    "Sweden 57%, Croatia 69%, against 91–100% elsewhere. "
                    "Dropping those three, or regions built on under 200 "
                    "respondents, leaves the flip intact.",
                ],
                "figure": "ranking_flip.png",
                "caption": "Candidate Figure 2. National correlations beside "
                           "within-country regional correlations, for development, "
                           "health, and trust.",
                "feature": True,
            },
            {
                "label": "The flip, externally measured",
                "heading": "It survives with no self-report at all — and it is a health flip",
                "body": [
                    "The strongest objection to the ranking flip is that health "
                    "and trust are reported by the same respondents as the "
                    "outcome. GDL's regional sub-indices remove that objection: "
                    "health, education and income indices measured per region "
                    "from external sources, sharing no method with the ESS.",
                    "Within countries, the external health index correlates "
                    "with regional life satisfaction at a median of +0.34, "
                    "significant in 6 of 15 usable countries, against +0.12 for "
                    "the income index and +0.06 for the education index. The "
                    "domain ordering is the same one the self-reports give, "
                    "from measurement the respondents never touched. Self-rated "
                    "health still runs higher (+0.50), which is exactly what "
                    "you expect if part — but only part — of its lead is shared "
                    "method variance. One country drops out: Albania's regional "
                    "health index is constant, another instance of a measure "
                    "with no variance left to predict with.",
                ],
                "figure": "within_country_external.png",
                "caption": "The within-country domain race with externally measured "
                           "predictors (solid) beside the same-survey self-reports "
                           "(faded). Sub-indices pooled 2010–2023.",
                "feature": True,
            },
            {
                "label": "The disconnect",
                "heading": "Stating it precisely, and stating what it is not",
                "body": [
                    "Development indicators tell you reliably where wellbeing is "
                    "high. They tell you almost nothing about when it will rise. "
                    "Across every framework tested here, year-on-year indicator "
                    "movement carries essentially no wellbeing information within "
                    "the measurement window — a decade or so — and inside "
                    "countries the domains that lead between them stop leading.",
                    "It is worth being explicit about what that is not. It is "
                    "not an argument that development frameworks should be kept "
                    "away from wellbeing, or that they have failed. The HDI and "
                    "the SDGs were built to track development — capability, "
                    "deprivation, the 2030 Agenda's negotiated priorities — and "
                    "on those terms they work. Nothing here says otherwise.",
                    "What the results describe is a disconnect between two "
                    "things that are often assumed to move together: what these "
                    "frameworks currently capture, and what tracks how "
                    "individuals experience their lives. That assumption is "
                    "reasonable and mostly untested. Tested, it holds between "
                    "countries and weakens sharply everywhere else.",
                    "So the useful question is not whether development matters. "
                    "It is which components of it track lived experience, and "
                    "whether the frameworks are currently in a position to see "
                    "them. The next three beats take the three results in turn.",
                ],
            },
            {
                "label": "Implication 1 · Education",
                "heading": "Which education construct a framework counts turns out to matter",
                "body": [
                    "Global education policy has shifted decisively over the "
                    "past decade from schooling to learning — the "
                    "learning-crisis framing, learning-poverty targets, an "
                    "indicator architecture built around measured proficiency. "
                    "That shift has good reasons behind it that have nothing to "
                    "do with wellbeing, and this commentary does not dispute "
                    "them.",
                    "It does observe that the wellbeing signal sits elsewhere. "
                    "Attainment and access carry it — 12.7% for SDG4 access, "
                    "40.7% and 34.0% for the HDI's schooling components, 32 of "
                    "36 countries at the individual level — while measured "
                    "learning outcomes sit at 0.9% and parity ratios at 2.5%. A "
                    "framework that reads SDG4 pooled will conclude education "
                    "barely matters for wellbeing; one that reads the access "
                    "series will rank it third of seventeen goals. Same data, "
                    "same countries.",
                    "Two cautions travel with this and it is weaker without "
                    "them. Education is the most consistent signal and the "
                    "smallest one. And it is a <em>between</em>-country signal: "
                    "inside countries it has no consistent signal at all, "
                    "positive in 8 of 16 and negative in 8. So the implication "
                    "is about what a global "
                    "monitoring framework counts, not a claim that moving one "
                    "region's schooling moves its wellbeing.",
                ],
            },
            {
                "label": "Implication 2 · Health",
                "heading": "A domain can disappear from a framework by being measured where it has stopped moving",
                "body": [
                    "Life expectancy is the standard summary of population "
                    "health and the HDI's only health input, and it is the "
                    "weakest of the five against wellbeing. Health is "
                    "simultaneously the strongest domain in the SDG database "
                    "and in the individual data. The gap between those two "
                    "facts is not substantive; it is that life expectancy has "
                    "largely stopped varying across the countries where it is "
                    "tested.",
                    "What still carries health's signal is survival at the "
                    "margin — child, infant and neonatal mortality, stunting, "
                    "sanitation, safe water — and, in richer countries, "
                    "self-rated health, which picks up morbidity and functional "
                    "limitation that life expectancy cannot see. Both are "
                    "already collected. The implication is about which of them "
                    "a framework reads as its health signal in a high-income "
                    "setting, not about adding a new instrument.",
                    "Health is also where the scale point runs the other way "
                    "from education's: weak between countries and strong inside "
                    "them. A subnational health measure is doing work a national "
                    "one cannot, which suggests disaggregation matters here as "
                    "much as indicator choice.",
                ],
            },
            {
                "label": "Implication 3 · Social trust",
                "heading": "A component that looks important, and that no framework is currently positioned to check",
                "body": [
                    "Social trust is at or near the top of every test the ESS "
                    "can run — 34 of 36 countries, +0.49 within countries — and "
                    "no development framework can currently check it. The HDI "
                    "and subnational HDI do not measure the construct. The SDG "
                    "framework's 13 satisfaction and integrity series average "
                    "one observation per country, which supports no "
                    "longitudinal design.",
                    "We did not stop at asserting that. Act II runs those series "
                    "the only way their coverage permits, across countries "
                    "rather than years: 9 are testable, 4 significant, and all "
                    "four land below the HDI's own components on the same "
                    "countries. So the gap is a real gap, established rather "
                    "than assumed.",
                    "The implication is the most tentative of the three, and "
                    "should be presented that way. Trust rests on one "
                    "instrument, in Europe, with a live shared-method caveat. "
                    "What can be said is narrow and still useful: a component "
                    "that performs this well wherever it is measured is "
                    "currently invisible to development measurement, and it is "
                    "invisible for reasons of coverage rather than because it "
                    "was weighed and found wanting. A repeated generalised-trust "
                    "item — already standard in the ESS, the World Values Survey "
                    "and several national statistical series — would be enough "
                    "to find out.",
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
                "label": "Where this leaves it",
                "heading": "Development frameworks may need to work harder at capturing what shapes lived experience",
                "body": [
                    "That is the conclusion, and it is deliberately exploratory. "
                    "Three components look consequential for how individuals "
                    "experience their lives — education, health, social trust — "
                    "and each is currently captured in a way that makes it hard "
                    "for a development framework to see. Education is pooled "
                    "with constructs that point the other way. Health is read "
                    "through a variable that has largely stopped moving. Social "
                    "trust is not measured with the coverage any longitudinal "
                    "design requires.",
                    "None of that is a demand that these frameworks become "
                    "wellbeing instruments. It is the narrower observation that "
                    "if wellbeing is to inform what development measurement "
                    "counts — and the post-2030 conversation suggests it may — "
                    "then the first question is not which domain to prioritise "
                    "but whether each is being measured somewhere it can still "
                    "move. On the evidence here, for at least two of the three, "
                    "it is not.",
                    "The honest form of the ask is a question rather than a "
                    "prescription: what would a development framework look like "
                    "if the components that track individual lived experience "
                    "were among the things it was built to capture? A "
                    "commentary cannot answer that. It can show that the "
                    "question is not rhetorical, and put the evidence on the "
                    "record so the field can take it up.",
                ],
            },
        ],
        "close": (
            "The recommended framing for submission: lead with education as "
            "the positive finding, use the generalised collapse as the backdrop "
            "that makes it surprising, and close on the disconnect rather than "
            "on a list of fixes. That ordering makes Act I load-bearing without "
            "making it the story, and it keeps the paper on the ground it can "
            "actually defend — that these components look like they matter for "
            "lived experience, and that development measurement is not "
            "currently arranged to see them."
        ),
    },
]

# --------------------------------------------------------------------------
# Decisions for the co-author team
# --------------------------------------------------------------------------
DECISIONS = [
    ("Framing",
     "Lead with education and use the generalised collapse as Act I backdrop "
     "— recommended — or lead with the robustness result and treat education "
     "as the coda. This decides title, abstract, and venue."),
    ("How hard to push the conclusion",
     "Act III now lands on a disconnect and an exploratory ask rather than a "
     "list of fixes: these components look like they matter for lived "
     "experience, and development measurement is not currently arranged to "
     "see them. Is that the right altitude for the venue, or should the "
     "health and education implications be sharpened into named "
     "recommendations? The evidence supports either; the framing does not "
     "change the analysis."),
    ("Display items",
     "Commentaries allow one or two. Proposed: the three-panel composite as "
     "Figure 1, the ranking flip as Figure 2. Everything else moves to "
     "supplementary."),
    ("Scope of the within-country work",
     "It now sits inside Act III as the evidence on priorities. Does it "
     "belong there, or in a third paper? It is the most policy-relevant and "
     "the most contested result we have, and it is Europe-only."),
    ("Resolved: subnational sub-indices",
     "The per-domain GDL exports are in. Within countries the external health "
     "index leads education and income (+0.34 vs +0.06 and +0.12), so the "
     "flip no longer rests on self-report. GDL's DHS-based Education &amp; "
     "Work and Health datasets were also examined: they cover only 6 ESS "
     "countries and cannot serve the European design."),
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
