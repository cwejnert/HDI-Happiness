#!/usr/bin/env python3
"""Paris at Ten — v3. Rebuilt on a true world aggregate and a 44-specification grid."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image
import os

FIGS = "/home/user/HDI-Happiness/carbon_breakpoints_takeaway_figures/outputs/final_master/figures_world_v3"
OUT = "/home/user/HDI-Happiness/carbon_breakpoints_takeaway_figures/paris_at_ten_world_deck.pptx"

INK = RGBColor(0x21, 0x21, 0x21); GRAY = RGBColor(0x55, 0x55, 0x55); LGRAY = RGBColor(0x8A, 0x8A, 0x8A)
GREEN = RGBColor(0x1B, 0x78, 0x37); BLUE = RGBColor(0x3A, 0x66, 0xA5)
RED = RGBColor(0xB3, 0x3A, 0x3A); AMBER = RGBColor(0xC7, 0x7F, 0x00)

prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
slide = lambda: prs.slides.add_slide(BLANK)


def box(s, x, y, w, h):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.text_frame.word_wrap = True
    return tb.text_frame


def para(tf, text, size=14, color=INK, bold=False, italic=False, first=False,
         space_after=6, align=PP_ALIGN.LEFT):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align; p.space_after = Pt(space_after)
    r = p.add_run(); r.text = text
    r.font.size, r.font.bold, r.font.italic, r.font.name = Pt(size), bold, italic, "Calibri"
    r.font.color.rgb = color
    return p


def runs(tf, parts, size=14, first=False, space_after=6, italic=False):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.space_after = Pt(space_after)
    for t, c, b in parts:
        r = p.add_run(); r.text = t
        r.font.size, r.font.bold, r.font.name = Pt(size), b, "Calibri"
        r.font.italic = italic; r.font.color.rgb = c
    return p


def kicker_title(s, kicker, title, kcolor=GREEN):
    tf = box(s, 0.55, 0.3, 12.25, 1.0)
    para(tf, kicker, size=12, color=kcolor, bold=True, first=True, space_after=2)
    para(tf, title, size=24, color=INK, bold=True, space_after=0)


def fit_image(s, path, x, y, maxw, maxh):
    iw, ih = Image.open(path).size
    sc = min(maxw / iw, maxh / ih); w, h = iw * sc, ih * sc
    return s.shapes.add_picture(path, Inches(x + (maxw - w) / 2), Inches(y + (maxh - h) / 2), Inches(w), Inches(h))


def notes(s, t):
    s.notes_slide.notes_text_frame.text = t


def finding(kicker, title, takeaway, img, caveat=None, note="", kcolor=GREEN):
    s = slide(); kicker_title(s, kicker, title, kcolor=kcolor)
    tf = box(s, 0.55, 1.30, 12.25, 0.5)
    runs(tf, [("Takeaway:  ", kcolor, True), (takeaway, INK, True)], size=14, first=True, space_after=0)
    top = 1.86
    if caveat:
        tf = box(s, 0.55, top, 12.25, 0.42)
        runs(tf, [("But:  ", RED, True), (caveat, GRAY, False)], size=12, first=True, space_after=0)
        top += 0.46
    fit_image(s, img, 0.35, top, 12.63, 7.2 - top)
    notes(s, note); return s


F = lambda n: os.path.join(FIGS, n)

# 1 · title
s = slide()
tf = box(s, 0.9, 1.7, 11.5, 3.6)
para(tf, "Paris at Ten", size=46, bold=True, first=True, space_after=8)
para(tf, "The world's carbon intensity is falling faster than ever. We ask whether the record can credit the Paris Agreement — and find that it cannot, for a specific and instructive reason.",
     size=18, color=GRAY, space_after=14)
runs(tf, [("True world aggregate, 1965-2023 · 44 specifications · unknown-break-date tests", GREEN, True)], size=14)
notes(s, "World-level paper. The country analysis is the follow-on. Every number here is from the true world aggregate unless stated; the specification grid is the robustness spine.")

# 2 · the question
s = slide()
kicker_title(s, "THE QUESTION", "Something changed. Was it Paris?")
tf = box(s, 0.55, 1.6, 7.4, 5.4)
para(tf, "The good news is real. Global CO2 growth fell from +2.1% a year over the Rio-to-Paris quarter century to +0.7% a year since, and carbon intensity is now improving at -2.1% a year: the fastest sustained rate in the observed record.",
     size=15, color=GRAY, first=True, space_after=14)
para(tf, "But the obvious reading — that the agreement did it — is the reading the data is worst at supporting. Carbon intensity has been falling for fifty years, in episodes with their own causes. Clean-energy costs collapsed on almost the same schedule as the treaty. And emissions growth slows when the economy slows.",
     size=15, color=GRAY, space_after=14)
para(tf, "So we ask a narrow question: when did the trend actually turn, and is 2015 a special year in the record — or a year that happens to sit near one?",
     size=15, color=INK, bold=True, space_after=0)
tf = box(s, 8.35, 1.6, 4.45, 5.4)
para(tf, "Why we look at intensity", size=15, bold=True, color=GREEN, first=True, space_after=6)
para(tf, "Emissions have three moving parts:", size=13.5, color=GRAY, space_after=6)
para(tf, "economic growth  +  fuel mix  +  energy efficiency", size=13.5, color=INK, bold=True, space_after=8)
para(tf, "Growth pushes emissions up; the fuel mix and efficiency are the only two things that push them down. A policy effect has to show up in one of them before it can show up in emissions at all.",
     size=13.5, color=GRAY, space_after=0)
notes(s, "Sympathetic frame, then the decomposition that structures everything.")

# 3 · what we did
s = slide()
kicker_title(s, "WHAT WE DID", "Four steps", kcolor=BLUE)
steps = [("1", "Use a true world series",
          "Not a sum over whichever countries reported. The published world totals for CO2 and energy, 1965-2023, with World Bank world GDP. No composition drift, no interpolation, eight post-Paris years."),
         ("2", "Let the data pick the turn",
          "Fit two straight lines meeting at a kink, try every possible kink year, keep the best. Then a formal unknown-break-date test with bootstrapped critical values, so searching over years does not manufacture significance."),
         ("3", "Ask if the treaty year is special",
          "A curving trend makes almost any year look significant. We rank 2015 against every other candidate year — a treaty earns credit only if its year beats its neighbours."),
         ("4", "Re-run everything 44 ways",
          "World aggregate or country panel, four start years, three endpoints, four completeness thresholds, with and without interpolation. We report only what survives.")]
x = 0.55
for n, t, d in steps:
    tf = box(s, x, 1.7, 3.0, 5.0)
    para(tf, n, size=32, bold=True, color=BLUE, first=True, space_after=6)
    para(tf, t, size=14.5, bold=True, space_after=8)
    para(tf, d, size=12, color=GRAY, space_after=0)
    x += 3.13
tf = box(s, 0.55, 6.7, 12.25, 0.6)
runs(tf, [("A turning point tells us when a trend changed — never, by itself, why. ", INK, True),
          ("That is the whole method.", GRAY, False)], size=13.5, first=True)
notes(s, "Step 4 is the addition that matters: it caught an earlier overclaim of ours, which is exactly what it is for.")

# 4 · finding 1
finding("WHAT WE FIND · 1 OF 4", "The decisive turn in the record is the 1970s — not a treaty",
        "The oil shocks remain the largest structural break in the world's carbon intensity, and the current fast episode began in 2012.",
        F("v3_fig1_long_record.png"),
        note="Unknown-break test: dominant break 1972 for carbon intensity (p = 0.002) and 1974 for efficiency (p < 0.001); the fuel mix has no statistically significant single break at all (p = 0.14). BIC selects three breaks: 1973, 2001, 2012. Note this reproduces the frozen 1973 result on an independently built series.")

# 5 · finding 2
finding("WHAT WE FIND · 2 OF 4", "Efficiency never changed pace. The fuel mix stalled, then resumed.",
        "Energy efficiency has improved at about 1% a year for fifty years. The whole story is the fuel mix, which stalled completely from Rio to Paris.",
        F("v3_fig2_baseline_problem.png"),
        caveat="this is why the size of the 'Paris effect' depends on the baseline: against the 2000s stall it looks dramatic, against the post-1973 record it is a resumption.",
        note="Fuel mix: -0.52%/yr after the oil shocks, +0.02 from Rio to Paris, -0.70 since. Efficiency: -0.95, -1.02, -1.08. The 1990-2015 fuel-mix stall is the anomaly, not the recent improvement.")

# 6 · finding 3
finding("WHAT WE FIND · 3 OF 4", "However we build the series, the turn comes before Paris",
        "In roughly nine specifications out of ten, the best-fitting turning point lands before 2015 — usually 2011 to 2013.",
        F("v3_fig3_specification_invariance.png"),
        note="89% of specifications for overall intensity, 93% for the fuel mix, 64% for efficiency. This is the single most robust finding in the paper and it does not depend on any construction choice.",
        kcolor=AMBER)

# 7 · finding 4
finding("WHAT WE FIND · 4 OF 4", "The timing result is robust. The rest is not.",
        "Whether the post-2015 change is statistically significant depends on the component and on how the series is built — for efficiency, only 41% of specifications agree.",
        F("v3_fig4_what_is_robust.png"),
        caveat="and Paris does not cleanly beat its neighbouring years: on the true world aggregate it ranks 80th percentile for overall intensity but only 11th for the fuel mix.",
        note="This corrects an earlier draft that reported Paris at the 97th percentile — that figure came from one constructed panel and does not survive the grid. Neither treaty year robustly outperforms its neighbours.",
        kcolor=AMBER)

# 8 · verdict
s = slide()
kicker_title(s, "WHAT IT ADDS UP TO", "A real acceleration that began before the treaty")
tf = box(s, 0.55, 1.6, 6.05, 5.4)
para(tf, "What we can say", size=15, bold=True, color=GREEN, first=True, space_after=6)
para(tf, "The world is decarbonizing faster than at any point in the record: carbon intensity has fallen at 2.1% a year since 2012, against 0.4% in the decade before. That improvement is real, it is large, and it is concentrated in the fuel mix — exactly where clean technology and energy policy operate.",
     size=13.5, color=GRAY, space_after=0)
tf = box(s, 7.0, 1.6, 5.8, 5.4)
para(tf, "What we cannot", size=15, bold=True, color=RED, first=True, space_after=6)
para(tf, "The turn is dated to 2012 in almost every specification — three years before the agreement. Energy efficiency did not respond at all. The fuel-mix improvement is a return to its pre-1990 pace rather than something new. And the timing coincides exactly with the collapse in clean-energy costs.",
     size=13.5, color=GRAY, space_after=10)
para(tf, "The acceleration is real. It started before Paris, and it looks like what cheap clean energy would produce.",
     size=13.5, color=INK, bold=True, space_after=0)
notes(s, "The honest verdict. Neither vindication nor indictment — a dating result that happens to be inconvenient for attribution.")

# 9 · what would settle it
s = slide()
kicker_title(s, "WHAT WOULD SETTLE IT", "Three things — and two are not at the world level")
tf = box(s, 0.55, 1.65, 11.9, 5.0)
para(tf, "Persistence. A 2012 turn driven by a one-off technology shock should decay as the cheap-solar transition matures. One that reflects policy ratcheting should not. Another decade of data distinguishes them; the size of the change is already detectable, so this is about durability rather than power.",
     size=15, color=GRAY, first=True, space_after=12)
para(tf, "The demand side. Efficiency is the informative half precisely because it has not moved. Cheap solar explains a cleaner fuel mix; it does not explain how much energy the world uses per unit of output. If efficiency accelerates, technology alone stops being a sufficient explanation.",
     size=15, color=GRAY, space_after=12)
para(tf, "Disaggregation. Paris works through national pledges, so its signature should appear country by country — where series are independent, placebo tests are genuinely separate, and a documentary record exists for what accompanied each turn. That is the companion paper.",
     size=15, color=GRAY, space_after=14)
para(tf, "The question we would put to the field: should treaty assessment be built on intensity turning points and placebo discipline, rather than on emissions levels and anniversaries?",
     size=15, color=INK, bold=True, space_after=0)
notes(s, "Forward-looking, and hands off to the national paper.")

# 10 · limits
s = slide()
kicker_title(s, "LIMITS", "What we are not claiming", kcolor=RED)
col = [("This is not causal",
        "A turning point identifies when a trend changed, never why. Even a perfect fit at 2015 would be a coincidence of timing. And an agreement that prevented backsliding would leave no turning point at all — absence of one is not absence of an effect."),
       ("Two GDP concepts",
        "Overall intensity and efficiency use World Bank world GDP in constant 2015 dollars; the country panels use purchasing-power GDP. The fuel-mix result — the one most relevant to policy — uses a single source and no GDP at all."),
       ("Eight post-Paris years",
        "The series ends in 2023 for CO2 and energy and 2022 for GDP. Country-level work stops in 2021 because GDP reporting, not emissions reporting, runs out. Adding partial years would overstate the recent trend."),
       ("Production-based accounting",
        "Emissions are counted where they are produced. At the world level that is the right frame, since global production equals global consumption — but it matters for the national work that follows.")]
xs, ys = [0.55, 7.0, 0.55, 7.0], [1.6, 1.6, 4.35, 4.35]
for (t, d), x, y in zip(col, xs, ys):
    tf = box(s, x, y, 5.9, 2.6)
    para(tf, t, size=14.5, bold=True, first=True, space_after=4)
    para(tf, d, size=12, color=GRAY, space_after=0)
notes(s, "Volunteer the GDP-concept issue; a referee will find it.")

# 11 · close
s = slide()
tf = box(s, 0.9, 1.6, 11.5, 2.0)
para(tf, "The curve is bending faster than ever.", size=28, bold=True, first=True, space_after=2)
para(tf, "It started bending in 2012.", size=28, bold=True, color=GREEN, space_after=0)
tf = box(s, 0.9, 3.7, 11.5, 2.9)
for t in ["The largest break in the world's carbon-intensity record is still the 1970s oil shocks.",
          "The current fast episode begins in 2012 — in nine specifications out of ten, before Paris.",
          "Energy efficiency has improved at about 1% a year for fifty years and did not respond to the treaty era.",
          "The fuel mix stalled from Rio to Paris and has since resumed — which is what cheap clean energy would produce."]:
    runs(tf, [("—  ", GREEN, True), (t, GRAY, False)], size=15, space_after=10)
tf = box(s, 0.9, 6.6, 11.5, 0.7)
para(tf, "Turning points say when · the Kaya split says through which door · placebo tests say whether the date is special · the specification grid says whether any of it holds",
     size=12.5, italic=True, color=LGRAY, first=True, align=PP_ALIGN.CENTER)
notes(s, "Close on the dating result, which is the robust one.")

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
