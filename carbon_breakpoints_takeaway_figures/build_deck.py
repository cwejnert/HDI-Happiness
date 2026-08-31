#!/usr/bin/env python3
"""Build the final narrative deck: What Bends the Curve? — Paris at ten."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
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

W, H = Inches(13.333), Inches(7.5)
prs = Presentation()
prs.slide_width, prs.slide_height = W, H
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


def runs(tf, parts, size=14, first=False, space_after=6, align=PP_ALIGN.LEFT):
    """parts: list of (text, color, bold)"""
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    for t, c, b in parts:
        r = p.add_run(); r.text = t
        r.font.size, r.font.bold, r.font.name = Pt(size), b, "Calibri"
        r.font.color.rgb = c
    return p


def kicker_title(s, kicker, title, tcolor=INK, kcolor=GREEN):
    tf = box(s, 0.55, 0.28, 12.25, 1.15)
    para(tf, kicker, size=12, color=kcolor, bold=True, first=True, space_after=2)
    para(tf, title, size=27, color=tcolor, bold=True, space_after=0)


def fit_image(s, path, x, y, maxw, maxh, align="center"):
    iw, ih = Image.open(path).size
    scale = min(maxw / iw, maxh / ih)
    w, h = iw * scale, ih * scale
    if align == "center":
        x = x + (maxw - w) / 2
    y = y + (maxh - h) / 2
    return s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def figure_slide(kicker, title, img, takeaway=None, note="", src_note=None, img_top=1.45):
    s = slide()
    kicker_title(s, kicker, title)
    top = img_top
    if takeaway:
        tf = box(s, 0.55, 1.32, 12.25, 0.45)
        para(tf, takeaway, size=13.5, color=GRAY, first=True, space_after=0)
        top = max(top, 1.82)
    fit_image(s, img, 0.35, top, 12.63, 7.06 - top)
    if src_note:
        tf = box(s, 0.55, 7.08, 12.25, 0.35)
        para(tf, src_note, size=9, color=LGRAY, first=True, space_after=0)
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
para(tf, "Rather than assuming treaty years are turning points, we estimate structural breaks from the data — globally and for every country with adequate annual series — then use historical evidence to ask why the trend changed.", size=15, color=GRAY, space_after=0)
tf = box(s, 8.15, 1.6, 4.65, 5.4)
para(tf, "Why intensity comes first", size=17, bold=True, color=GREEN, first=True, space_after=6)
para(tf, "growth of CO2  =  growth of GDP", size=14, space_after=0, font="Consolas")
para(tf, "  +  change in C/E  (fuel mix)", size=14, space_after=0, font="Consolas")
para(tf, "  +  change in E/GDP  (efficiency)", size=14, space_after=10, font="Consolas")
para(tf, "Emissions cannot bend until an intensity slope accelerates. Intensity is the leading indicator: any policy signal must appear there first — on carbon or energy intensity, not necessarily on emissions.", size=14, color=GRAY, space_after=8)
para(tf, "Unless the intensity terms outpace GDP growth, emissions cannot stabilize.", size=14, color=INK, bold=True, space_after=0)
notes(s, "Set the sympathetic frame, then pivot to the identity: the mathematically required location of any policy signal is the intensity slopes. That justifies the paper's whole design.")

# ---------------------------------------------------------------- 3 · methods 1
s = slide()
kicker_title(s, "METHODS", "What a breakpoint means — and the Kaya lens", kcolor=BLUE)
tf = box(s, 0.55, 1.6, 6.1, 5.4)
para(tf, "The breakpoint model", size=16, bold=True, first=True, space_after=6)
para(tf, "y(t) = a + b·t + d·max(t − k, 0) + e(t)", size=14, font="Consolas", space_after=6)
para(tf, "b is the pre-break slope; b + d the post-break slope; d the change. The unrestricted model searches all admissible years for the strongest slope change; a moving-block bootstrap describes how stable that date is under serially dependent noise.", size=13.5, color=GRAY, space_after=10)
para(tf, "A breakpoint identifies when a trend changed — with uncertainty. It is not a peak year, not a policy-adoption date, and never a causal estimate by itself. Historical and external evidence answers why.", size=13.5, color=INK, space_after=10)
para(tf, "Inference: Newey–West standard errors for fixed-date tests; BIC for model evidence; moving-block bootstrap for date stability.", size=13.5, color=GRAY, space_after=0)
tf = box(s, 7.0, 1.6, 5.8, 5.4)
para(tf, "The Kaya decomposition", size=16, bold=True, first=True, space_after=6)
para(tf, "C/GDP = (C/E) × (E/GDP)", size=15, font="Consolas", space_after=8)
runs(tf, [("C/GDP — ", BLUE, True), ("aggregate carbon intensity of output: the observed outcome.", GRAY, False)], size=13.5, space_after=6)
runs(tf, [("C/E — ", GREEN, True), ("supply side: fuel mix, electricity systems, conversion technology.", GRAY, False)], size=13.5, space_after=6)
runs(tf, [("E/GDP — ", AMBER, True), ("demand side: efficiency, sectoral structure, economic composition.", GRAY, False)], size=13.5, space_after=10)
para(tf, "We estimate all three, for the world aggregate and every country, with one harmonized procedure. The component pattern constrains which mechanisms are plausible.", size=13.5, color=INK, space_after=0)
notes(s, "One methods slide on the estimator, one on the sample. Emphasize: 'when, not why' — the design lock's central discipline.")

# ---------------------------------------------------------------- 4 · methods 2 (evidence base)
s = slide()
kicker_title(s, "METHODS", "From 204 jurisdictions to 97 eligible national breaks", kcolor=BLUE)
tf = box(s, 0.55, 1.5, 5.4, 5.6)
para(tf, "Eligibility is strict by design", size=16, bold=True, first=True, space_after=6)
for t in ["at least 40 annual observations, 10+ years on each side of the break, break 10+ years from the boundary",
          "BIC improvement of at least 6 over the unbroken trend",
          "70%+ of bootstrap dates within 5 years; interval no wider than 12 years",
          "standardized slope change of at least 0.25"]:
    runs(tf, [("•  ", GREEN, True), (t, GRAY, False)], size=13, space_after=5)
para(tf, "204 jurisdictions → 158 estimable → 97 countries with an eligible, stable headline break; nearby component breaks consolidate into 107 transition episodes (15-year grouping; 10/20-year sensitivity).", size=13, color=INK, space_after=8)
para(tf, "Treaty attribution ladder (all five required): Newey–West significance → top 10% vs nearby placebo dates → best date within 3 years of the treaty → compatible unrestricted break → plausible domestic mechanism.", size=13, color=INK, bold=True, space_after=0)
fit_image(s, M("image1.png"), 6.15, 1.5, 6.85, 5.6)
notes(s, "The funnel figure is from the current deck. The five-step ladder is the frozen attribution standard — it returns in Act I applied to Paris itself.")

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
notes(s, "Act I is reframed relative to earlier drafts: not 'treaties failed' but 'the record shows a real recent acceleration whose timing cannot yet separate Paris from the renewables cost decline.'")

# ---------------------------------------------------------------- 6 · Act I fig 1
figure_slide("ACT I · IS THE GLOBAL BEND PARIS?",
             "Global curves first bent in the 1970s — decades before the climate regime",
             F("takeaway_fig01_global_bend_predates_treaties.png"),
             note="C/GDP breaks ~1973, E/GDP ~1974 — the oil-shock era. C/E's point estimate is 1992 but its interval spans 1978–2011: it does not uniquely identify Rio. Multiple-break models show several episodes, not one intervention. Robust to consumption-based emissions, excluding former Soviet economies, PPP GDP.")

# ---------------------------------------------------------------- 7 · Act I fig 2A
figure_slide("ACT I · IS THE GLOBAL BEND PARIS?",
             "Paris at ten: intensity is outrunning its old trend — but the bend began earlier",
             F("takeaway_fig02a_paris_and_the_long_trend.png"),
             note="The post-2015 points fall below the extrapolated Rio-to-Paris trend: a real supply-side acceleration (C/E −0.7 pp/yr, NW t=4.3; C/GDP −0.9, t=2.9). But onsets from 2011–2016 fit the full record about equally well (best 2013), and E/GDP shows no acceleration. So the acceleration is what an effective Paris should look like — and it cannot yet be separated from the renewables cost collapse that preceded the treaty.")

# ---------------------------------------------------------------- 8 · Act I fig 2B
figure_slide("ACT I · IS THE GLOBAL BEND PARIS?",
             "The arithmetic of bending the curve: intensity must fall as fast as GDP grows",
             F("takeaway_fig02b_stabilization_arithmetic.png"),
             note="Kaya growth accounting by era. Emissions growth slowed from +2.1 to +0.4%/yr after 2015 — but roughly two-thirds of the slowdown is slower GDP growth; one-third is the cleaner fuel mix. The dotted line marks the intensity decline needed to hold emissions flat: the world is still short of it.")

# ---------------------------------------------------------------- 9 · Act I placebo
figure_slide("ACT I · IS THE GLOBAL BEND PARIS?",
             "The placebo discipline: many years look like turning points",
             F("takeaway_fig02_placebo_test.png"),
             note="Top: the model-fit profile across candidate break years is a plateau — why a significant treaty-year hinge is weak evidence alone. Bottom: the evidentiary funnel. Nominal treaty-date significance is common (48–69% of series); date-uniqueness is rare (Rio: 10 C/GDP, 21 C/E, 34 E/GDP series; Paris: 14, 5, 6). Applied to Paris's own decade, the same discipline dates the global acceleration's onset to ~2013.")

# ---------------------------------------------------------------- 10 · Act I verdict
s = slide()
kicker_title(s, "ACT I · VERDICT", "The global record can show an acceleration — not yet its author")
tf = box(s, 0.55, 1.6, 6.05, 5.4)
para(tf, "What the data establishes", size=16, bold=True, color=GREEN, first=True, space_after=6)
for t in ["A real post-2013 supply-side acceleration: C/E falling −0.5%/yr after a flat quarter-century; C/GDP −0.9 pp/yr faster than the Rio-to-Paris trend (Newey–West).",
          "Emissions growth slowed from +2.1 to +0.4%/yr — the direction an effective Paris requires.",
          "No acceleration on the demand side (E/GDP): efficiency and structure continue their 50-year trend."]:
    runs(tf, [("•  ", GREEN, True), (t, GRAY, False)], size=13.5, space_after=7)
tf = box(s, 7.0, 1.6, 5.8, 5.4)
para(tf, "Why attribution stays open", size=16, bold=True, color=RED, first=True, space_after=6)
for t in ["Timing: candidate onsets 2011–2016 fit about equally well (best 2013) — indistinguishable from the renewables cost collapse that preceded Paris.",
          "Power: with 8 post-Paris years, only an acceleration ≈0.8 pp/yr is detectable at 80% power — Paris would have had to double a 50-year trend to prove itself already.",
          "Aggregation: China's WTO-era coal boom flattened the global fuel-mix baseline; the world series is a China-weighted average that hides national signals.",
          "Design: Paris works through NDCs and national transformation — its signature should appear country by country. So we look there."]:
    runs(tf, [("•  ", RED, True), (t, GRAY, False)], size=13.5, space_after=7)
notes(s, "This is the hinge of the talk: the non-attribution is not a failure of Paris — it is the reason the analysis must descend to the national level, where attribution machinery actually has power.")

# ---------------------------------------------------------------- 11 · Act II timeline
figure_slide("ACT II · WHAT BENDS NATIONAL CURVES?",
             "97 national breaks across five decades — tracking economic history",
             F("takeaway_fig03_when_and_why_curves_bend.png"),
             note="No common treaty era: breaks scatter 1970–2013 and pile up around oil shocks, post-Cold-War upheaval, crises, and the renewables era. Bottom: among 71 documented episodes, events sit near the estimated breaks far more often than restricted random dates allow (45% vs 17% within 2 years; 80% vs 37% within 5; 70% vs 33% inside the episode) — the historical classifications carry real temporal information.")

# ---------------------------------------------------------------- 12 · Act II census
figure_slide("ACT II · WHAT BENDS NATIONAL CURVES?",
             "What accompanied the bends: mostly markets, restructuring, disruption",
             F("takeaway_fig04_mechanism_census.png"),
             note="One square per country. Fuel and energy markets 22, restructuring 18, political disruption 11, macro shocks 9, development and access 6 — and climate policy with low-carbon technology in 9 of 97. 22 remain honestly unresolved. Mechanisms are structured author-coded interpretations against documentary sources — not causal estimates.")

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
para(tf, "favorable? persistent? absolute CO2 falling? constructive mechanism?", size=12.5, italic=True, color=GRAY, space_after=8)
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
             "From mechanism to verdict: 97 countries flow to six outcomes",
             M("image4.png"),
             note="Shocks flow into contraction; restructuring often ends in 'intensity gain, CO2 rising'. Only nine countries end in constructive persistent decarbonization. The gray band on the left axis is the distinct 22 with no attributed mechanism.")

# ---------------------------------------------------------------- 15 · quadrant
figure_slide("ACT III · DID THE BENDS COUNT?",
             "Lower carbon intensity is not the same as falling emissions",
             F("takeaway_fig05_bend_vs_success.png"),
             note="Raw quadrant counts: 55 favorable bends coincide with still-rising CO2; only 19 with falling CO2. The stricter quality classification — adding persistence and mechanism — narrows these to 12 improving-but-rising and 9 constructive. Green triangles are the 9 policy-enabled cases: Bhutan and Paraguay improve intensity while absolute emissions still rise — policy-enabled and constructive overlap but are not identical.")

# ---------------------------------------------------------------- 16 · the nine
figure_slide("ACT III · DID THE BENDS COUNT?",
             "The nine constructive persistent decarbonizations",
             M("image7.png"),
             takeaway="Sweden 1986 · Finland 1993 · Hungary 1996 · Switzerland 1999 · Nauru 1999 · Denmark 2002 · Portugal 2004 · United Kingdom 2010 · Ireland 2012",
             note="The defining test: intensity AND absolute CO2 both fall after the break. Six of nine are policy-enabled; Hungary, Nauru, and Ireland arrived via restructuring. Caveat: Nauru is a micro-state whose 'restructuring' is the phosphate collapse — treat with care. This is the paper's constructive core: policy made physical in fuel mix, infrastructure, and economic structure.")

# ---------------------------------------------------------------- 17 · nineteen cutters
figure_slide("ACT III · DID THE BENDS COUNT?",
             "Nineteen countries cut emissions — ten don't earn the verdict",
             M("image8.png"),
             note="Three routes around the constructive verdict: fuel substitution (5), evidence limits (4), collapse (1). Netherlands 1975 is gas-substitution decarbonization forty years before the US shale version. Somalia 1985 is the caution: collapse mimics decarbonization in every raw statistic; only the persistence screen catches it. Even genuine emission-cutters span 1975–2012 — no treaty era here either.")

# ---------------------------------------------------------------- 18 · geography
s = slide()
kicker_title(s, "ACT III · THE GEOGRAPHY", "Mechanisms are regional stories; success concentrates where policy changed physical systems", kcolor=AMBER)
fit_image(s, M("image9.png"), 0.30, 1.55, 6.35, 5.5)
fit_image(s, M("image10.png"), 6.75, 1.55, 6.35, 5.5)
notes(s, "Left: primary mechanism by country — fuel-market transformations cluster in the Americas and MENA, restructuring across Asia-Pacific, policy-enabled cases in northern Europe. Right: transition quality — dark-green outlines mark the nine; much of the map is contraction, incompleteness, or intensity gains overwhelmed by growth.")

# ---------------------------------------------------------------- 19 · Act IV ratings
figure_slide("ACT IV · CAN WE TRUST THE STORY?",
             "Independent raters recognize the same countries — on thin coverage",
             F("takeaway_fig06_external_corroboration.png"),
             note="Policy-enabled cases rank high on independent assessments: median CAT percentile ~64 vs 34 for other classified breaks; CCPI ~91 vs 44. But CAT covers only 3 of the 9 and CCPI 2 — every covered country is shown as a dot so the thin coverage is visible. Corroborative, not definitive.")

# ---------------------------------------------------------------- 20 · robustness & limits
s = slide()
kicker_title(s, "ACT IV · CAN WE TRUST THE STORY?", "Robustness, corroboration, and honest limits", kcolor=RED)
col = [("Consumption-based accounting",
        "Of 17 countries eligible under both accountings, only 6 agree within 5 years; the median gap is ~12 years. Some 'domestic' transitions partly reflect trade and offshoring — a main result, not a footnote. (Consumption series begin in 1990, so very early production breaks cannot be matched by construction.)"),
       ("Carbon pricing & policy stringency",
        "Pricing is negatively associated with C/E in country-and-year fixed-effects models (contemporaneous strongest); C/GDP and E/GDP estimates are imprecise. OECD EPS covers only 15 of 28 focal countries. Associational, not causal."),
       ("Event-timing validation",
        "45% of documented events within 2 years of the break vs ~17% by chance; 80% within 5 vs 37%; 70% inside the episode vs 33% — far beyond retrospective storytelling."),
       ("What breakpoints can't tell you",
        "Break timing identifies change, not cause. Attribution and outcome classification each leave 22 cases open — restraint that makes the resolved 75% credible. No counterfactual: a treaty that prevents backsliding produces no break at all.")]
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
             note="97 eligible breaks classified by realized transition quality — and none of this heterogeneity aligns on a treaty date. The treaty question dissolves into 97 national stories; nine end in unambiguous decarbonization.")

# ---------------------------------------------------------------- 22 · close
s = slide()
tf = box(s, 0.9, 1.15, 11.5, 1.8)
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
notes(s, "End on the closing line and the four-part method signature. If one sentence survives the talk, it is this one.")

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
