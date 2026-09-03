"""
The commentary, structured in three acts — step-by-step through the evidence.

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
    "A commentary in three acts. What tracks individual lived experience "
    "when development is measured: education, health, and social trust. And why "
    "the frameworks built to monitor development systematically miss some of them."
)
DATELINE = "Working synthesis for the co-author team · September 2026"
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
        "commentary closes that escape route by asking: which parts of "
        "development track lived experience at all? And why do some frameworks "
        "capture them while others systematically miss them?",
        "The answer turns out to be about the frameworks' construction choices, "
        "not about development itself. Education, health, and social trust all "
        "matter — but which one you find depends on which framework you measure "
        "with, which construct you count, and whether you collected the data "
        "in the first place.",
    ],
    "acts": [
        ("I", "The levels-to-differences collapse is universal.",
         "Replicate it on the HDI, against a second wellbeing survey, and one spatial scale down. "
         "It holds every time. So we can analyze the levels."),
        ("II", "At the levels, three domains emerge: education, health, and social trust.",
         "But each framework sees a different subset, for a different reason: the wrong construct, "
         "a variable that stopped varying, or no coverage at all."),
        ("III", "What this means for how we measure development.",
         "A disconnect between what frameworks capture and what predicts lived experience, "
         "with implications for each domain."),
    ],
}

# --------------------------------------------------------------------------
# Acts
# --------------------------------------------------------------------------
ACTS = [
    {
        "numeral": "I",
        "title": "Replicating the collapse: three frameworks, three data sources",
        "key_numbers": [
            ("71% → 5%", "of countries significant, SDG levels → differences"),
            ("42% → 2%", "the same collapse under the HDI composite"),
            ("14% → 8%", "of cells, against the ESS wellbeing survey"),
        ],
        "thesis": (
            "Run the original levels-and-differences design on a second development "
            "framework, against a second wellbeing instrument, and the collapse "
            "appears every time. It is not a property of the SDGs. Once we show "
            "the levels are where the signal is, we can drill into what that signal "
            "actually is."
        ),
        "close": (
            "The levels are where development and wellbeing predict each other. "
            "Now we can ask: which components of development matter for lived experience?"
        ),
        "beats": [
            {
                "label": "Replication 1 · the HDI",
                "heading": "A deliberately parsimonious index shows the same collapse",
                "body": [
                    "The Human Development Index is the opposite of the SDG framework in every "
                    "way the dismissal relies on: three dimensions rather than seventeen goals, "
                    "a single custodian, a stable definition, near-universal coverage. "
                    "Substituting it for the SDGs and holding everything else fixed gives "
                    "64 of 151 countries FDR-significant in levels and 3 of 151 in first "
                    "differences — 42% down to 2%.",
                    "The levels-to-differences ratio is identical in order of magnitude "
                    "whether you use the SDGs or the HDI. Whatever produces the asymmetry, "
                    "it is not a property of either framework's scope or construction.",
                ],
                "figure": "collapse_hdi_shdi_whr.png",
                "caption": "Countries with FDR-significant development–happiness association, "
                           "levels versus first differences, under the SDG framework and the HDI.",
            },
            {
                "label": "Replication 2 · the ESS",
                "heading": "Switch the wellbeing measure from the World Happiness Report to the European Social Survey",
                "body": [
                    "The World Happiness Report compiles a single survey question: the Cantril "
                    "ladder, 'how satisfied are you with your life on a scale of 0–10?' The "
                    "European Social Survey asks similar life satisfaction and happiness questions "
                    "of individuals rather than aggregating them to countries.",
                    "Running the same levels-and-differences design against the ESS — 36 European "
                    "countries, 351,000 respondents — shows the collapse holds there too. At the "
                    "individual level, within countries, development composite scores predict "
                    "significant variance in life satisfaction and happiness; year-to-year changes "
                    "in the HDI within countries predict almost none. The levels are where the "
                    "signal is, regardless of the framework or the instrument.",
                ],
                "figure": "ess_levels_diffs_collapse.png",
                "caption": "ESS + HDI: levels-to-differences collapse holds for both life satisfaction "
                           "and happiness at the individual level.",
            },
            {
                "label": "The composite + sub-components",
                "heading": "Beneath the composites, the components tell different stories",
                "body": [
                    "Expected years of schooling leads the HDI: highest median R² at levels "
                    "(0.326) and in differences (0.069), above the composite itself. Income is "
                    "level with it in levels, weaker in differences. Life expectancy — the HDI's "
                    "proxy for health — is weakest in levels.",
                    "Education's apparent strength in levels is not a hint that differences would "
                    "show it recovering. Instead, it is the entry point to Act II: which components "
                    "are actually strong, weak, or invisible once you look at each framework's "
                    "construction choices rather than its top-line numbers?",
                ],
                "figure": "hdi_full_structure.png",
                "caption": "HDI composite and sub-components, levels and first differences. "
                           "Benjamini–Hochberg corrected within each country.",
            },
        ],
    },

    {
        "numeral": "II",
        "title": "What predicts wellbeing at the levels? Three findings.",
        "key_numbers": [
            ("92% vs 34% vs 3.3%", "countries significant: education in ESS, HDI, and SDG4 pooled"),
            ("100% vs 20% vs 11.5%", "countries significant: health in ESS, HDI, and SDG3"),
            ("94% vs 1.5% vs —", "countries significant: social trust in ESS, SDG16, and HDI (not measured)"),
        ],
        "thesis": (
            "Three domains emerge when you ask which indicators of education, health, "
            "and social trust predict life satisfaction at the levels. But each framework "
            "sees a different subset — not because the domains differ across contexts, "
            "but because of three distinct reasons frameworks fail to capture what matters "
            "for lived experience."
        ),
        "close": (
            "Each framework's construction choices — which construct to count, which variable "
            "to measure, which domains to collect at all — determine what it can see. The problem is not "
            "the domains; the problem is the measurement."
        ),
        "beats": [
            {
                "label": "All three matter",
                "heading": "Education, health, and social trust all significantly predict life satisfaction",
                "body": [
                    "In the European Social Survey, where all three are measured at the individual level, "
                    "all three are significant in the majority of countries. But which framework can see "
                    "all three? Which sees only some? The answer depends on three different failure modes.",
                ],
                "figure": "domains_at_levels_comparison.png",
                "caption": "% of countries where each domain significantly predicts wellbeing at levels. "
                           "ESS: 36 countries. HDI: 150 countries. SDG: country-indicator pairs.",
            },

            {
                "label": "Result 1 · Education",
                "heading": "Significant in 92% of ESS countries, but only when measured as attainment",
                "body": [
                    "Expected years of schooling predicts life satisfaction in 34% of HDI countries — "
                    "the highest among the five HDI components, but still a minority. In the ESS individual "
                    "data, education (measured as years attained) is significant in 92% of countries. The "
                    "difference is not about the data; it is about which construct you count.",
                    "The SDG framework's education goal is 35 indicators spanning access, attainment, "
                    "equity (parity ratios), learning outcomes, infrastructure, and financing. Pooled, "
                    "3.3% of country-indicator pairs are significant. But access indicators alone (primary "
                    "and secondary enrollment, completion rates) reach 12.7% — because they measure "
                    "participation, the closest SDG analogue to HDI attainment. Parity ratios, learning "
                    "outcomes, and infrastructure contribute little to wellbeing, so pooling them masks "
                    "the signal from access.",
                ],
                "figure": "education_levels_comparison.png",
                "caption": "Education's R² (% of countries significant at levels) across three frameworks. "
                           "SDG4's pooled rate (3.3%) includes all 35 constructs; access alone reaches 12.7%.",
            },

            {
                "label": "Access check · why education's rank swings",
                "heading": "The difference between measuring attainment and measuring parity",
                "body": [
                    "When the SDG framework pools constructs, it weights all equally by series count. "
                    "Parity ratios are 18 of 35 series but carry almost no signal for wellbeing. Learning "
                    "outcomes (6 series, 0.9% significant), infrastructure (7 series, 2.0%), and financing "
                    "(1 series, 11.5%) together drive the pooled rate below what access alone achieves. "
                    "This is not a discovery about education; it is a mechanical artifact of construction.",
                ],
                "figure": "sdg4_unpooled.png",
                "caption": "SDG4 by construct: access and participation (12.7%) vs. equity/parity ratios "
                           "(2.5%), learning outcomes (0.9%), and others.",
            },

            {
                "label": "Result 2 · Health",
                "heading": "Significant in 100% of ESS countries, weak in the HDI, strong in the SDGs",
                "body": [
                    "Self-rated health is the single strongest predictor of life satisfaction in the ESS: "
                    "100% of countries significant at the individual level, median R² = 0.091 (four times "
                    "education's). In the HDI, health's proxy is life expectancy, and it is the weakest "
                    "of five components — only 20% of countries significant. In the SDG database, health "
                    "(Goal 3) reaches 11.5% of country-indicator pairs, fourth of 17 goals.",
                    "Life expectancy is close to saturated in developed countries: the top 100 countries "
                    "range from 81 to 85 years. The variance that remains is so small that between-country "
                    "differences add little predictive power. This is not health's problem; it is the "
                    "specific HDI indicator's problem. The gap between frameworks shows the importance "
                    "of variable choice, not of health itself.",
                ],
                "figure": "health_levels_comparison.png",
                "caption": "Health's R² (% of countries significant at levels) across three frameworks. "
                           "Self-rated health in ESS dominates; external HDI proxy (life expectancy) is weak.",
            },

            {
                "label": "Result 3 · Discussion · The coverage gap",
                "heading": "Social trust leads the ESS, is nearly invisible to development frameworks",
                "body": [
                    "Social trust — 'most people can be trusted' — is significant in 94% of ESS countries, "
                    "third strongest domain after health and income, with median R² = 0.041. Neither the HDI "
                    "nor the SDG framework measures it at all.",
                    "The SDG database does carry 13 trust- and satisfaction-adjacent series under Goal 16: "
                    "satisfaction with public services, perception of bribery, perceived decision-making "
                    "inclusiveness. But these measure institutional confidence, not interpersonal trust — a "
                    "different construct, and one that correlates more weakly with life satisfaction even "
                    "when tested across countries. Moreover, their median coverage is one observation per "
                    "country-series against six for the database as a whole; 147 of 163 country-series cannot "
                    "support a time-series design.",
                    "Education's and health's problems are about which variable to count within a domain. "
                    "Trust's problem is different: it is not in the frameworks at all. That is a coverage gap, "
                    "not a measurement problem.",
                ],
                "figure": "trust_coverage_comparison.png",
                "caption": "Social trust: 94% of ESS countries significant (individual level), 1.5% of SDG16 "
                           "country-indicator pairs (institutional confidence, not interpersonal trust), "
                           "not measured in the HDI.",
            },

            {
                "label": "Synthesis",
                "heading": "Three domains, three ways frameworks lose sight of what matters",
                "body": [
                    "Education's rank depends on which construct you count: attainment works, but parity "
                    "ratios and learning outcomes do not, so pooling dilutes the signal. Health's rank depends "
                    "on whether your chosen variable still varies: life expectancy does not, but self-rated "
                    "health does, so the HDI's choice costs it. Social trust's rank is zero because it is not "
                    "collected at scale in development frameworks at all — a coverage gap that cannot be fixed "
                    "by choosing the right variable, because no variable was ever measured.",
                    "These are not criticisms of the frameworks; they were built to track development, and "
                    "they do. But which components look most consequential for lived experience is not the "
                    "question they were built to answer.",
                ],
                "figure": "domain_horse_race.png",
                "caption": "Domains competing within one instrument (ESS), at two levels of aggregation. "
                           "Individual level (left) and country means (right).",
            },
        ],
    },

    {
        "numeral": "III",
        "title": "What this means for development frameworks",
        "key_numbers": [
            ("3 vs. 1", "domains the HDI can test for wellbeing, vs. social trust"),
            ("42 vs. 661", "countries with SDG data, vs. series in the database"),
            ("0.041", "median R² for trust — below income, health, education individually, above none"),
        ],
        "thesis": (
            "The disconnect is real and worth naming. Development frameworks have done their job "
            "of tracking progress on development. But the components that predict individual lived "
            "experience are ones these frameworks are not currently built to see — because of "
            "construction choices, variable saturation, or coverage that was never collected."
        ),
        "close": (
            "Whether development measurement should be redesigned with wellbeing in mind is beyond "
            "this scope. But if it is, this evidence suggests the measurement should be different: "
            "more attentive to which variables still move, which constructs predict outcomes, and which "
            "domains are collected at all."
        ),
        "beats": [
            {
                "label": "The disconnect",
                "heading": "These frameworks work for development. They do not work for wellbeing.",
                "body": [
                    "The HDI and SDG frameworks do not answer the question 'what makes people's "
                    "lives better?' any more than a global income statistics database answers 'what "
                    "makes a person happy?' They were designed to track development, measured at "
                    "the aggregate level, with indicators chosen before the question of individual "
                    "wellbeing was systematically tested. That is not a design failure; it is the "
                    "intended scope.",
                    "But it means the gap is structural. Education's access indicators work; pooling "
                    "them with constructs that do not does not fix wellbeing prediction — it just "
                    "builds a worse measure. Choosing a variable for health that is closer to saturated "
                    "than the outcome it predicts is a measurement choice, not an incurable problem. "
                    "And when a domain is never collected, no amount of better construction on the "
                    "others will reach it.",
                ],
                "figure": None,
                "caption": None,
            },

            {
                "label": "Implication 1 · Measurement choices constrain what frameworks can see",
                "heading": "Education and health: the case for measurement specificity",
                "body": [
                    "Education is significant everywhere it is measured as attainment, but nearly "
                    "invisible in SDG4 because most indicators measure something else. Health is "
                    "nearly invisible in the HDI because life expectancy has saturated. Neither domain "
                    "has changed; the frameworks' construction choices have.",
                    "For education, this suggests development measurement should weigh access and "
                    "completion more heavily than parity ratios in wellbeing contexts — not universally, "
                    "but with explicit construction choices that account for what is known to matter. "
                    "For health, it suggests that wellbeing-motivated measurement may need different "
                    "variables at different development levels: life expectancy in lower-income settings, "
                    "self-reported health or specific conditions in saturated ones.",
                ],
                "figure": None,
                "caption": None,
            },

            {
                "label": "Implication 2 · Coverage gaps are more fundamental than construct choice",
                "heading": "Social trust: why you cannot fix a measurement by measuring better",
                "body": [
                    "Social trust is the most tentative finding here. The ESS is Europe-only, across "
                    "36 countries, and relies on a single item. That bounds the claim: the pattern "
                    "holds in Europe, with a wellbeing survey, on a self-report basis. It does not claim "
                    "universality.",
                    "But the reason it is tentative points to the deepest problem: trust is not collected "
                    "at global scale in either framework. The SDG database has 13 series adjacent to trust, "
                    "but they measure institutional confidence, not interpersonal trust, and they are "
                    "intermittent (147 of 163 country-series have fewer than four years of data). "
                    "This is not a construct-choice problem that better measurement can solve. "
                    "It is a coverage gap that requires deciding to collect the data in the first place.",
                    "For wellbeing-conscious development monitoring, this suggests either building "
                    "interpersonal-trust measurement into the core frameworks, or acknowledging that "
                    "other surveys (the ESS, Gallup World Poll, World Values Survey) may be more suitable "
                    "for understanding what shapes lived experience.",
                ],
                "figure": None,
                "caption": None,
            },

            {
                "label": "Conclusion",
                "heading": "A question rather than a prescription",
                "body": [
                    "The evidence shows a consistent pattern: which domain looks most consequential "
                    "for wellbeing depends on which framework measures it and what variable they chose. "
                    "This is not about the domains; it is about the tools.",
                    "Whether development frameworks should be redesigned around wellbeing is outside "
                    "the scope here. But if they were, this finding suggests the question to ask: "
                    "should measurement choices be made with explicit reference to which variables "
                    "still move and still matter for lived experience? Should coverage be built in for "
                    "domains the frameworks discovered only by studying something else?",
                    "The frameworks work well for their stated purpose. The question is whether wellbeing "
                    "should become part of that purpose — and if it does, whether the measurement that comes "
                    "from that intent should be different from the aggregate, development-first measurement "
                    "in place today.",
                ],
                "figure": None,
                "caption": None,
            },
        ],
    },
]

# --------------------------------------------------------------------------
# Appendix (figures carried for reference, not in main narrative)
# --------------------------------------------------------------------------
APPENDIX = [
]

# --------------------------------------------------------------------------
# Decisions and open questions
# --------------------------------------------------------------------------
DECISIONS = [
    ("Figure count",
     "Commentaries allow one or two. Proposed: three-panel composite as Figure 1 "
     "and domain scorecard as Figure 2. Everything else supplementary."),

    ("Scope of trust findings",
     "Trust findings rest on ESS (36 European countries, individual-level). The "
     "design requires ≥4 years per country-series; only 16 of 163 SDG trust-adjacent "
     "series have that coverage, and 1 is significant. Tested cross-sectionally, 9 of 13 "
     "series are usable and 4 are significant, but all fall below HDI components on the "
     "same countries. The claim is Europe-only and rests on one instrument in each "
     "framework; it is the most tentative of the three."),

    ("Institutional confidence vs. interpersonal trust",
     "The SDG's Goal 16 trust series measure satisfaction with public services, "
     "perceived bribery, and perceived inclusiveness in decision-making — institutional "
     "confidence, not interpersonal trust ('most people can be trusted'). These are "
     "conceptually distinct. The commentarymust be explicit that SDG16 is not a direct "
     "analogue for the ESS trust item."),

    ("Three failure modes frame",
     "The narrative positions education's, health's, and trust's findings as evidence "
     "of three different ways frameworks lose sight of domains that matter: wrong construct, "
     "saturated variable, coverage gap. This is a meta-finding about measurement, not about "
     "the domains themselves."),
]
