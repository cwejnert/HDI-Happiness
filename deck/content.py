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
    "kicker": "Three questions about measurement",
    "heading": "What actually matters for individual lived experience, and are development frameworks measuring it?",
    "body": [
        "Development measurement has a wellbeing problem. Frameworks like the SDG and HDI were built to track "
        "progress on development goals, not to understand what predicts how people experience their lives. But "
        "if development is meant to improve wellbeing, we should ask: Do the frameworks capture what actually matters? "
        "What does matter at the individual level? And if they don't align, how should development measurement change?",
        "The SDG paper under review provides the opening: the association between development indicators and "
        "happiness is strong between countries but nearly absent within them year-to-year. Thirty of 42 countries "
        "are significant in levels. Two are in differences. The obvious dismissal: the SDG framework is sprawling "
        "and unevenly covered; a null says as much about the framework as the world.",
        "This commentary answers the three questions by testing them across frameworks. We replicate the collapse "
        "on the HDI, test it against individual-level wellbeing data (the ESS), and ask what domains actually predict "
        "life satisfaction when measured at the right level and resolution. The answer: education, health, and social "
        "trust all matter. But which framework sees them depends entirely on construction choices—which construct you "
        "count, which variable you measure, which domains you collect. Based on that evidence, we suggest how development "
        "measurement could evolve.",
    ],
    "acts": [
        ("I", "The levels-to-differences collapse is universal.",
         "Replicate it on the HDI, against a second wellbeing survey, and one spatial scale down. "
         "It holds every time — except in ESS, where individual-level data is responsive to change."),
        ("II", "At the levels: what actually matters for lived experience?",
         "Three domains predict life satisfaction: education, health, and social trust. But frameworks see them differently "
         "because of construction choices, variable saturation, or missing coverage. This is what measurement shows matters."),
        ("III", "Why measurement type matters: within-country evidence.",
         "Individual-level, self-reported data captures year-to-year change that administrative frameworks miss. "
         "Development frameworks measure at the wrong temporal and individual resolution to see lived experience."),
        ("IV", "How development frameworks could evolve.",
         "Based on what matters for individual wellbeing, specific recommendations for education, health, and social trust. "
         "A roadmap for aligning development measurement with what research shows actually predicts lived experience."),
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
                    "countries, 351,000 respondents — reveals something unexpected: the collapse "
                    "does NOT hold here. Both levels and differences show significant associations. "
                    "Life satisfaction and happiness respond to year-to-year changes in how people "
                    "report themselves, not just to between-country differences. This is a important "
                    "caveat to our main finding: self-reported wellbeing measures capture changes that "
                    "administrative development indicators miss — but only at the temporal and geographic "
                    "resolution of the ESS (36 European countries, annual cycles). The persistence of the "
                    "collapse in SDG and HDI suggests their construction choices matter more than the "
                    "measurement method alone.",
                ],
                "figure": "ess_levels_diffs_collapse.png",
                "caption": "ESS shows persistent associations in differences, unlike SDG and HDI. "
                           "Caveat: 36 European countries, self-reported measures, annual survey cycles.",
            },
            {
                "label": "The composite + sub-components",
                "heading": "Beneath the composites, the components tell different stories",
                "body": [
                    "Expected years of schooling leads the HDI: highest median R² at levels "
                    "(0.326) and in differences (0.069), above the composite itself. Income is "
                    "level with it in levels, weaker in differences. Life expectancy — the HDI's "
                    "proxy for health — is weakest in levels.",
                    "The HDI still shows the collapse, unlike the ESS, so the question shifts: "
                    "which components of development are actually strong at the levels, and why does "
                    "the type of measurement matter? This is the entry point to Act II: which components "
                    "are actually strong, weak, or invisible when you look at each framework's "
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
        "title": "At the levels: three domains, three failure modes",
        "key_numbers": [
            ("92% vs 34% vs 3.3%", "countries significant: education in ESS, HDI, and SDG4 pooled"),
            ("100% vs 20% vs 11.5%", "countries significant: health in ESS, HDI, and SDG3"),
            ("94% vs 1.5% vs —", "countries significant: social trust in ESS, SDG16, and HDI (not measured)"),
        ],
        "thesis": (
            "Three domains predict life satisfaction. But which frameworks can see them "
            "depends entirely on construction choices: which construct you count, which variable "
            "you measure, which domains you collect. Each framework's limitations reveal different "
            "failure modes, not different realities."
        ),
        "close": (
            "The problem is not the domains; the problem is the measurement. Frameworks designed "
            "for development, with aggregate indicators measured at long intervals, structurally "
            "cannot see what matters for individual lived experience."
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
                    "specific HDI indicator's problem. Within the SDG database's vast landscape of 661 series "
                    "across 42 countries, health indicators dominate the top-ranked individual series, with "
                    "16 of the top 25 most predictive SDG series falling under Goal 3 — survival measures like "
                    "infant mortality, under-five mortality, stunting, and sanitation. The low 11.5% rate for "
                    "health is not evidence that health doesn't matter; it is evidence that most of the SDG "
                    "database does not predict wellbeing. Within that context, health ranks high.",
                ],
                "figure": "health_levels_comparison.png",
                "caption": "Health's R² (% of countries significant at levels) across three frameworks. "
                           "Self-rated health in ESS dominates; external HDI proxy (life expectancy) is weak.",
            },

            {
                "label": "Result 3 · Social trust",
                "heading": "Social trust leads the ESS, is nearly invisible to development frameworks",
                "body": [
                    "Social trust — 'most people can be trusted' — is significant in 94% of ESS countries, "
                    "third strongest domain after health and income, with median R² = 0.041. Neither the HDI "
                    "nor the SDG framework measures it at all.",
                    "The SDG database does carry 13 trust- and satisfaction-adjacent series under Goal 16, but "
                    "the detail reveals why they fail to capture interpersonal trust. First, coverage: only nine "
                    "of thirteen can be tested across countries, and four are significant — weaker than the development "
                    "indicators the frameworks already carry. Second, construct: bribery (individuals and firms) and "
                    "decision-making inclusiveness predict wellbeing; satisfaction with healthcare, government services, "
                    "and secondary education do not. These measure institutional confidence, not interpersonal trust. "
                    "Third, when you control for income — net of log GNI per capita — nearly all SDG trust series disappear. "
                    "This is a known artifact of subjective institutional scales; interpersonal trust, by contrast, shows robust "
                    "signal independent of income controls.",
                    "Education's and health's problems are about which variable to count within a domain. Trust's problem is "
                    "different: it is not in the frameworks at all. That is a coverage gap that cannot be fixed by choosing the "
                    "right variable, because no variable was ever measured.",
                ],
                "figure": "K1_sdg_trust_cross_section.png",
                "caption": "SDG16 trust series can barely be tested (9 of 13 measurable, 4 significant) and collapse when "
                           "controlled for income. Interpersonal trust only appears in ESS.",
            },

            {
                "label": "Synthesis",
                "heading": "Three domains, three frameworks, three different blind spots",
                "body": [
                    "Education's rank depends on which construct you count: attainment works, but parity "
                    "ratios and learning outcomes do not, so pooling dilutes the signal. Health's rank depends "
                    "on whether your chosen variable still varies: life expectancy does not, but self-rated "
                    "health does, so the HDI's choice costs it. Social trust's rank is zero because it is not "
                    "collected at scale in development frameworks at all — a coverage gap that cannot be fixed "
                    "by choosing the right variable, because no variable was ever measured.",
                    "These are not criticisms of the frameworks; they were built to track development, and they do. "
                    "Education is testable in all three frameworks but its rank depends entirely on which construct was chosen. "
                    "Health is testable everywhere and leads wherever it is measured something that still varies — a robust "
                    "signal despite the HDI's proxy choice. Social trust is testable in one instrument only: the ESS, where it "
                    "emerges as third strongest. It does not appear in the HDI at all, and the SDG framework measures institutional "
                    "confidence instead, a different construct entirely.",
                ],
                "figure": "domain_scorecard.png",
                "caption": "Which frameworks can test each domain (green = tracks wellbeing, "
                           "yellow = measurable but weak signal, gray = framework cannot test it).",
            },
        ],
    },

    {
        "numeral": "III",
        "title": "Within-country evidence: Why measurement type matters",
        "key_numbers": [
            ("69% → 64%", "ESS levels → differences (NOT collapsed)"),
            ("71% → 5%", "SDG levels → differences (collapsed)"),
            ("42% → 2%", "HDI levels → differences (collapsed)"),
        ],
        "thesis": (
            "Individual-level, self-reported data shows a fundamentally different pattern. "
            "Unlike administrative development frameworks, ESS captures year-to-year variation "
            "within countries. This is not a measurement failure; it is a structural consequence "
            "of how development is measured — at the country level, with long intervals. "
            "Social trust emerges not because frameworks miss it, but because development "
            "frameworks measure at the wrong temporal and individual resolution where trust varies."
        ),
        "close": (
            "The three domains predict wellbeing differently depending on where and how you measure. "
            "Development frameworks' blindness is not incurable; it is structural. Frameworks designed "
            "for tracking aggregate national progress cannot see individual experience responsive to change."
        ),
        "beats": [
            {
                "label": "Within-country evidence",
                "heading": "Individual-level, self-reported data captures year-to-year change that administrative frameworks miss",
                "body": [
                    "Here is the critical observation that reshapes the question: unlike SDG (71% levels "
                    "→ 5% differences) and HDI (42% → 2%), the ESS shows 69% levels → 64% differences. "
                    "The association persists within countries over time. This is not because development "
                    "frameworks are poorly designed; it is because they measure aggregate, administrative "
                    "data at long intervals (annual at best for HDI and SDG). Individual survey responses "
                    "capture year-to-year variation in how people experience their lives.",
                    "This is why social trust emerges here. At the country level, the SDG database carries 13 trust-adjacent series, "
                    "but only nine can be tested, four are significant, and nearly all disappear when controlling for income. They measure "
                    "institutional confidence, not interpersonal trust. In the HDI, trust is not measured at all. But at the individual level, "
                    "within countries, the ESS shows interpersonal trust is significant in 94% of countries and drives year-to-year change "
                    "in wellbeing. The three domains emerge not because the frameworks reveal them, but because ESS measures them where people "
                    "actually experience variation: in themselves, over time.",
                    "This is not about measurement error. It is structural. Frameworks designed for tracking aggregate national progress "
                    "cannot see individual experience responsive to change. At regional scale, the collapse persists: across 167 subnational "
                    "regions within ESS countries with ≥5 survey years, life satisfaction and regional development show the same pattern as "
                    "national data — strong levels associations, weak differences associations. The problem is not aggregation; it is temporal "
                    "resolution and individual measurement.",
                    "The caveats are substantial: 36 European countries, self-reported measures, annual cycles. But the implication is clear. "
                    "Development frameworks' blindness to social trust is not because trust does not matter for wellbeing; it is because development "
                    "was never designed to measure individual experience at the temporal resolution where people and places change.",
                ],
                "figure": "collapse_shdi_ess_regional.png",
                "caption": "Regional collapse: 167 subnational regions, levels vs. differences. ESS persists; collapse "
                           "confirms it is not an artifact of national aggregation but of measurement type.",
            },
        ],
    },

    {
        "numeral": "IV",
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
                "label": "The structural disconnect",
                "heading": "These frameworks were built to measure development, not to capture what predicts wellbeing",
                "body": [
                    "The HDI and SDG frameworks do not answer the question 'what makes people's lives better?' "
                    "They were designed to track development at the aggregate level, with indicators chosen before "
                    "the question of individual wellbeing was systematically tested. That is not a design failure; "
                    "it is the intended scope. But it creates a structural gap: frameworks measuring aggregate, "
                    "infrequent administrative data cannot see individual experience that responds to change.",
                    "The gap is not incurable. It is built on three concrete, fixable problems: wrong constructs "
                    "for some domains, saturated variables for others, and missing coverage for those not measured "
                    "at all. This commentary suggests how to fix each.",
                ],
                "figure": None,
                "caption": None,
            },

            {
                "label": "Implication 1 · Fix wrong constructs",
                "heading": "Education and health: measurement specificity based on what predicts wellbeing",
                "body": [
                    "Education is significant everywhere it is measured as attainment (92% in ESS, 34% in HDI, "
                    "12.7% in SDG4 access alone). But SDG4 averages it with parity ratios and learning outcomes, "
                    "which do not predict wellbeing, collapsing the pooled rate to 3.3%. The fix: development "
                    "frameworks should make construction choices with explicit reference to what research shows "
                    "matters for lived experience. For education in wellbeing contexts, this means weighting access "
                    "and completion more heavily than equity ratios.",
                    "Health is nearly invisible in the HDI (20% significant) because life expectancy is saturated "
                    "in developed countries — the top 100 range from 81–85 years. Yet self-rated health is significant "
                    "in 100% of ESS countries. The fix: use different variables at different income levels. Life expectancy "
                    "for lower-income settings where it still varies; self-reported health, or condition-specific mortality "
                    "(maternal, neonatal, under-five), in saturated ones.",
                ],
                "figure": None,
                "caption": None,
            },

            {
                "label": "Implication 2 · Add missing coverage",
                "heading": "Social trust: why coverage gaps cannot be fixed by better measurement of wrong things",
                "body": [
                    "Social trust is significant in 94% of ESS countries and is the third-strongest predictor after "
                    "health and income. Neither the HDI nor the SDG framework measures it. The SDG database has 13 "
                    "series under Goal 16, but they measure institutional confidence—satisfaction with government, "
                    "healthcare, education—not interpersonal trust. Moreover, 147 of 163 country-series have fewer than "
                    "four years of data, making time-series designs impossible.",
                    "The fix: development frameworks cannot discover what matters by measuring something else and hoping "
                    "it correlates. If wellbeing is part of development measurement's purpose, interpersonal trust must be "
                    "collected at scale. This could mean building social trust into core frameworks, or integrating data from "
                    "surveys designed to measure individual experience (ESS, Gallup World Poll, World Values Survey). The scope "
                    "of trust findings—36 European countries, individual-level—is tentative. But tentative is better than absent.",
                ],
                "figure": None,
                "caption": None,
            },

            {
                "label": "Conclusion",
                "heading": "From evidence to redesign",
                "body": [
                    "The evidence is clear: which domain predicts life satisfaction depends on which framework measures it "
                    "and what variable they chose. This is not about the domains; it is about the tools. Development frameworks "
                    "work well for their stated purpose — tracking aggregate progress toward development goals. But if that purpose "
                    "is understood to include supporting lived experience, the measurement needs to change.",
                    "The three implications suggest where to start: make construction choices based on what research shows matters "
                    "(education's access, health's variation, not saturation); choose variables that still move at the development "
                    "levels being measured; and collect data for domains that matter but are currently missing. This is not a complete "
                    "redesign. It is targeted adjustment rooted in evidence about what predicts individual wellbeing.",
                    "The underlying question remains: Should development measurement be redesigned with lived experience in mind? "
                    "If yes, should it measure at the individual level, with shorter intervals, using variables chosen for their "
                    "responsiveness to change and their evidence of predicting wellbeing? The frameworks in place today are built for "
                    "a different answer. These findings suggest what a different answer might measure.",
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
