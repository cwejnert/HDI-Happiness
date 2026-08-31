"""
Render content.py as a single self-contained HTML page.

Figures are base64-embedded so the page survives on its own (and so a
re-published artifact doesn't depend on this container still existing).

    python build_artifact.py [out.html]

Default output: deck/education_exception.html
"""
from __future__ import annotations

import base64
import sys
from pathlib import Path

import content as C

HERE = Path(__file__).parent
FIGDIR = HERE / "figures"


def embed(name: str) -> str:
    data = base64.b64encode((FIGDIR / name).read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


def plate(name: str, caption: str, feature: bool = False) -> str:
    cls = "plate plate--feature" if feature else "plate"
    return f"""
      <figure class="{cls}">
        <div class="plate__stock"><img src="{embed(name)}" alt="{caption}"></div>
        <figcaption>{caption}</figcaption>
      </figure>"""


def render_beat(beat: dict) -> str:
    paras = "\n".join(f"          <p>{p}</p>" for p in beat["body"])
    fig = plate(beat["figure"], beat["caption"], beat.get("feature", False)) if beat.get("figure") else ""
    return f"""
      <section class="beat">
        <p class="beat__label">{beat['label']}</p>
        <h3 class="beat__heading">{beat['heading']}</h3>
        <div class="prose">
{paras}
        </div>{fig}
      </section>"""


def render_act(act: dict, index: int) -> str:
    nums = "\n".join(
        f'          <div class="keynum"><span class="keynum__v">{v}</span>'
        f'<span class="keynum__k">{k}</span></div>'
        for v, k in act["key_numbers"]
    )
    beats = "\n".join(render_beat(b) for b in act["beats"])
    return f"""
    <article class="act" id="act-{index}">
      <header class="act__open">
        <span class="act__numeral" aria-hidden="true">{act['numeral']}</span>
        <div class="act__head">
          <p class="act__eyebrow">Act {act['numeral']}</p>
          <h2 class="act__title">{act['title']}</h2>
          <p class="act__thesis">{act['thesis']}</p>
        </div>
      </header>
      <div class="keynums">
{nums}
      </div>
{beats}
      <aside class="act__close">
        <p class="act__close-label">Where Act {act['numeral']} leaves us</p>
        <p>{act['close']}</p>
      </aside>
    </article>"""


def render() -> str:
    toc = "\n".join(
        f"""        <li>
          <a href="#act-{i}">
            <span class="toc__num">{n}</span>
            <span class="toc__body"><strong>{claim}</strong><span>{gloss}</span></span>
          </a>
        </li>"""
        for i, (n, claim, gloss) in enumerate(C.HOOK["acts"], 1)
    )
    hook_paras = "\n".join(f"        <p>{p}</p>" for p in C.HOOK["body"])
    acts = "\n".join(render_act(a, i) for i, a in enumerate(C.ACTS, 1))
    decisions = "\n".join(
        f"""        <div class="decision">
          <h3>{h}</h3>
          <p>{b}</p>
        </div>"""
        for h, b in C.DECISIONS
    )
    appendix = "\n".join(
        f"""        <figure class="ap">
          <div class="plate__stock"><img src="{embed(f)}" alt="{t}"></div>
          <figcaption><strong>{t}</strong>{d}</figcaption>
        </figure>"""
        for f, t, d in C.APPENDIX
    )
    rail = "\n".join(
        f'      <li><a href="#act-{i}"><span>{n}</span></a></li>'
        for i, (n, _, _) in enumerate(C.HOOK["acts"], 1)
    )

    return f"""<title>{C.TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,500;0,600;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root {{
  --ground:      #E8EBEF;
  --surface:     #FCFCFB;
  --ink:         #14171C;
  --ink-soft:    #5A6068;
  --ink-faint:   #868D96;
  --rule:        #CDD3DB;
  --rule-soft:   #DDE1E7;
  --accent:      #17549E;
  --accent-wash: #DDE6F3;
  --flag:        #A63A30;
  --shadow:      0 1px 2px rgba(20,23,28,.06), 0 8px 24px -12px rgba(20,23,28,.18);
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground:      #0F1216;
    --surface:     #171B21;
    --ink:         #E6EAEF;
    --ink-soft:    #949CA6;
    --ink-faint:   #737B85;
    --rule:        #29303A;
    --rule-soft:   #212831;
    --accent:      #7FB2F2;
    --accent-wash: #1B2836;
    --flag:        #DE7A6E;
    --shadow:      0 1px 2px rgba(0,0,0,.4), 0 10px 28px -14px rgba(0,0,0,.7);
  }}
}}
:root[data-theme="dark"] {{
  --ground:      #0F1216;
  --surface:     #171B21;
  --ink:         #E6EAEF;
  --ink-soft:    #949CA6;
  --ink-faint:   #737B85;
  --rule:        #29303A;
  --rule-soft:   #212831;
  --accent:      #7FB2F2;
  --accent-wash: #1B2836;
  --flag:        #DE7A6E;
  --shadow:      0 1px 2px rgba(0,0,0,.4), 0 10px 28px -14px rgba(0,0,0,.7);
}}

* {{ box-sizing: border-box; }}

body {{
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font-family: "IBM Plex Sans", ui-sans-serif, system-ui, -apple-system, sans-serif;
  font-size: 16px;
  line-height: 1.62;
  -webkit-font-smoothing: antialiased;
}}

.wrap {{
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 clamp(1.25rem, 4vw, 3rem);
}}
.col {{ max-width: 40rem; }}

/* ---------- masthead ---------- */
.mast {{
  border-bottom: 1px solid var(--rule);
  padding: clamp(3.5rem, 9vw, 7rem) 0 clamp(2rem, 5vw, 3.25rem);
}}
.mast__rule {{
  display: flex; align-items: center; gap: .75rem;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: .688rem; letter-spacing: .16em; text-transform: uppercase;
  color: var(--accent); margin: 0 0 1.75rem;
}}
.mast__rule::after {{
  content: ""; flex: 1; height: 1px; background: var(--rule);
}}
.mast h1 {{
  font-family: Newsreader, Georgia, "Times New Roman", serif;
  font-weight: 500;
  font-size: clamp(2.75rem, 8vw, 5.25rem);
  line-height: 1.02;
  letter-spacing: -0.022em;
  text-wrap: balance;
  margin: 0 0 1.25rem;
  max-width: 16ch;
}}
.mast__sub {{
  font-family: Newsreader, Georgia, serif;
  font-style: italic;
  font-size: clamp(1.125rem, 2.3vw, 1.4rem);
  line-height: 1.45;
  color: var(--ink-soft);
  max-width: 46rem;
  margin: 0 0 2.25rem;
}}
.mast__meta {{
  display: flex; flex-wrap: wrap; gap: .5rem 1.5rem;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: .75rem; line-height: 1.6; color: var(--ink-faint);
}}
.mast__meta span:first-child {{ color: var(--ink-soft); }}

/* ---------- hook ---------- */
.hook {{ padding: clamp(2.5rem, 6vw, 4.5rem) 0 0; }}
.kicker {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: .688rem; letter-spacing: .16em; text-transform: uppercase;
  color: var(--ink-faint); margin: 0 0 1rem;
}}
.hook h2 {{
  font-family: Newsreader, Georgia, serif;
  font-weight: 500; font-size: clamp(1.75rem, 4vw, 2.6rem);
  line-height: 1.18; letter-spacing: -0.014em; text-wrap: balance;
  margin: 0 0 1.5rem; max-width: 24ch;
}}
.prose p {{ margin: 0 0 1.05em; }}
.prose p:last-child {{ margin-bottom: 0; }}

/* ---------- table of acts ---------- */
.toc {{
  list-style: none; margin: clamp(2.5rem, 5vw, 3.5rem) 0 0; padding: 0;
  border-top: 1px solid var(--rule);
}}
.toc li {{ border-bottom: 1px solid var(--rule-soft); }}
.toc a {{
  display: flex; gap: clamp(1rem, 3vw, 2.25rem); align-items: baseline;
  padding: 1.1rem .25rem; text-decoration: none; color: inherit;
  transition: background .16s ease, padding-left .16s ease;
}}
.toc a:hover, .toc a:focus-visible {{
  background: var(--accent-wash); padding-left: .75rem;
}}
.toc a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: -2px; }}
.toc__num {{
  font-family: Newsreader, Georgia, serif;
  font-size: 1.4rem; color: var(--accent); min-width: 2.25rem;
  font-variant-numeric: tabular-nums;
}}
.toc__body {{ display: flex; flex-direction: column; gap: .15rem; }}
.toc__body strong {{ font-weight: 600; font-size: 1.02rem; }}
.toc__body span {{ color: var(--ink-soft); font-size: .9rem; line-height: 1.5; }}

/* ---------- act openers ---------- */
.act {{ padding-top: clamp(4rem, 10vw, 8rem); }}
.act__open {{
  position: relative;
  border-top: 2px solid var(--ink);
  padding-top: 1.5rem;
  margin-bottom: 2rem;
}}
.act__numeral {{
  position: absolute;
  right: 0; top: .35rem;
  font-family: Newsreader, Georgia, serif;
  font-size: clamp(6rem, 17vw, 13rem);
  line-height: .78;
  font-weight: 400;
  color: var(--accent);
  opacity: .13;
  pointer-events: none;
  user-select: none;
}}
.act__head {{ position: relative; max-width: 42rem; }}
.act__eyebrow {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: .688rem; letter-spacing: .18em; text-transform: uppercase;
  color: var(--accent); margin: 0 0 .85rem;
}}
.act__title {{
  font-family: Newsreader, Georgia, serif;
  font-weight: 500; font-size: clamp(2rem, 5vw, 3.15rem);
  line-height: 1.08; letter-spacing: -0.018em; text-wrap: balance;
  margin: 0 0 1rem;
}}
.act__thesis {{
  font-family: Newsreader, Georgia, serif;
  font-style: italic; font-size: clamp(1.05rem, 2.1vw, 1.25rem);
  line-height: 1.5; color: var(--ink-soft); margin: 0; max-width: 38rem;
}}

/* ---------- key numbers ---------- */
.keynums {{
  display: grid; gap: 1px;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
  background: var(--rule);
  border: 1px solid var(--rule);
  margin-bottom: clamp(2.5rem, 5vw, 3.5rem);
}}
.keynum {{
  background: var(--surface);
  padding: 1.1rem 1.25rem;
  display: flex; flex-direction: column; gap: .3rem;
}}
.keynum__v {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 1.35rem; font-weight: 500; letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums; color: var(--ink);
}}
.keynum__k {{ font-size: .8rem; line-height: 1.45; color: var(--ink-soft); }}

/* ---------- beats ---------- */
.beat {{ margin-bottom: clamp(2.75rem, 6vw, 4.25rem); max-width: 40rem; }}
.beat__label {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: .688rem; letter-spacing: .13em; text-transform: uppercase;
  color: var(--ink-faint); margin: 0 0 .6rem;
  padding-left: .85rem; border-left: 2px solid var(--flag);
}}
.beat__heading {{
  font-family: Newsreader, Georgia, serif;
  font-weight: 500; font-size: clamp(1.4rem, 3vw, 1.85rem);
  line-height: 1.22; letter-spacing: -0.01em; text-wrap: balance;
  margin: 0 0 1rem;
}}

/* ---------- figure plates ---------- */
.plate {{ margin: 2rem 0 0; }}
.plate--feature {{ margin-top: 2.5rem; }}
.plate__stock {{
  background: #FCFCFB;
  border: 1px solid var(--rule);
  box-shadow: var(--shadow);
  padding: .5rem;
  overflow-x: auto;
}}
.plate__stock img {{ display: block; width: 100%; height: auto; }}
.plate figcaption, .ap figcaption {{
  font-size: .8rem; line-height: 1.55; color: var(--ink-soft);
  margin-top: .7rem; max-width: 38rem;
}}

/* plates break out of the prose measure on wide screens */
@media (min-width: 62rem) {{
  .plate {{ width: min(56rem, calc(100vw - 6rem)); }}
  .plate--feature {{ width: min(66rem, calc(100vw - 6rem)); }}
}}

/* ---------- act close ---------- */
.act__close {{
  max-width: 42rem;
  border-left: 3px solid var(--accent);
  background: var(--accent-wash);
  padding: 1.4rem 1.6rem;
}}
.act__close-label {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: .688rem; letter-spacing: .14em; text-transform: uppercase;
  color: var(--accent); margin: 0 0 .6rem;
}}
.act__close p:last-child {{
  font-family: Newsreader, Georgia, serif;
  font-size: 1.1rem; line-height: 1.55; margin: 0;
}}

/* ---------- decisions ---------- */
.closing {{
  margin-top: clamp(4.5rem, 10vw, 8rem);
  border-top: 2px solid var(--ink);
  padding-top: 1.75rem;
}}
.closing h2 {{
  font-family: Newsreader, Georgia, serif;
  font-weight: 500; font-size: clamp(1.75rem, 4vw, 2.5rem);
  line-height: 1.12; margin: 0 0 .5rem; letter-spacing: -0.015em;
}}
.closing__note {{ color: var(--ink-soft); max-width: 40rem; margin: 0 0 2.5rem; }}
.decisions {{
  display: grid; gap: 1px;
  grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
  background: var(--rule); border: 1px solid var(--rule);
}}
.decision {{ background: var(--surface); padding: 1.4rem 1.5rem; }}
.decision h3 {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: .7rem; letter-spacing: .14em; text-transform: uppercase;
  color: var(--accent); margin: 0 0 .7rem; font-weight: 500;
}}
.decision p {{ margin: 0; font-size: .92rem; line-height: 1.6; }}

/* ---------- appendix ---------- */
.appendix {{ margin-top: clamp(4.5rem, 10vw, 8rem); padding-bottom: 6rem; }}
.appendix > h2 {{
  font-family: Newsreader, Georgia, serif;
  font-weight: 500; font-size: clamp(1.6rem, 3.5vw, 2.1rem);
  margin: 0 0 .4rem; letter-spacing: -0.012em;
}}
.appendix > p {{ color: var(--ink-soft); max-width: 40rem; margin: 0 0 2.5rem; }}
.ap-grid {{
  display: grid; gap: clamp(2rem, 4vw, 3rem);
  grid-template-columns: repeat(auto-fit, minmax(22rem, 1fr));
}}
.ap {{ margin: 0; }}
.ap figcaption strong {{
  display: block; color: var(--ink); font-weight: 600;
  font-size: .875rem; margin-bottom: .25rem;
}}

/* ---------- act rail ---------- */
.rail {{ display: none; }}
@media (min-width: 82rem) {{
  .rail {{
    display: block; position: fixed; right: 1.75rem; top: 50%;
    transform: translateY(-50%); z-index: 5;
    list-style: none; margin: 0; padding: 0;
  }}
  .rail li + li {{ margin-top: .4rem; }}
  .rail a {{
    display: grid; place-items: center;
    width: 2rem; height: 2rem; text-decoration: none;
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .7rem; color: var(--ink-faint);
    border: 1px solid transparent; border-radius: 2px;
    transition: color .16s ease, border-color .16s ease, background .16s ease;
  }}
  .rail a:hover, .rail a:focus-visible, .rail a.is-current {{
    color: var(--accent); border-color: var(--rule); background: var(--surface);
  }}
  .rail a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
}}

@media (prefers-reduced-motion: reduce) {{
  * {{ transition: none !important; scroll-behavior: auto !important; }}
}}
html {{ scroll-behavior: smooth; }}
</style>

<main class="wrap">

  <header class="mast">
    <p class="mast__rule">Commentary · working draft</p>
    <h1>{C.TITLE}</h1>
    <p class="mast__sub">{C.SUBTITLE}</p>
    <p class="mast__meta"><span>{C.DATELINE}</span><span>{C.SCOPE}</span></p>
  </header>

  <section class="hook">
    <div class="col">
      <p class="kicker">{C.HOOK['kicker']}</p>
      <h2>{C.HOOK['heading']}</h2>
      <div class="prose">
{hook_paras}
      </div>
    </div>
    <ol class="toc">
{toc}
    </ol>
  </section>

{acts}

  <section class="closing">
    <h2>Decisions for the team</h2>
    <p class="closing__note">Five things the acts above do not settle, in the
      order they block drafting.</p>
    <div class="decisions">
{decisions}
    </div>
  </section>

  <section class="appendix">
    <h2>Evidence appendix</h2>
    <p>Everything the four acts rest on but do not carry. In submission these
      become supplementary material.</p>
    <div class="ap-grid">
{appendix}
    </div>
  </section>

</main>

<ul class="rail" aria-label="Acts">
{rail}
</ul>

<script>
(function () {{
  var links = Array.prototype.slice.call(document.querySelectorAll(".rail a"));
  if (!links.length || !("IntersectionObserver" in window)) return;
  var obs = new IntersectionObserver(function (entries) {{
    entries.forEach(function (e) {{
      if (!e.isIntersecting) return;
      links.forEach(function (a) {{
        a.classList.toggle("is-current", a.getAttribute("href") === "#" + e.target.id);
      }});
    }});
  }}, {{ rootMargin: "-45% 0px -50% 0px" }});
  document.querySelectorAll(".act").forEach(function (a) {{ obs.observe(a); }});
}})();
</script>
"""


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "education_exception.html"
    out.write_text(render(), encoding="utf-8")
    print(f"Saved: {out}  ({out.stat().st_size / 1_048_576:.1f} MB)")


if __name__ == "__main__":
    main()
