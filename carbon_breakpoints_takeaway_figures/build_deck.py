#!/usr/bin/env python3
"""Build the final narrative deck: What Bends the Curve? — Paris at ten.
v2: plain-language methods, and a 'How to read it' guide on every figure slide."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image
import os

MEDIA = "/tmp/claude-0/-home-user-HDI-Happiness/1513cf0d-fca1-52a3-b470-357bab9ee4f8/scratchpad/deck_media/ppt/media"
FIGS = "/home/user/HDI-Happiness/carbon_breakpoints_takeaway_figures/figures"
OUT = "/tmp/claude-0/-home-user-HDI-Happiness/1513cf0d-fca1-52a3-b470-357bab9ee4f8/scratchpad/what_bends_the_curve_final.pptx"

INK = RGBColor(0x21, 0x21, 0x21)
GRAY = RGBColor(0x55, 0x55, 0x55)
LGRAY = RGBColor(0x8A, 0x8A, 0x8A)
GREEN = RGBColor(0x1B, 0x78, 0x37)
BLUE = RGBColor(0x3A, 0x66, 0xA5)
RED = RGBColor(0xB3, 0x3A, 0x3A)
AMBER = RGBColor(0xC7, 0x7F, 0x00)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def box(s, x, y, w, h):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.text_frame.word_wrap = True
    return tb.text_frame


def para(tf, text, size=14, color=INK, bold=False, italic=False, first=False,
         space_after=6, align=PP_ALIGN.LEFT, font="Calibri"):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    r = p.add_run()
    r.text = text
    f = r.font
    f.size, f.bold, f.italic, f.name = Pt(size), bold, italic, font
    f.color.rgb = color
    return p


def runs(tf, parts, size=14, first=False, space_after=6, align=PP_ALIGN.LEFT, italic=False):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    for t, c, b in parts:
        r = p.add_run(); r.text = t
        r.font.size, r.font.bold, r.font.name = Pt(size), b, "Calibri"
        r.font.italic = italic
        r.font.color.rgb = c
    return p


def kicker_title(s, kicker, title, kcolor=GREEN):
    tf = box(s, 0.55, 0.3, 12.25, 1.0)
    para(tf, kicker, size=12, color=kcolor, bold=True, first=True, space_after=2)
    para(tf, title, size=24, color=INK, bold=True, space_after=0)


def fit_image(s, path, x, y, maxw, maxh):
    iw, ih = Image.open(path).size
    sc = min(maxw / iw, maxh / ih)
    w, h = iw * sc, ih * sc
    return s.shapes.add_picture(path, Inches(x + (maxw - w) / 2), Inches(y + (maxh - h) / 2),
                                Inches(w), Inches(h))


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def figure_slide(kicker, title, img, guide=None, takeaway=None, note="", kcolor=GREEN):
    s = slide()
    kicker_title(s, kicker, title, kcolor=kcolor)
    top = 1.32
    if takeaway:
        tf = box(s, 0.55, top, 12.25, 0.42)
        para(tf, takeaway, size=13, color=INK, bold=True, first=True, space_after=0)
        top += 0.44
    if guide:
        tf = box(s, 0.55, top, 12.25, 0.66)
        runs(tf, [("How to read it:  ", BLUE, True), (guide, GRAY, False)], size=12.5, first=True, space_after=0)
        top += 0.68
    fit_image(s, img, 0.35, top + 0.04, 12.63, 7.18 - top)
    notes(s, note)
    return s


M = lambda n: os.path.join(MEDIA, n)
F = lambda n: os.path.join(FIGS, n)

# ---------------------------------------------------------------- 1 · title
s = slide()
tf = box(s, 0.9, 1.7, 11.5, 3.6)
para(tf, "WHAT BENDS THE CURVE?", size=48, bold=True, first=True, space_after=8)
para(tf, "Paris at ten: long trends, a new acceleration, and the national transformations that carry the signal",
     size=20, color=GRAY, space_after=16)
runs(tf, [("Structural breaks · Kaya pathways · five decades of national decarbonization", GREEN, True)], size=15)
tf = box(s, 0.9, 5.9, 11.5, 0.9)
runs(tf, [("204 jurisdictions     ", INK, True), ("97 eligible national breaks     ", INK, True),
          ("7 mechanism families     ", INK, True), ("9 constructive decarbonizations", GREEN, True)],
     size=13.5, first=True)
notes(s, "Frame up front: this is a pro-Paris paper that takes measurement seriously. The question is not whether Paris matters, but what the observed record can attribute — and where the policy signal actually lives.")

# ---------------------------------------------------------------- 2 · framing
s = slide()
kicker_title(s, "THE QUESTION", "Paris is working — but through what?")
tf = box(s, 0.55, 1.6, 7.3, 5.4)
para(tf, "The good news is real.", size=17, bold=True, first=True, space_after=4)
para(tf, "Worst-case emissions scenarios have moved off the table, and global CO2 growth has slowed from +2.1% per year (1990–2015) to +0.4% per year since Paris.", size=15, color=GRAY, space_after=14)
para(tf, "The open question:", size=17, bold=True, space_after=4)
para(tf, "Is the global improvement a direct effect of the agreement — or the continuation of trends rooted decades earlier, which Paris coordinates and reinforces?", size=15, color=GRAY, space_after=14)
para(tf, "Our approach:", size=17, bold=True, space_after=4)
para(tf, "Rather than assuming treaty years are turning points, we let the data tell us when trends actually changed — globally and for every country with enough annual data — and then use historical evidence to ask why.", size=15, color=GRAY, space_after=0)
tf = box(s, 8.15, 1.6, 4.65, 5.4)
para(tf, "Why intensity comes first", size=17, bold=True, color=GREEN, first=True, space_after=6)
para(tf, "Emissions can be split into three moving parts:", size=14, color=GRAY, space_after=4)
para(tf, "CO2 growth = economic growth + change in fuel mix + change in energy efficiency", size=14, bold=True, space_after=10)
para(tf, "Emissions cannot bend until the fuel mix or efficiency improves faster. Intensity is the leading indicator: any policy effect must show up there first — before it can ever show up in emissions.", size=14, color=GRAY, space_after=8)
para(tf, "Unless intensity improves faster than the economy grows, emissions cannot stabilize.", size=14, color=INK, bold=True, space_after=0)
notes(s, "Set the sympathetic frame, then pivot to the identity: the mathematically required location of any policy signal is the intensity slopes. That justifies the paper's whole design.")

# ---------------------------------------------------------------- 3 · methods 1 (plain language)
s = slide()
kicker_title(s, "HOW WE MEASURE IT", "Finding the bend: two straight lines and a kink", kcolor=BLUE)
tf = box(s, 0.55, 1.55, 6.1, 5.5)
para(tf, "Three steps, no assumptions about treaty years", size=15.5, bold=True, first=True, space_after=8)
runs(tf, [("1.  ", BLUE, True), ("Plot each series on a log scale, so a straight line means a steady percentage change per year.", GRAY, False)], size=13.5, space_after=8)
runs(tf, [("2.  ", BLUE, True), ("Fit two straight lines that meet at a kink — the 'breakpoint'. Try every possible kink year and keep the one that fits the data best. That year is the estimate of when the trend changed.", GRAY, False)], size=13.5, space_after=8)
runs(tf, [("3.  ", BLUE, True), ("Stress-test the date: re-estimate it on many statistically reshuffled versions of the series. If the estimated year barely moves, the break is credible; if it jumps around, we say so.", GRAY, False)], size=13.5, space_after=12)
para(tf, "A breakpoint tells us when a trend changed — never, by itself, why. Historical evidence answers that separately.", size=13.5, color=INK, bold=True, space_after=8)
para(tf, "(Formally: y(t) = a + b·t + d·max(t−k, 0); slope b before year k, b+d after. Uncertainty via moving-block bootstrap; autocorrelation-robust standard errors for fixed-date tests.)", size=10.5, color=LGRAY, italic=True, space_after=0)
tf = box(s, 7.0, 1.55, 5.8, 5.5)
para(tf, "Two doors for any improvement", size=15.5, bold=True, first=True, space_after=8)
para(tf, "Carbon intensity — CO2 per dollar of output — can only improve through one of two doors:", size=13.5, color=GRAY, space_after=8)
runs(tf, [("Cleaner energy (C/E):  ", GREEN, True), ("less CO2 per unit of energy — fuel switching, nuclear, renewables, the power system.", GRAY, False)], size=13.5, space_after=8)
runs(tf, [("Less energy per dollar (E/GDP):  ", AMBER, True), ("efficiency, and changes in what the economy makes — industry versus services.", GRAY, False)], size=13.5, space_after=10)
para(tf, "We estimate the bend in the overall series and in both doors, for the world and for every country, with one identical procedure. Which door moved tells us what kind of transition happened — a fuel-mix bend points to energy policy or markets; an efficiency bend often points to economic change.", size=13.5, color=INK, space_after=0)
notes(s, "Keep this conversational: two lines and a kink, tried at every year; then shake the data to see if the date holds still. The 'two doors' framing sets up the mechanism logic used throughout Acts II-III.")

# ---------------------------------------------------------------- 4 · methods 2 (plain language)
s = slide()
kicker_title(s, "HOW WE MEASURE IT", "Which breaks do we trust — and when does a treaty get credit?", kcolor=BLUE)
tf = box(s, 0.55, 1.55, 5.5, 5.5)
para(tf, "A country's break counts only if:", size=15.5, bold=True, first=True, space_after=8)
for t in ["the series is long enough (40+ years, with at least 10 on each side of the break);",
          "the two-line model fits clearly better than a single straight line;",
          "the estimated year stays put when the data are reshuffled; and",
          "the change in slope is big enough to matter, not a statistical whisker."]:
    runs(tf, [("•  ", GREEN, True), (t, GRAY, False)], size=13.5, space_after=7)
para(tf, "204 jurisdictions → 158 with estimable series → 97 countries with a break that passes every test. Breaks close together in time are read as one national transition: 107 episodes in all.", size=13.5, color=INK, space_after=0)
tf = box(s, 6.35, 1.55, 6.45, 5.5)
para(tf, "A treaty year gets credit only if all five hold:", size=15.5, bold=True, first=True, space_after=8)
for i, t in enumerate(["the slope genuinely changes at the treaty year (by a robust statistical test);",
                       "the treaty year beats nearly all nearby 'placebo' years — because when a trend curves gently, almost any year looks significant;",
                       "the best-fitting year is within three years of the treaty;",
                       "the data-chosen break agrees with it; and",
                       "there is a documented domestic policy story that fits."], 1):
    runs(tf, [(f"{i}.  ", BLUE, True), (t, GRAY, False)], size=13.5, space_after=7)
para(tf, "This ladder is deliberately hard to climb. Many series pass step 1; few pass them all. We hold Paris itself to the same standard.", size=13.5, color=INK, bold=True, space_after=0)
notes(s, "The placebo idea in one line: a significant result at the treaty year means little if 1990 and 1994 are just as 'significant'. The ladder is the paper's discipline — and Act I applies it to Paris.")

# ---------------------------------------------------------------- 5 · four acts
s = slide()
kicker_title(s, "THE ARGUMENT", "Four acts")
acts = [("I", "Is the global bend Paris?", "Global curves bent in the 1970s; since ~2013 they are bending faster. The acceleration is real — its attribution is not yet identified."),
        ("II", "What bends national curves?", "97 eligible breaks scattered across five decades and seven historically validated mechanism families."),
        ("III", "Did the bends count?", "Transition quality separates genuine decarbonization from recessions, disruption, offshoring, and growth that outruns efficiency."),
        ("IV", "Can we trust the story?", "Event-timing tests against chance, external ratings, consumption-based accounting — and unresolved cases reported as such.")]
x = 0.55
for roman, t, d in acts:
    tf = box(s, x, 1.75, 2.95, 4.6)
    para(tf, roman, size=40, bold=True, color=GREEN, first=True, space_after=6)
    para(tf, t, size=16, bold=True, space_after=8)
    para(tf, d, size=12.5, color=GRAY, space_after=0)
    x += 3.12
notes(s, "Act I is reframed: not 'treaties failed' but 'the record shows a real recent acceleration whose timing cannot yet separate Paris from the renewables cost decline.'")

# ---------------------------------------------------------------- 6 · Act I fig 1
figure_slide("ACT I · IS THE GLOBAL BEND PARIS?",
             "Global curves first bent in the 1970s",
             F("takeaway_fig01_global_bend_predates_treaties.png"),
             guide="Gray dots are the world's CO2 per dollar of output each year (1965 = 100). The red line is the best-fitting pair of straight lines; where they meet — 1973 — is the estimated break. Rio and Paris are marked for comparison: both come long after the bend. The lower panel repeats the estimate for each component; the whiskers show how uncertain each break year is.",
             note="C/GDP breaks ~1973, E/GDP ~1974 — the oil-shock era. C/E's point estimate is 1992 but its interval spans 1978–2011: it does not uniquely identify Rio. Robust to consumption-based emissions, excluding former Soviet economies, PPP GDP.")

# ---------------------------------------------------------------- 7 · Act I fig 2A
figure_slide("ACT I · IS THE GLOBAL BEND PARIS?",
             "Paris at ten: ahead of trend — but the bend began earlier",
             F("takeaway_fig02a_paris_and_the_long_trend.png"),
             guide="We draw the 1990–2015 trend, then extend it past Paris (dashed line) with a band showing where future years should fall if nothing changed. Red dots are the actual years since Paris. Dots below the band mean the world is now improving faster than its old trend — clearly so for the fuel mix, not at all for energy efficiency.",
             note="A real supply-side acceleration (C/E −0.7 pp/yr, NW t=4.3; C/GDP −0.9, t=2.9). But onsets from 2011–2016 fit the full record about equally well (best 2013), and E/GDP shows no acceleration. What an effective Paris should look like — and not yet separable from the renewables cost collapse that preceded the treaty.")

# ---------------------------------------------------------------- 8 · Act I fig 2B
figure_slide("ACT I · IS THE GLOBAL BEND PARIS?",
             "The arithmetic: intensity must fall as fast as GDP grows",
             F("takeaway_fig02b_stabilization_arithmetic.png"),
             guide="Each bar is an average annual growth rate. By construction, the red emissions bar equals the gray GDP bar plus the two colored intensity bars. Emissions stop growing only when the colored bars together are as long as the gray one — the dotted line marks that target. We are closer than before Paris, but not there.",
             note="Emissions growth slowed from +2.1 to +0.4%/yr after 2015 — but roughly two-thirds of the slowdown is slower GDP growth; one-third is the cleaner fuel mix. The gap to the dotted line is the remaining task.")

# ---------------------------------------------------------------- 9 · Act I placebo
figure_slide("ACT I · IS THE GLOBAL BEND PARIS?",
             "Why a treaty-year result needs a placebo test",
             F("takeaway_fig02_placebo_test.png"),
             guide="Top: we place the break at every possible year, one at a time, and record how much better the model fits. Rio fits well — but so do many neighboring years, which is why a good fit at a treaty year proves little on its own. Bottom: the share of country series with a significant change at each treaty year (left point) versus the share where the treaty year also beats its neighbors (right point).",
             note="Nominal treaty-date significance is common (48–69% of series); date-uniqueness is rare (Rio: 10/21/34 series by component; Paris: 14/5/6). The same discipline applied to Paris's decade dates the global acceleration's onset to ~2013.")

# ---------------------------------------------------------------- 10 · Act I verdict
s = slide()
kicker_title(s, "ACT I · VERDICT", "The global record can show an acceleration — not yet its author")
tf = box(s, 0.55, 1.6, 6.05, 5.4)
para(tf, "What the data establishes", size=16, bold=True, color=GREEN, first=True, space_after=6)
for t in ["A real post-2013 supply-side acceleration: the fuel mix is improving −0.5%/yr after a flat quarter-century; overall intensity is falling ~0.9 pp/yr faster than its Rio-to-Paris trend.",
          "Emissions growth slowed from +2.1 to +0.4%/yr — the direction an effective Paris requires.",
          "No acceleration on the demand side: energy efficiency continues its 50-year trend, no faster."]:
    runs(tf, [("•  ", GREEN, True), (t, GRAY, False)], size=13.5, space_after=7)
tf = box(s, 7.0, 1.6, 5.8, 5.4)
para(tf, "Why attribution stays open", size=16, bold=True, color=RED, first=True, space_after=6)
for t in ["Timing: start years from 2011 to 2016 fit about equally well (best: 2013) — indistinguishable from the renewables cost collapse that preceded Paris.",
          "Power: with only 8 post-Paris years, we could only detect a very large acceleration — Paris would have had to double a 50-year trend to prove itself already.",
          "Aggregation: China's WTO-era coal boom flattened the global fuel-mix baseline; the world series is a China-weighted average that hides national signals.",
          "Design: Paris works through national pledges and national transformation — its signature should appear country by country. So we look there."]:
    runs(tf, [("•  ", RED, True), (t, GRAY, False)], size=13.5, space_after=7)
notes(s, "The hinge of the talk: the non-attribution is not a failure of Paris — it is the reason the analysis must descend to the national level, where attribution machinery has power.")

# ---------------------------------------------------------------- 11 · Act II timeline
figure_slide("ACT II · WHAT BENDS NATIONAL CURVES?",
             "97 national breaks, five decades of economic history",
             F("takeaway_fig03_when_and_why_curves_bend.png"),
             guide="Top: each dot is one country, placed at its estimated break year; green triangles are the nine policy-enabled cases. Shaded bands mark major economic and political episodes; Rio and Paris are the two dashed lines. Bottom: how often a documented historical event falls near a country's break (red) versus what randomly chosen years would produce (blue).",
             note="No common treaty era: breaks scatter 1970–2013 and pile up around oil shocks, post-Cold-War upheaval, crises, and the renewables era. Event alignment: 45% vs 17% within 2 years; 80% vs 37% within 5; 70% vs 33% inside the episode.")

# ---------------------------------------------------------------- 12 · Act II census
figure_slide("ACT II · WHAT BENDS NATIONAL CURVES?",
             "What accompanied the bends",
             F("takeaway_fig04_mechanism_census.png"),
             guide="One square per country, grouped by the historical process best supported by documentary evidence around its break. Green marks the countries where climate policy and low-carbon technology are that best-supported process; light gray means the record cannot yet explain the break — reported honestly rather than forced into a category.",
             note="Fuel and energy markets 22, restructuring 18, political disruption 11, macro shocks 9, development and access 6, policy 9, unresolved 22. Author-coded against authoritative sources with a stopping rule — interpretations, not causal estimates.")

# ---------------------------------------------------------------- 13 · Act III framework
s = slide()
kicker_title(s, "ACT III · DID THE BENDS COUNT?", "Seven mechanisms, six verdicts", kcolor=AMBER)
tf = box(s, 0.55, 1.5, 6.05, 5.7)
para(tf, "MECHANISMS — what accompanied the bend", size=14, bold=True, first=True, space_after=6)
for name, d in [("Policy-enabled low carbon", "deliberate climate/energy policy made physical: infrastructure, fuel mix, market design"),
                ("Fuel & energy markets", "market-driven fuel switching or supply transformation"),
                ("Economic restructuring", "industry to services, liberalization, post-socialist transition"),
                ("Macroeconomic shock", "recessions and financial crises that cut energy use"),
                ("Political disruption", "wars, state collapse, sanctions, regime change"),
                ("Development & energy access", "electrification and modernization"),
                ("No attributed mechanism", "a real, eligible break the record cannot yet explain (22 of 97)")]:
    runs(tf, [(name + " — ", INK, True), (d + ".", GRAY, False)], size=12, space_after=4)
tf = box(s, 7.0, 1.5, 5.8, 5.7)
para(tf, "VERDICTS — four tests of the outcome", size=14, bold=True, first=True, space_after=4)
para(tf, "Did the trend improve? Did it last? Did absolute CO2 actually fall? Was the underlying process constructive?", size=12.5, italic=True, color=GRAY, space_after=8)
for name, n, d in [("Constructive persistent decarbonization", 9, "passes all four — the gold standard"),
                   ("Persistent fuel substitution", 13, "durable supply-side switch; narrower transformation"),
                   ("Intensity gain; CO2 still rising", 12, "relative gain overwhelmed by growth"),
                   ("Contractionary / disruptive", 20, "the 'improvement' is a crisis in disguise"),
                   ("Incomplete / nonpersistent", 21, "the bend reversed or did not hold"),
                   ("Outcome not classifiable", 22, "too little post-break evidence")]:
    runs(tf, [(f"{name} ", INK, True), (f"({n}) — ", GREEN if n == 9 else LGRAY, True), (d + ".", GRAY, False)], size=12, space_after=4)
notes(s, "The reading key for everything that follows. Note the two distinct 22s: mechanism-unresolved and outcome-unclassifiable are different sets.")

# ---------------------------------------------------------------- 14 · sankey
figure_slide("ACT III · DID THE BENDS COUNT?",
             "From mechanism to verdict: 97 countries, six outcomes",
             M("image4.png"),
             guide="Each ribbon carries countries from the process that accompanied their break (left) to how the outcome is judged (right); ribbon width is the number of countries. Follow any left-hand category to see where those transitions actually ended up.",
             note="Shocks flow into contraction; restructuring often ends in 'intensity gain, CO2 rising'. Only nine countries end in constructive persistent decarbonization.", kcolor=AMBER)

# ---------------------------------------------------------------- 15 · quadrant
figure_slide("ACT III · DID THE BENDS COUNT?",
             "Lower intensity is not the same as falling emissions",
             F("takeaway_fig05_bend_vs_success.png"),
             guide="Each dot is a country. Further right means its intensity trend improved more after the break; below the dashed horizontal line means absolute emissions are actually falling. Success lives only in the lower right — and most improving countries sit above the line, where growth still outruns their gains.",
             note="Raw counts: 55 favorable bends with rising CO2; 19 with falling CO2. The stricter classification narrows these to 12 and 9. Green triangles: the 9 policy-enabled cases — Bhutan and Paraguay improve intensity while emissions still rise, so policy-enabled and constructive are overlapping but different sets.", kcolor=AMBER)

# ---------------------------------------------------------------- 16 · the nine
figure_slide("ACT III · DID THE BENDS COUNT?",
             "The nine constructive persistent decarbonizations",
             M("image7.png"),
             takeaway="Sweden 1986 · Finland 1993 · Hungary 1996 · Switzerland 1999 · Nauru 1999 · Denmark 2002 · Portugal 2004 · United Kingdom 2010 · Ireland 2012",
             guide="Each panel is one country. Both lines are set to 100 at its break year: blue is carbon intensity, red is absolute CO2. The defining test is that both fall together after the break (shaded region) — intensity improved, and total emissions genuinely declined.",
             note="Six of nine are policy-enabled; Hungary, Nauru, and Ireland arrived via restructuring. Caveat: Nauru is a micro-state whose 'restructuring' is the phosphate collapse — treat with care.", kcolor=AMBER)

# ---------------------------------------------------------------- 17 · nineteen cutters
figure_slide("ACT III · DID THE BENDS COUNT?",
             "Nineteen countries cut emissions — ten don't earn the verdict",
             M("image8.png"),
             guide="Each row is a country where absolute CO2 fell after a favorable bend. The whisker is the uncertainty around its break year; rows are grouped by the verdict, and each label names the best-supported mechanism. Falling emissions alone are not enough — the route matters.",
             note="Routes around the constructive verdict: fuel substitution (5), evidence limits (4), collapse (1). Netherlands 1975: gas substitution forty years before US shale. Somalia 1985: collapse mimics decarbonization in every raw statistic; only the persistence screen catches it. Breaks span 1975–2012 — no treaty era here either.", kcolor=AMBER)

# ---------------------------------------------------------------- 18 · geography
s = slide()
kicker_title(s, "ACT III · THE GEOGRAPHY", "Mechanisms are regional; success is concentrated", kcolor=AMBER)
tf = box(s, 0.55, 1.32, 12.25, 0.66)
runs(tf, [("How to read it:  ", BLUE, True),
          ("Left map: each country is colored by the process that accompanied its break. Right map: the same countries colored by outcome verdict — dark green marks the nine constructive cases, concentrated in northern Europe.", GRAY, False)],
     size=12.5, first=True, space_after=0)
fit_image(s, M("image9.png"), 0.30, 2.05, 6.35, 5.0)
fit_image(s, M("image10.png"), 6.75, 2.05, 6.35, 5.0)
notes(s, "Fuel-market transformations cluster in the Americas and MENA; restructuring across Asia-Pacific; policy-enabled cases in northern Europe. Right: much of the map is contraction, incompleteness, or intensity gains overwhelmed by growth.")

# ---------------------------------------------------------------- 19 · Act IV ratings
figure_slide("ACT IV · CAN WE TRUST THE STORY?",
             "Independent raters recognize the same countries",
             F("takeaway_fig06_external_corroboration.png"),
             guide="Each dot is a country covered by the rating, placed by where it ranks among covered countries (right = rated better). Green triangles are our policy-enabled cases; the vertical bars mark each group's median. The policy cases rank high on both ratings — but only 3 and 2 of them are covered, so we show every point rather than hide the small sample.",
             note="Median CAT percentile ~64 vs 34; CCPI ~91 vs 44. Corroborative, not definitive.", kcolor=RED)

# ---------------------------------------------------------------- 20 · robustness & limits
s = slide()
kicker_title(s, "ACT IV · CAN WE TRUST THE STORY?", "Robustness, corroboration, and honest limits", kcolor=RED)
col = [("Consumption-based accounting",
        "When emissions embodied in trade are assigned to consumers instead of producers, only 6 of 17 comparable countries keep a break within 5 years of their production-based date; the median shift is ~12 years. Some 'domestic' transitions partly reflect offshoring — a main result, not a footnote."),
       ("Carbon pricing & policy stringency",
        "Carbon pricing is associated with a cleaner fuel mix in panel models with country and year controls; effects on the other components are imprecise. Policy-stringency data cover only 15 of 28 focal countries. Associational, not causal."),
       ("Event-timing validation",
        "45% of documented events fall within 2 years of the estimated break versus ~17% if dates were drawn at random; 80% vs 37% within 5 years; 70% vs 33% inside the episode. The historical classifications carry real temporal information — far beyond retrospective storytelling."),
       ("What breakpoints can't tell you",
        "Break timing identifies change, not cause. Attribution and outcome classification each leave 22 cases open — restraint that makes the resolved 75% credible. And there is no counterfactual: a treaty that prevents backsliding produces no break at all.")]
xs, ys = [0.55, 7.0, 0.55, 7.0], [1.55, 1.55, 4.35, 4.35]
for (t, d), x, y in zip(col, xs, ys):
    tf = box(s, x, y, 5.9, 2.7)
    para(tf, t, size=15, bold=True, first=True, space_after=4)
    para(tf, d, size=12, color=GRAY, space_after=0)
notes(s, "The credibility slide. If asked about causality: the design lock is explicit about supported vs unsupported claims — lean on it.")

# ---------------------------------------------------------------- 21 · verdict
figure_slide("THE VERDICT",
             "Curves bend everywhere; decarbonization is rare",
             M("image12.png"),
             guide="All 97 breaks looked statistically favorable. The colors show what they turned out to be once persistence, mechanism, and absolute emissions are checked — only the dark green block on the right is unambiguous decarbonization.",
             note="None of this heterogeneity aligns on a treaty date. The treaty question dissolves into 97 national stories; nine end in unambiguous decarbonization.")

# ---------------------------------------------------------------- 22 · close
s = slide()
tf = box(s, 0.9, 1.15, 11.5, 1.9)
para(tf, "Global agreements can organize climate action —", size=27, bold=True, first=True, space_after=2)
para(tf, "durable national transformations bend the curve.", size=27, bold=True, color=GREEN, space_after=0)
tf = box(s, 0.9, 3.15, 11.5, 3.3)
for t in ["Global curves bent in the 1970s; since ~2013 they bend faster — a real supply-side acceleration whose timing cannot yet separate Paris from the renewables revolution it helped consolidate.",
          "Treaty-adjacent signals exist — especially around Rio — but few survive placebo scrutiny, and national transitions scatter across five decades.",
          "Favorable bends often reflect recession, disruption, deindustrialization, or offshoring; intensity gains are routinely overwhelmed by growth.",
          "Nine countries pair persistent intensity declines with falling absolute CO2 — policy made physical in fuel mix, infrastructure, and economic structure."]:
    runs(tf, [("—  ", GREEN, True), (t, GRAY, False)], size=14, space_after=8)
tf = box(s, 0.9, 6.55, 11.5, 0.7)
para(tf, "Structural breaks say when · Kaya says through which pathway · historical validation says what plausibly happened · transition quality says whether it mattered",
     size=13, italic=True, color=LGRAY, first=True, align=PP_ALIGN.CENTER)
notes(s, "End on the closing line and the four-part method signature.")

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
