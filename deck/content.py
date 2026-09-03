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
        ("II", "At the levels, education and health carry the frameworks.",
         "Both domains, across all three frameworks at once. Health is 4th of 17 SDG goals and the "
         "weakest HDI component; education looks 12th of 17 — until you unpool it."),
        ("II-a", "Trust: the domain only people can report, and what it is worth.",
         "Second strongest on people, ahead of education, and invisible to both development "
         "frameworks. It also survives differencing — worth +0.20 life-satisfaction points, "
         "with no person answering both questions."),
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
            ("+0.44 → +0.20", "HDI × ESS pooled, levels → differences — swap the instrument"),
        ],
        "thesis": (
            "The SDG null invites an easy dismissal: sprawling framework, uneven coverage, so "
            "the absence of a within-country signal says more about the instrument than about "
            "development. Test that by changing one leg of the design at a time. If the collapse "
            "is an artefact of the SDGs, it should not survive."
        ),
        "close": (
            "Three pairings, the same asymmetry in all of them: development composites predict wellbeing "
            "between units and barely track it within one over time. That holds whichever framework and "
            "whichever wellbeing instrument you use. So the levels are where to look next — and the "
            "differences question comes back in Act II-a, once the predictor is no longer a composite."
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
                    "Run country by country it returns 8% at levels and 16% in differences across 25 countries, "
                    "which is a null test rather than a finding: the ESS has seven survey rounds where the WHR "
                    "panels have thirteen years, and panel b shows what that costs — at seven observations a "
                    "genuine correlation of 0.5 is recovered in about 3% of units. Differences landing above "
                    "levels is the tell that the test is not working, not a result.",
                    "The comparison is like-for-like on the outcome: the Cantril ladder is a life evaluation, "
                    "so the ESS analogue is its life-satisfaction item rather than its separate happiness "
                    "question. Pooled across countries, where the power is, the HDI's within-country "
                    "association falls from r = +0.44 at levels to +0.20 in differences — and stays there "
                    "(+0.19) once survey-round effects are removed, so it is not a shared shock across "
                    "European countries.",
                    "So the HDI attenuates by about 55% against ESS life satisfaction — substantial, but short "
                    "of the clean null the Cantril ladder gives on the full panel, where across 1,548 "
                    "country-year changes the HDI goes from +0.15 to −0.02 and is not significant at all. The "
                    "collapse survives the instrument swap in direction and roughly in magnitude, on a much "
                    "smaller and Europe-only panel.",
                    "The ESS also corroborates the levels half in cross-section, where it has plenty of power: "
                    "subnational HDI predicts ESS life satisfaction across regions inside each country in 47% "
                    "of 15 countries, sitting on top of the 42% the HDI reaches nationally. So the collapse "
                    "survives the instrument swap. What it does not survive — and this is Act II-a — is "
                    "changing the predictor from a development composite to the domain measures themselves.",
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
        "title": "At the levels: education and health, across three frameworks",
        "key_numbers": [
            ("41% vs 19%", "HDI: mean years of schooling leads, life expectancy is weakest"),
            ("12.7% vs 3.3%", "SDG4 access indicators alone vs all 35 pooled"),
            ("89% / 100%", "ESS countries significant on people: education / health"),
        ],
        "thesis": (
            "If the levels are where development and wellbeing meet, the useful question is which "
            "components are carrying that association — asked of all three frameworks at once, "
            "domain by domain, rather than one framework's internals at a time. Two domains come "
            "out: education and health. Both need a second look before they agree with each other."
        ),
        "close": (
            "Health and education are what the frameworks can see at the levels. Health registers "
            "wherever it is measured somewhere that still varies; education registers only when the "
            "construct being counted is access. That is two domains — and, so far, it is everything "
            "these frameworks are able to test. The next section is the domain that only appears "
            "once you measure people rather than countries."
        ),
        "beats": [
            {
                "label": "All three domains, at the levels",
                "heading": "Education, health and social trust all predict life satisfaction — where they can be measured",
                "body": [
                    "Before drilling into any one domain, the shape of the whole result. Test each of "
                    "education, health and social trust against wellbeing at the levels, in every framework "
                    "that measures it, on one comparable unit: % of countries FDR-significant. Where a "
                    "framework can test a domain, the domain matters — the question that varies is which "
                    "frameworks can test which domains.",
                    "The HDI and the SDGs can both test education and health, and both find something, "
                    "though not always in agreement with each other at face value. Neither can test social "
                    "trust at all — there is no HDI bar for it, and the SDGs' nearest series measure a "
                    "different construct. That gap is the subject of the next section. This one is about "
                    "the two domains every framework here can at least attempt.",
                ],
                "figure": "domains_at_levels_comparison.png",
                "caption": "All three domains across all three frameworks, all on % of countries "
                           "FDR-significant. Trust has no HDI bar because the HDI does not measure it.",
            },
            {
                "label": "Education, across frameworks",
                "heading": "Strong wherever you measure attainment; the SDGs' 3.3% is the outlier that needs explaining",
                "body": [
                    "Inside the HDI, education is not one component but two, and both lead the index at "
                    "levels: mean years of schooling 41%, expected years of schooling 33% — both ahead of "
                    "the composite itself (42% is close, but that's the whole index against two of its five "
                    "parts). On people, in the ESS, years of schooling is significant in 89% of countries.",
                    "Against that, SDG4 pooled across all 35 of its series returns 3.3% — twelfth of "
                    "seventeen goals, which taken at face value says education barely matters. Three "
                    "measurements agree and the fourth contradicts them, which is a sign to look inside "
                    "the fourth rather than to average it in as if it settled anything.",
                ],
                "figure": "education_levels_comparison.png",
                "caption": "Education across four measurements: ESS individual, HDI expected years of "
                           "schooling, SDG4 access only, SDG4 pooled across all 35 series.",
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
                    "that does. Unpooled, education's access series would rank third among the seventeen "
                    "goals rather than twelfth — and would agree with the HDI instead of contradicting it.",
                ],
                "figure": "sdg4_unpooled.png",
                "caption": "SDG4 split by construct. Access and participation (12.7%) against equity and "
                           "parity ratios (2.5%), infrastructure (2.0%) and learning outcomes (0.9%).",
            },
            {
                "label": "Health, across frameworks",
                "heading": "The strongest domain on people; the weakest component of the HDI; still ranks 4th of 17 SDG goals",
                "body": [
                    "Self-rated health is the single strongest predictor of life satisfaction in the ESS: "
                    "every country significant, median individual R² 0.092 — roughly fifteen times "
                    "education's. In the SDGs, health (Goal 3) reaches 11.5% of country-indicator pairs, "
                    "fourth of seventeen goals and first among the goals with substantive coverage; it also "
                    "dominates the database's individual-series ranking, with 16 of the top 25 most "
                    "predictive series falling under Goal 3 — survival measures, infant and under-five "
                    "mortality, stunting, sanitation, drinking water.",
                    "In the HDI, health's proxy is life expectancy, and it is last of five components at "
                    "19%, against 41% for mean years of schooling. The domain is not weak; the HDI's chosen "
                    "proxy for it is. The top 100 countries span 81 to 85 years of life expectancy, and a "
                    "variable with that little range left cannot carry much association, whatever the "
                    "underlying domain does. Same domain, three variables, three very different-looking "
                    "results — and it is the variable doing the work, not the domain.",
                ],
                "figure": "health_levels_comparison.png",
                "caption": "Health measured three ways. The HDI result is about life expectancy's "
                           "saturation, not about health.",
            },
        ],
    },

    {
        "numeral": "II-a",
        "title": "Trust: the domain only people can report, and what it is worth",
        "key_numbers": [
            ("97%", "ESS countries where social trust is significant at levels"),
            ("+0.20 pts / 59%", "trust's differences effect, share of a typical round-to-round move"),
            ("93%", "of that effect retained with predictor and outcome from disjoint respondents"),
        ],
        "thesis": (
            "Neither the HDI nor the SDGs measure interpersonal trust. The ESS does, at the individual "
            "level, which is also the level at which the differences half of Act I can finally be "
            "answered — not just whether a domain survives differencing, but what a change in it is "
            "worth in life-satisfaction points."
        ),
        "close": (
            "Social trust is the second-strongest domain on people, ahead of education, and it is the "
            "one domain neither development framework collects. It also survives differencing where "
            "development composites do not: a country whose trust rises between ESS rounds sees life "
            "satisfaction rise with it, by an amount worth more than half of what life satisfaction "
            "typically moves round to round — and that holds with no person answering both questions."
        ),
        "beats": [
            {
                "label": "Social trust, at levels",
                "heading": "Second strongest domain on people; absent from both development frameworks",
                "body": [
                    "Interpersonal trust — 'generally speaking, would you say that most people can be "
                    "trusted?' — is significant in 35 of 36 ESS countries, with a median individual R² of "
                    "0.039: below self-rated health, well above years of schooling.",
                    "The HDI does not measure trust in any form. The SDG framework's nearest thing is Goal "
                    "16's thirteen series, and they measure something else — satisfaction with public "
                    "services, perceived bribery, perceived inclusiveness in decision-making. Institutional "
                    "confidence and interpersonal trust are distinct constructs, and coverage compounds the "
                    "mismatch: median one observation per country-series against six for the database "
                    "overall, and 147 of 163 country-series cannot support a time-series design at all.",
                    "Education's and health's problems, in the previous section, were about which variable "
                    "to count inside a domain the frameworks already have. Trust's is categorically "
                    "different: there is no variable to choose between, because the domain was never "
                    "collected in the first place.",
                ],
                "figure": "trust_coverage_comparison.png",
                "caption": "Interpersonal trust in the ESS against the closest SDG counterpart and an "
                           "absent HDI one. The asterisked bar is a different construct.",
            },
            {
                "label": "What trust is worth in differences",
                "heading": "A country's rising trust predicts rising life satisfaction — and the effect is not small",
                "body": [
                    "Act I left the differences half of the argument unresolved, because the per-country "
                    "design spends its power on 25 separate tests of seven points each. Pool the same "
                    "within-country question across all countries and it has the power to answer: the "
                    "collapse is not a property of differencing in general, it is specific to what you "
                    "differenced. Development composites collapse. The domain measures do not, all of them.",
                    "In points: a one-SD change in a country's trust reading between ESS rounds predicts a "
                    "+0.20 point change in mean life satisfaction, on the 0–10 scale — 59% of a typical "
                    "round-to-round swing in life satisfaction itself. Health's equivalent effect is +0.14 "
                    "points, 41% of a typical swing. Education and the HDI composite are not "
                    "distinguishable from zero. These are not curiosities; they are the size of the thing.",
                    "The obvious objection is common-method variance — the same person answers the trust "
                    "question and the life-satisfaction question in the same sitting, so of course they "
                    "move together. That is testable: split each country-round's respondents at random, "
                    "take the trust mean from one half and life satisfaction from the other, so no person "
                    "answers both. Trust retains 93% of its estimate this way, health 88%. The association "
                    "is between people in a country, not inside a questionnaire.",
                    "What still bounds the claim is cross-source replication. Against the World Happiness "
                    "Report ladder, health's differences result survives (+0.20) and trust's does not "
                    "(+0.06, not significant) — plausibly because that pairing sets ESS rounds against a "
                    "different sample with its own fieldwork timing, and trust is the weaker signal to "
                    "begin with, so it has less room before vanishing. Read as a bound, not a refutation: "
                    "trust has not yet been corroborated on an independent wellbeing instrument, and health "
                    "has. That is the honest state of the evidence, and it is why the recommendation in "
                    "Act IV treats trust as the most tentative of the three.",
                ],
                "figure": "domains_survive_differences.png",
                "caption": "Panel a: the differences effect converted to life-satisfaction points. Panel b: "
                           "the correlation evidence behind it, with split-half validation.",
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
            "construction choices made for other reasons — that one domain is missing outright, "
            "and that the domain measures track wellbeing dynamically in a way the composites do not."
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
                    "The shape of what follows, before the detail. Two of the three domains are already inside "
                    "these frameworks — health, and the access half of education — and on this evidence they "
                    "are the two that track lived experience. The suggestion is not to add a wellbeing pillar "
                    "but to let those two carry that weight explicitly: elevate them as wellbeing-relevant "
                    "highlights, measured with variables that still vary, with social trust flagged as a "
                    "likely third that neither framework can currently see.",
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
                    "The caveats stay attached, and they are about coverage rather than about whether the "
                    "association is real. It rests on 36 European countries and one survey item, and it has "
                    "not yet been corroborated against an independent wellbeing instrument the way health has. "
                    "What it is not is a questionnaire artefact: with predictor and outcome taken from "
                    "different respondents, the within-country result holds at +0.55. So this is the most "
                    "tentative of the three recommendations on scope, and the one where the cost of being "
                    "right and not measuring is highest — because a domain no framework collects cannot show "
                    "up as a gap in any framework's own diagnostics.",
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
    ("hdi_full_structure.png",
     "HDI composite and its five components, in full",
     "Levels and first differences for all five, Benjamini–Hochberg corrected within each "
     "country. The source for the 41%/33%/19% component figures cited in Act II."),
    ("sdg_indicator_top20.png",
     "Top 25 SDG series by levels significance",
     "Sixteen of the 25 most predictive individual series in the whole SDG database are "
     "Goal 3 health indicators — the source for Act II's health ranking."),
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

    ("Which ESS wellbeing item, and why",
     "The deck runs on ESS life satisfaction throughout, because the WHR Cantril ladder is a life "
     "evaluation and that is the like-for-like analogue. The ESS happiness item was run as a check "
     "and agrees (trust +0.59 identical; health +0.26 against +0.40; education null in both), so "
     "nothing turns on the choice — with one exception worth knowing: the HDI's differences result "
     "against happiness reads +0.31 raw but +0.17 net of survey-round effects, where the life "
     "satisfaction result is +0.20 either way. Numbers in processed/differences_robustness.csv."),

    ("Robustness of the differences result",
     "Two checks beyond the item choice. Removing survey-round effects leaves health and trust "
     "intact (+0.42, +0.58) rather than reducing them, so they are idiosyncratic country movement "
     "and not shocks common to a round. And the split-half design — predictor and outcome from "
     "disjoint respondents — rules out common-method variance, with trust retaining 93%. What "
     "remains untested is replication of the trust result on an independent wellbeing instrument."),

    ("Where the effect-size numbers come from",
     "Act II-a's '+0.20 pts / 59%' is OLS of the change in ESS life satisfaction on the change in "
     "the predictor, round fixed effects, SEs clustered by country (processed/"
     "differences_effect_sizes.csv). Trust: b=0.56 per point of trust (t=6.2), health: b=1.59 per "
     "point of good-health (t=2.7). Effect per 1 SD of the predictor's typical round-to-round move, "
     "benchmarked against 0.35 pts, the SD of life satisfaction's own round-to-round move. Education "
     "and the HDI composite are not distinguishable from zero at conventional significance."),

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
     "significant at levels; +0.59 within-country in first differences, and +0.55 with predictor "
     "and outcome drawn from disjoint respondents, so it is not a common-method artefact. What is "
     "still missing is corroboration against an independent wellbeing instrument: against the WHR "
     "ladder it is +0.06 n.s. in differences, plausibly attenuation from pairing two samples with "
     "different fieldwork timing, but unproven either way. Health has that corroboration and trust "
     "does not — worth stating plainly rather than leaning on trust as hard as on health."),

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
