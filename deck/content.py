"""
The commentary, structured as a walk through the paper — step by step through
the evidence, in the order the analysis was actually run.

Single source of truth for both outputs: build_artifact.py renders it as a
self-contained HTML page for the co-author team, build_pptx.py renders the
same content as a slide deck for presenting. Edit the argument here, rebuild
both.

Every number in this file traces back to make_figures.py /
build_comparative_figures.py / HappinessSDG.R; figure filenames refer to
deck/figures/.

One unit throughout: the percentage of units (countries, or regions) in which
the association is Benjamini-Hochberg FDR-significant at q < .05. Wherever a
median R-squared appears it is labelled as such.
"""
from __future__ import annotations

TITLE = "Measured Where It Varies"
SUBTITLE = (
    "Development indicators predict wellbeing between countries and not within them. "
    "Working through why: which domains actually track lived experience, and which of "
    "them the frameworks built to monitor development are able to see."
)
DATELINE = "Working synthesis for the co-author team · September 2026"
SCOPE = (
    "SDG: 42 countries, 661 series · HDI × World Happiness Report: 150 "
    "countries, 2011–2023 · Subnational HDI: 167 regions · European Social "
    "Survey: 36 countries, 351,023 respondents, rounds 5–11 (2010–2023) · "
    "All tests Benjamini–Hochberg FDR at q &lt; .05"
)

# --------------------------------------------------------------------------
# Opening
# --------------------------------------------------------------------------
HOOK = {
    "kicker": "Where this starts",
    "heading": "The SDG paper found something odd. This is the walk through what it turned out to mean.",
    "body": [
        "In the SDG paper, development indicators predict happiness strongly between countries and "
        "almost not at all within them year to year. Thirty of 42 countries are significant in levels; "
        "two are in differences. The obvious dismissal is that this says more about the SDG framework "
        "than about the world — 661 series, uneven coverage, seventeen goals of wildly different maturity.",
        "So we tested that dismissal. Swap the framework for the HDI — built the opposite way on every "
        "dimension the dismissal leans on — and the collapse is just as sharp. Swap the Cantril ladder for "
        "the European Social Survey and go one spatial scale down, and the levels association holds on an "
        "independent instrument. The asymmetry is a property of the design, not of the SDGs, and the levels "
        "are where the signal actually lives.",
        "That licenses the next question. If levels are where development and wellbeing meet, which parts "
        "of development are doing the work? In the frameworks, health and education both register — but only "
        "once you stop pooling education's 35 series together. Then we ask the same question of the ESS, "
        "where the domains are measured on people rather than on national aggregates, and a third domain "
        "appears that neither framework collects: social trust.",
        "The last act is what that implies. Not that the SDGs and HDI are bad instruments — they do the job "
        "they were built for. The narrower claim is that they may not be capturing what shapes lived "
        "experience at the individual level, and the evidence points to fairly specific things one could "
        "change about that.",
    ],
    "acts": [
        ("I", "The collapse is real, and it is not about the SDGs.",
         "The HDI shows it as sharply as the SDGs do, and an independent wellbeing instrument "
         "corroborates the levels half. Differences carry nothing — so analyse the levels."),
        ("II", "At the levels, health and education carry the frameworks.",
         "The HDI's five components and the SDGs' seventeen goals, ranked. Health is 4th of 17. "
         "Education looks 12th — until you unpool it."),
        ("II-a", "Measure the same domains on people, and a third one appears.",
         "In the ESS, health, education and social trust are all significant within countries. Trust "
         "is second strongest — and neither framework collects it."),
        ("III", "Three domains, three different reasons frameworks lose them.",
         "Wrong construct pooled together, a variable that has stopped varying, and a domain that "
         "was never collected at all."),
        ("IV", "What this could mean for development frameworks.",
         "Not a verdict on the SDGs or HDI. A set of specific, evidence-backed things to change if "
         "lived experience is meant to be part of what they track."),
    ],
}

# --------------------------------------------------------------------------
# Acts
# --------------------------------------------------------------------------
ACTS = [
    {
        "numeral": "I",
        "title": "Does the collapse survive when you change the design?",
        "key_numbers": [
            ("71% → 5%", "SDG × WHR, 42 countries, ~13 years — the original finding"),
            ("42% → 2%", "HDI × WHR, 150 countries, ~13 years — swap the framework"),
            ("47%", "SHDI × ESS at levels, across regions — swap the instrument and scale"),
        ],
        "thesis": (
            "The SDG null invites an easy dismissal: sprawling framework, uneven coverage, so "
            "the absence of a within-country signal says more about the instrument than about "
            "development. Test that by changing one leg of the design at a time. If the collapse "
            "is an artefact of the SDGs, it should not survive."
        ),
        "close": (
            "Two well-powered pairings, the same asymmetry in both. The ESS corroborates the levels "
            "half with an independent wellbeing instrument, and is too short a panel to rule on "
            "differences either way. Differences cannot carry an argument — so everything that "
            "follows is a question about the levels."
        ),
        "beats": [
            {
                "label": "Where we start · the SDG paper",
                "heading": "Development indicators predict happiness between countries, not within them",
                "body": [
                    "The original design is a per-country time-series test: within each country, does the "
                    "SDG indicator move with the Cantril ladder? Run at levels, 30 of 42 countries come back "
                    "FDR-significant on at least one of 661 series — 71%. Run the identical test on first "
                    "differences, and 5% survive.",
                    "That gap is the whole starting point. A between-country association this strong and a "
                    "within-country association this weak are hard to hold at once: either development stops "
                    "mattering once you look inside a country, or the design cannot see it there. Before "
                    "interpreting it, it is worth checking that it is not simply the SDG framework misbehaving.",
                ],
                "figure": "sdg_by_goal.png",
                "caption": "The SDG framework at levels, by goal. Even here the pooled rates are low and "
                           "uneven — health reaches 11.5%, education 3.3% — which is what makes the "
                           "framework-artefact dismissal plausible enough to need testing.",
            },
            {
                "label": "Swap 1 · the framework",
                "heading": "The HDI is built the opposite way and shows the same collapse",
                "body": [
                    "The HDI is the SDG framework's opposite on every dimension the dismissal leans on: "
                    "three dimensions rather than seventeen goals, one custodian, a stable definition, "
                    "near-universal coverage. Substituting it and holding everything else fixed gives 42% "
                    "of 150 countries significant at levels and 2% in differences.",
                    "The three panels are the fair-comparison check. The SDG framework detects in more "
                    "countries (71% vs 51%) simply because it has more shots on goal; give it the HDI's "
                    "five-indicator budget and its advantage disappears; normalise per indicator and the "
                    "HDI dominates outright, with 54% of SDG series significant in no country at all. "
                    "Neither framework is the problem — the ratio between levels and differences is the "
                    "same order of magnitude in both.",
                ],
                "figure": "framework_three_comparisons.png",
                "caption": "HDI versus the SDG framework on detection, on a matched five-indicator budget, "
                           "and per indicator. The SDG lead is breadth, not sharper instruments.",
            },
            {
                "label": "Swap 2 · the wellbeing measure",
                "heading": "Swapping the Cantril ladder for the ESS: what it can and cannot settle",
                "body": [
                    "The World Happiness Report is a single Cantril-ladder question aggregated to countries. "
                    "The European Social Survey asks its own life-satisfaction item of individuals, on a "
                    "different sampling frame, run by a different institution. Holding the HDI and the country "
                    "unit fixed and changing only the wellbeing data isolates that one leg.",
                    "The result is 8% at levels and 16% in differences across 25 countries — and it should be "
                    "read as a null test rather than a finding in either direction. The ESS runs seven survey "
                    "rounds where the WHR panels run thirteen years, and differences coming out above levels is "
                    "not a pattern a real association produces. Panel b is the check: at seven observations, a "
                    "genuine correlation of 0.5 is recovered in about 3% of units. This design cannot see much "
                    "at that length, so its silence is not evidence.",
                    "Where the ESS does have power is in cross-section. Pairing subnational HDI with ESS life "
                    "satisfaction across regions inside each country — many regions per country rather than "
                    "seven rounds — gives 47% of 15 countries FDR-significant at levels, sitting right on top "
                    "of the 42% the HDI reaches nationally against the Cantril ladder. So the levels half "
                    "corroborates on an independent instrument at a finer scale. The differences half rests on "
                    "the SDG and HDI panels, which is where it always rested.",
                ],
                "figure": "ess_levels_diffs_collapse.png",
                "caption": "Panel a: the same FDR test, levels and differences on the same units, in all three "
                           "pairings. Panel b: how much of a genuine association each series length recovers — "
                           "the reason the hatched bars carry no verdict.",
            },
        ],
    },

    {
        "numeral": "II",
        "title": "At the levels, what is actually doing the work?",
        "key_numbers": [
            ("19% vs 41%", "HDI life expectancy vs mean years of schooling, at levels"),
            ("4th of 17", "where health ranks among SDG goals (11.5%)"),
            ("12.7% vs 3.3%", "SDG4 access indicators alone vs all 35 pooled"),
        ],
        "thesis": (
            "If the levels are where development and wellbeing meet, the useful question is which "
            "components are carrying that association. Ask it of both frameworks' internals: the "
            "HDI's five components, and the SDGs' seventeen goals. Two domains come out — but one "
            "of them only after you stop pooling it."
        ),
        "close": (
            "Health and education are what the frameworks can see at the levels. Health registers "
            "wherever it is measured somewhere that still varies; education registers only when the "
            "construct being counted is access. That is two domains — and it is everything these "
            "frameworks are able to test."
        ),
        "beats": [
            {
                "label": "Inside the HDI",
                "heading": "Schooling leads the HDI's components; life expectancy is the weakest of the five",
                "body": [
                    "Decompose the composite and the five components separate cleanly at levels: mean years "
                    "of schooling 41%, income 40%, expected years of schooling 33%, the composite itself 42% "
                    "— and life expectancy last at 19%. In differences all five sit between 1% and 5%, so "
                    "the collapse is a property of the composite and of every part of it.",
                    "Life expectancy being the weakest is the first hint that this is about measurement rather "
                    "than about health. The top 100 countries span 81 to 85 years. A variable with that little "
                    "range left cannot carry much association, whatever the underlying domain does.",
                ],
                "figure": "hdi_full_structure.png",
                "caption": "HDI composite and its five components, levels and first differences, "
                           "Benjamini–Hochberg corrected within each country.",
            },
            {
                "label": "Inside the SDGs",
                "heading": "Health ranks 4th of 17 goals; education ranks 12th",
                "body": [
                    "The same question of the SDG side. Pooled within each goal, health (Goal 3) reaches 11.5% "
                    "of country-indicator pairs — fourth of seventeen, and first among the goals with "
                    "substantive coverage. Health also dominates the individual-series ranking: 16 of the 25 "
                    "most predictive series in the whole database fall under Goal 3, and they are survival "
                    "measures — infant and under-five mortality, stunting, neonatal mortality, sanitation, "
                    "drinking water.",
                    "Education comes twelfth, at 3.3%. Taken at face value that says education barely matters "
                    "for wellbeing — which contradicts the HDI, where schooling is the strongest component "
                    "there is. Both cannot be right, and the next slide is why.",
                    "One caveat worth stating here rather than later: Goal 16 is where anything trust-shaped "
                    "would live, and it comes fifteenth at 1.5%. But its thirteen trust-adjacent series measure "
                    "satisfaction with public services, perceived bribery, and perceived inclusiveness in "
                    "decision-making. That is confidence in institutions, not trust in other people. It is a "
                    "different construct, and the low rank should not be read as evidence about interpersonal trust.",
                ],
                "figure": "sdg_indicator_top20.png",
                "caption": "The 25 most predictive individual SDG series. Sixteen are Goal 3 health "
                           "indicators, nearly all of them survival measures.",
            },
            {
                "label": "Access check",
                "heading": "Education's 3.3% is a pooling artefact: access alone reaches 12.7%",
                "body": [
                    "SDG4 is 35 series measuring six different things. Split them and they do not agree: "
                    "access and participation 12.7%, financing 11.5%, attainment and completion 3.8%, "
                    "equity and parity ratios 2.5%, infrastructure 2.0%, learning outcomes 0.9%.",
                    "Parity ratios are 18 of the 35 series. Pooling weights every series equally, so the "
                    "half of the goal that carries no wellbeing signal drags the whole goal below the part "
                    "that does. Unpooled, education would rank third among the seventeen goals rather than "
                    "twelfth — and it would agree with the HDI instead of contradicting it.",
                ],
                "figure": "sdg4_unpooled.png",
                "caption": "SDG4 split by construct. Access and participation (12.7%) against equity and "
                           "parity ratios (2.5%), infrastructure (2.0%) and learning outcomes (0.9%).",
            },
        ],
    },

    {
        "numeral": "II-a",
        "title": "Now measure the same domains on people",
        "key_numbers": [
            ("100% / 97% / 89%", "ESS countries significant: health, trust, education"),
            ("0.092 / 0.039 / 0.006", "median individual R² for the same three"),
            ("351,023", "respondents, 36 countries, ~10,700 per country"),
        ],
        "thesis": (
            "Everything so far is national aggregates against national aggregates. The ESS carries the "
            "same three domains asked directly of individuals — self-rated health, years of schooling, "
            "and whether most people can be trusted. Estimated across respondents and demeaned within "
            "country-round, so the association is within-country and within-year by construction."
        ),
        "close": (
            "Health, trust and education are all significant on people, in almost every country. The "
            "ordering is the surprise: interpersonal trust is second, ahead of education, and it is the "
            "one domain of the three that neither development framework collects."
        ),
        "beats": [
            {
                "label": "Three domains, one unit",
                "heading": "Health, social trust and education all predict life satisfaction — trust is second",
                "body": [
                    "Same FDR test, same unit, now on 351,023 respondents. Self-rated health is significant "
                    "in 36 of 36 countries, median individual R² 0.092. Interpersonal trust in 35 of 36, "
                    "median R² 0.039. Years of schooling in 32 of 36, median R² 0.006 — significant almost "
                    "everywhere but explaining far less per person than either of the others.",
                    "Set against the frameworks, health behaves consistently: strongest on people, and the "
                    "highest-ranked substantive goal in the SDGs. Education behaves consistently too, once "
                    "unpooled. Trust is the one that does not appear anywhere else, because there is nowhere "
                    "else for it to appear — the HDI has no counterpart at all, and SDG16's 1.5% measures "
                    "confidence in institutions rather than trust in people.",
                    "The caveat is real and bounds the claim: the ESS is 36 European countries, self-reported, "
                    "one trust item. This is not a global result. It is enough to say that a domain the "
                    "frameworks never collect outranks one they both do.",
                ],
                "figure": "domains_at_levels_comparison.png",
                "caption": "The three domains across all three frameworks, all on % of countries "
                           "FDR-significant. Trust has no HDI bar because the HDI does not measure it.",
            },
            {
                "label": "Education, close up",
                "heading": "Significant on people and in the HDI; invisible in the SDGs only because of pooling",
                "body": [
                    "Education across all four ways of measuring it: 89% of ESS countries on individual years "
                    "of schooling, 33% of HDI countries on expected years of schooling, 12.7% of SDG4 access "
                    "series, 3.3% pooled across all 35.",
                    "Three of those four numbers tell a consistent story and the fourth is a construction "
                    "choice. Nothing about education changed between the third bar and the fourth — only which "
                    "series were averaged together. This is the cleanest case in the paper of a framework "
                    "hiding a domain it does in fact measure.",
                ],
                "figure": "education_levels_comparison.png",
                "caption": "Education across four measurements. The gap between the last two bars is "
                           "entirely pooling, not data.",
            },
            {
                "label": "Health, close up",
                "heading": "The strongest domain on people, and the weakest component of the HDI",
                "body": [
                    "Self-rated health is the single strongest predictor of life satisfaction in the ESS: "
                    "every country significant, median R² 0.092, roughly fifteen times education's. In the "
                    "SDGs, health leads the substantive goals at 11.5%. In the HDI it is last of five, at 19%.",
                    "The domain is not weak; the HDI's chosen proxy for it is. Life expectancy has largely "
                    "saturated across the countries the index covers, and a variable with almost no variance "
                    "left cannot predict much. Self-rated health, asked of the same populations, is the "
                    "strongest thing in the ESS. Same domain, different variable, opposite conclusion.",
                ],
                "figure": "health_levels_comparison.png",
                "caption": "Health measured three ways. The HDI result is about life expectancy's "
                           "saturation, not about health.",
            },
            {
                "label": "Social trust, close up",
                "heading": "Second strongest on people, and absent from both frameworks",
                "body": [
                    "Interpersonal trust — 'generally speaking, would you say that most people can be trusted?' "
                    "— is significant in 35 of 36 ESS countries, with a median R² of 0.039: below self-rated "
                    "health, well above years of schooling.",
                    "The HDI does not measure trust in any form. The SDG framework's nearest thing is Goal 16's "
                    "thirteen series, and they measure something else: satisfaction with public services, "
                    "perceived bribery, perceived inclusiveness in decision-making. Institutional confidence "
                    "and interpersonal trust are distinct constructs, and the substitution should not pass "
                    "silently. Coverage compounds it — median one observation per country-series against six "
                    "for the database overall, and 147 of 163 country-series cannot support a time-series "
                    "design at all.",
                    "Education's and health's problems are about which variable to count inside a domain the "
                    "framework already has. Trust's is categorically different: there is no variable to choose "
                    "between, because the domain was never collected.",
                ],
                "figure": "trust_coverage_comparison.png",
                "caption": "Interpersonal trust in the ESS against the closest SDG counterpart and an "
                           "absent HDI one. The asterisked bar is a different construct.",
            },
            {
                "label": "Why the SDG trust series cannot stand in",
                "heading": "Institutional confidence does not survive an income control; interpersonal trust does",
                "body": [
                    "Worth testing directly rather than asserting. Of the thirteen Goal 16 trust-adjacent "
                    "series, nine can be tested cross-sectionally and four are significant. Then control for "
                    "log GNI per capita: perceived bribery survives, but satisfaction with government services, "
                    "healthcare and secondary education all vanish.",
                    "That pattern is a known artefact of subjective institutional scales across income levels — "
                    "the same question administered in richer and poorer countries produces response shifts "
                    "unrelated to the construct. Interpersonal trust in the ESS does not behave this way.",
                    "So this is not an execution failure in the SDG framework. It reflects what development "
                    "frameworks are for: they measure institutions and systems. Trust between people is not "
                    "an institution, and it does not show up when you measure one.",
                ],
                "figure": "K1_sdg_trust_cross_section.png",
                "caption": "SDG16 trust series cross-sectionally. Panel (b): net of income, bribery persists "
                           "and the satisfaction measures do not.",
            },
        ],
    },

    {
        "numeral": "III",
        "title": "Three domains, three ways a framework loses one",
        "key_numbers": [
            ("Pooled", "education: the right construct averaged away"),
            ("Saturated", "health: the chosen variable stopped varying"),
            ("Never collected", "trust: no variable to choose between"),
        ],
        "thesis": (
            "Put the three results together and they are not three findings about three domains. "
            "They are three distinct failure modes — and they need different fixes, which is the "
            "only reason the distinction matters."
        ),
        "close": (
            "None of this is a criticism of frameworks built to track development. It is the "
            "observation that which domain looks consequential for lived experience depends on "
            "construction choices made for other reasons — and that one domain is missing outright."
        ),
        "beats": [
            {
                "label": "The synthesis",
                "heading": "A pooling problem, a saturation problem, and a coverage gap",
                "body": [
                    "Education is a pooling problem. The framework measures the right thing — access and "
                    "participation, 12.7% — and then averages it together with 18 parity-ratio series that "
                    "carry no wellbeing signal, landing at 3.3%. The signal is present in the data and "
                    "absent from the published number.",
                    "Health is a saturation problem. The domain is the strongest of the three on people, but "
                    "the HDI's proxy for it has run out of range across the countries it covers, so it comes "
                    "last of five components. A different variable in the same domain reverses the result.",
                    "Trust is a coverage gap, and it is the one that no amount of better construction reaches. "
                    "You cannot unpool a series that does not exist or re-specify a variable that was never "
                    "collected. The only fix available is deciding to collect it.",
                ],
                "figure": "domain_scorecard.png",
                "caption": "Which framework can test which domain, and whether the test returns a signal. "
                           "Grey is not a weak result — it is no result available.",
            },
            {
                "label": "What survives which method",
                "heading": "Health is robust to how you measure it. Trust only appears when you ask people.",
                "body": [
                    "One more cut, because it separates the failure modes cleanly. Health registers in "
                    "administrative sources (SDG3, 11.5%) and in self-reported ones (ESS, median R² 0.092) "
                    "alike — it is robust to measurement method, and the HDI's weak result is specific to "
                    "life expectancy rather than to the domain.",
                    "Education registers in both too, once unpooled, so its problem is construction rather "
                    "than method. Trust registers in one and only one: 97% of ESS countries against 1.5% of "
                    "SDG16 country-indicator pairs measuring a different construct.",
                    "That asymmetry is the argument for why level of measurement matters, and not just "
                    "which indicator you pick. Some things about a life are legible in national aggregates. "
                    "Whether you think your neighbours can be trusted is not one of them.",
                ],
                "figure": "health_trust_corroboration.png",
                "caption": "Health corroborates across administrative and self-reported sources. "
                           "Trust appears only in individual-level data.",
            },
        ],
    },

    {
        "numeral": "IV",
        "title": "What this could mean for development frameworks",
        "key_numbers": [
            ("Unpool", "report SDG4 access separately from parity ratios"),
            ("Re-specify", "a health variable that still varies where it is used"),
            ("Collect", "interpersonal trust, or link to a survey that has it"),
        ],
        "thesis": (
            "The SDGs and the HDI do the job they were built for, and none of this evidence says "
            "otherwise. The narrower claim is that they may not be capturing what shapes lived "
            "experience at the individual level — and that the evidence points to reasonably "
            "specific things one could do about it."
        ),
        "close": (
            "Whether wellbeing belongs in the purpose of a development framework is a choice, not a "
            "finding. But if it does, the measurement that follows from that intent looks different "
            "from the measurement in place today — and the three changes above are where it would start."
        ),
        "beats": [
            {
                "label": "The disconnect",
                "heading": "Two different questions, and only one of them is being measured",
                "body": [
                    "'How is development progressing?' and 'what shapes how people experience their lives?' "
                    "are not the same question, and the frameworks were built to answer the first. Indicators "
                    "were chosen before the second was systematically testable, at an aggregate level, on "
                    "annual or slower cycles. That is scope, not failure.",
                    "But the consequence is that a framework can be working exactly as designed and still be "
                    "a poor guide to lived experience. Two of the three domains that predict life satisfaction "
                    "in the ESS are present in the frameworks and obscured by construction choices; the third "
                    "is not present at all. None of that shows up in a framework's own diagnostics, because "
                    "nothing in those diagnostics is asking about wellbeing.",
                ],
                "figure": None,
                "caption": None,
            },
            {
                "label": "Change 1 · education",
                "heading": "Report access separately, rather than pooling it into a goal-level average",
                "body": [
                    "The cheapest change on this list, because it needs no new data collection. SDG4's access "
                    "and participation series already reach 12.7%; the published goal-level figure of 3.3% is "
                    "produced by averaging them with parity ratios, infrastructure and learning outcomes, "
                    "which reach 2.5%, 2.0% and 0.9%.",
                    "So the suggestion is a reporting convention rather than a measurement programme: where a "
                    "goal pools constructs that behave differently, publish the constituents alongside the "
                    "pooled rate. Every number needed for this already exists in the database. What it would "
                    "buy is that education stops looking like a domain that does not matter for wellbeing, "
                    "which on this evidence it plainly does.",
                ],
                "figure": None,
                "caption": None,
            },
            {
                "label": "Change 2 · health",
                "heading": "Use a health variable that still varies where the framework is being applied",
                "body": [
                    "Life expectancy is a good development indicator and a poor wellbeing one in exactly the "
                    "places where development has already happened. Between 81 and 85 years across the top "
                    "100 countries, there is very little variance left for it to explain — which is why it "
                    "comes last of the HDI's five components at 19%, while self-rated health leads the ESS at "
                    "100% of countries.",
                    "The evidence suggests health measurement could be made conditional on context rather than "
                    "uniform: life expectancy where mortality still varies, and something with range left — "
                    "self-rated health, or condition-specific measures — where it does not. This is not two "
                    "frameworks. It is one domain, measured with an instrument chosen to still be sensitive "
                    "in the setting it is used in.",
                ],
                "figure": None,
                "caption": None,
            },
            {
                "label": "Change 3 · social trust",
                "heading": "Collect interpersonal trust, or link systematically to surveys that already do",
                "body": [
                    "This is the expensive one, and the only one that cannot be solved by re-analysing what "
                    "exists. On the ESS evidence, interpersonal trust is the second strongest of the three "
                    "domains — ahead of education — and neither framework collects it. SDG16's institutional "
                    "confidence series are not a substitute: different construct, and they do not survive an "
                    "income control.",
                    "Two routes. Add a trust item to core collection, which is a single well-validated "
                    "question and cheap per respondent but slow institutionally. Or build systematic linkage "
                    "to instruments that already carry it — the ESS in Europe, Gallup World Poll and the "
                    "World Values Survey more broadly — so that country assessments can draw on it without "
                    "the frameworks having to own the collection.",
                    "The honest caveat stays attached: this rests on 36 European countries and one survey "
                    "item. It is the most tentative finding in the paper. It is also the one where the cost "
                    "of being right and not measuring is highest, because the gap is invisible from inside "
                    "the frameworks.",
                ],
                "figure": None,
                "caption": None,
            },
            {
                "label": "Where this leaves the argument",
                "heading": "Not a verdict on the frameworks — a question about what they are for",
                "body": [
                    "Two of the three changes above are re-analysis of data that already exists. The third is "
                    "a collection decision. None of them requires accepting that the SDGs or the HDI are "
                    "failing at what they set out to do.",
                    "What the evidence does support is narrower and, we think, harder to dismiss: which domain "
                    "looks consequential for lived experience depends heavily on construction choices that "
                    "were made for other, defensible reasons — and on one domain that was never on the list "
                    "at all. If wellbeing is meant to be part of what these frameworks track, those choices "
                    "are now testable rather than conventional, and this is what testing them shows.",
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
    ("collapse_hdi_shdi_whr.png",
     "The collapse across all three national pairings",
     "Countries FDR-significant at levels versus first differences under the SDG framework, "
     "the HDI, and subnational HDI aggregated nationally."),
    ("collapse_shdi_ess_regional.png",
     "Per-region collapse, subnational HDI against ESS life satisfaction",
     "167 regions with at least five survey rounds. Levels R² on the horizontal axis, "
     "across-year differences on the vertical."),
    ("domain_horse_race.png",
     "The three domains competing inside one instrument",
     "ESS only, at two levels of aggregation: individual respondents on the left, "
     "country means on the right."),
    ("ess_individual_education.png",
     "Individual-level education by country",
     "The distribution behind the 89% figure — per-country associations between years of "
     "schooling and life satisfaction across 351,023 respondents."),
]

# --------------------------------------------------------------------------
# Decisions and open questions
# --------------------------------------------------------------------------
DECISIONS = [
    ("Figure count",
     "Commentaries allow one or two. Proposed: the three-way collapse as Figure 1 and the "
     "three-domain comparison as Figure 2. Everything else supplementary."),

    ("One unit, everywhere",
     "Every headline number is now % of units FDR-significant at q < .05, so ESS, HDI and SDG "
     "bars can sit in one chart. An earlier draft scored ESS as R² > 0.04 on ~7 country-round "
     "means; at that n roughly two-thirds of pure noise clears the bar, which inflated the ESS "
     "figures and made the framework comparison meaningless. ESS is now estimated on individual "
     "respondents, demeaned within country-round."),

    ("What the ESS panel can and cannot test",
     "Seven survey rounds is too short for the per-country time-series design. Simulating a REAL "
     "correlation and asking how often the test finds it: at seven observations rho = 0.5 is "
     "recovered in ~3% of units and rho = 0.7 in ~23%, against ~50% and ~79% at thirteen years. "
     "So HDI x ESS returning 8% levels / 16% differences is a null test, not a finding — and the "
     "inversion (differences above levels) is itself the tell. We report the bars and flag them "
     "rather than dropping them. The ESS levels contribution comes from cross-section instead: "
     "47% of 15 countries across regions, which is well-powered."),

    ("Scope of the trust finding",
     "Trust rests on the ESS: 36 European countries, one item, self-reported. 97% of countries "
     "significant with median individual R² 0.039. The SDG16 comparison is cross-sectional "
     "because only 16 of 163 country-series have the four years a time-series design needs. "
     "This is the most tentative of the three domains and should be framed as such."),

    ("Institutional confidence is not interpersonal trust",
     "SDG16's trust-adjacent series measure satisfaction with public services, perceived bribery "
     "and perceived inclusiveness in decision-making. These are conceptually distinct from 'most "
     "people can be trusted', and they do not survive an income control while interpersonal trust "
     "does. The commentary must be explicit that SDG16 is not a direct analogue, wherever the "
     "1.5% figure appears."),

    ("Three failure modes as the meta-finding",
     "The paper's contribution is arguably not the three domains but the three distinct ways a "
     "framework loses one: pooled construct, saturated variable, absent coverage. They need "
     "different remedies, which is what makes Act IV specific rather than rhetorical."),

    ("What we are not claiming",
     "No causal claim, and no verdict on the SDGs or HDI as development instruments. The claim is "
     "about what these frameworks can and cannot see when the question is individual lived "
     "experience — and it is bounded by ESS coverage on the trust half."),
]
