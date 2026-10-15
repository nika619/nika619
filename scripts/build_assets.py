"""Generate the animated SVGs used in the profile README.

GitHub renders README images through <img>, so every SVG here is fully
self-contained: no scripts, no external fonts or images (thumbnails are
inlined as base64), CSS + SMIL animation only, and a reduced-motion fallback.

    python scripts/build_assets.py
"""

from __future__ import annotations

import base64
from html import escape
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "motion"

INK = "#16130F"
INK2 = "#1F1A15"
LINE = "#2E271F"
AMBER = "#E8A33D"
AMBER_DEEP = "#B97A22"
CREAM = "#F4EDE2"
MUTED = "#B9AE9F"
DIM = "#8C8173"
GREEN = "#7BC47F"

SANS = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Cascadia Code', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
EASE = "0.22 1 0.36 1"  # ease-out-quint for SMIL keySplines
EASE_CSS = "cubic-bezier(.22,1,.36,1)"

REDUCED = """@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; }
}"""


def svg(w: int, h: int, body: str, style: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{title}">\n<title>{title}</title>\n'
        f"<style>\n{style}\n{REDUCED}\n</style>\n{body}\n</svg>\n"
    )


def cover(x: float, y: float, w: float, h: float, begin: float, dur: float,
          fill: str = INK, steps: int | None = None) -> str:
    """A panel painted over text that shrinks to the right, wiping the text in.

    CSS transforms are used instead of SMIL clip animations because they render
    consistently in every browser GitHub users have, including Safari.
    """
    timing = f"steps({steps}, end)" if steps else EASE_CSS
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
        f'style="transform-box: fill-box; transform-origin: right; '
        f'animation: wipe {dur}s {timing} {begin}s forwards"/>'
    )


WIPE = "@keyframes wipe { to { transform: scaleX(0); } }"


# ── Hero ──────────────────────────────────────────────────────────────
def hero() -> str:
    W, H = 1200, 440
    rnd = random.Random(7)
    dots = []
    for i in range(46):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.choice([1, 1, 1.4, 2])
        dur = rnd.uniform(9, 18)
        dx, dy = rnd.uniform(-30, 30), rnd.uniform(-24, 24)
        op = rnd.uniform(0.15, 0.55)
        dots.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{CREAM}" opacity="{op:.2f}" '
            f'style="animation: drift{i % 4} {dur:.1f}s ease-in-out {-rnd.uniform(0, dur):.1f}s infinite alternate; '
            f'--dx:{dx:.0f}px; --dy:{dy:.0f}px"/>'
        )
    # perspective floor grid: horizontal lines slide toward the viewer
    floor = []
    for i in range(8):
        floor.append(
            f'<line x1="0" x2="{W}" y1="360" y2="360" class="hline" style="animation-delay:{-i * 0.5:.1f}s"/>'
        )
    rays = "".join(
        f'<line x1="{600 + k * 40}" y1="300" x2="{600 + k * 260}" y2="{H}" class="ray"/>' for k in range(-6, 7)
    )
    orbit_labels = [("AI", 0), ("3D", 120), ("MOTION", 240)]
    orbit_nodes = "".join(
        f'<g class="spin" style="animation-duration:{22 + i * 6}s; animation-delay:{-a / 360 * (22 + i * 6):.1f}s">'
        f'<circle cx="980" cy="{170 - 70 - i * 26}" r="{6 - i}" fill="{AMBER if i != 1 else CREAM}"/></g>'
        for i, (_, a) in enumerate(orbit_labels)
    )
    body = f"""
<defs>
  <radialGradient id="glow" cx="980" cy="170" r="260" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{AMBER}" stop-opacity=".28"/>
    <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sweep" x1="0" x2="1">
    <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{CREAM}"/>
    <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{INK}"/>
    <stop offset=".5" stop-color="{INK}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g opacity=".55">{rays}{''.join(floor)}</g>
  <rect y="290" width="{W}" height="150" fill="url(#floorfade)"/>
  <circle cx="980" cy="170" r="260" fill="url(#glow)" class="breathe"/>
  {''.join(dots)}

  <g class="orbit-ring">
    <circle cx="980" cy="170" r="70" class="ring"/>
    <circle cx="980" cy="170" r="96" class="ring" style="animation-delay:.15s"/>
    <circle cx="980" cy="170" r="122" class="ring" style="animation-delay:.3s"/>
  </g>
  <circle cx="980" cy="170" r="22" fill="{AMBER}" class="core"/>
  <circle cx="980" cy="170" r="22" fill="none" stroke="{AMBER}" stroke-width="2" class="ping"/>
  {orbit_nodes}

  <text x="64" y="74" class="mono slide">LUCKNOW, INDIA · LOVHACK S2 WINNER · AMPLIFIED NATIONAL FINALIST #6</text>
  <text x="58" y="168" class="name">Mayank Tiwari</text>
  {cover(54, 92, 660, 96, 0.35, 1.1)}
  <rect x="64" y="190" width="560" height="3" rx="1.5" fill="{AMBER}" class="underline"/>
  <rect x="64" y="190" width="120" height="3" fill="url(#sweep)" class="shine"/>
  <text x="64" y="236" class="role">AI full-stack developer &amp; motion designer</text>
  {cover(60, 208, 660, 36, 1.1, 1.2)}
  <text x="64" y="270" class="line">I ship AI products in a weekend, then make them solid enough to sell.</text>
  {cover(60, 248, 800, 32, 1.6, 1.4)}

  <g class="chips">
    <g class="chip" style="animation-delay:2.2s"><rect x="64" y="300" width="132" height="34" rx="17"/><text x="130" y="322">Hire on Contra</text></g>
    <g class="chip" style="animation-delay:2.35s"><rect x="206" y="300" width="112" height="34" rx="17"/><text x="262" y="322">Portfolio ↗</text></g>
    <g class="chip ghost" style="animation-delay:2.5s"><rect x="328" y="300" width="164" height="34" rx="17"/><text x="410" y="322">React · Three.js · Rive</text></g>
  </g>
  <circle cx="928" cy="392" r="6" fill="{GREEN}" class="pulse"/>
  <text x="944" y="397" class="mono avail">AVAILABLE FOR WORK</text>
</g>"""
    style = f"""
.name {{ font: 700 82px {SANS}; fill: {CREAM}; letter-spacing: -1.5px; }}
.role {{ font: 600 28px {SANS}; fill: {AMBER}; }}
.line {{ font: 400 21px {SANS}; fill: {MUTED}; }}
.mono {{ font: 600 14px {MONO}; fill: {DIM}; letter-spacing: 1.6px; }}
.avail {{ fill: {MUTED}; }}
.underline {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: grow-x 1s {EASE_CSS} .9s forwards; }}
@keyframes grow-x {{ to {{ transform: scaleX(1); }} }}
{WIPE}
.slide {{ opacity: 0; animation: slideIn .9s {EASE_CSS} .1s forwards; }}
.hline {{ stroke: {LINE}; stroke-width: 1; animation: floor 4s cubic-bezier(.55,0,1,.45) infinite; transform-origin: 600px 300px; }}
.ray {{ stroke: {LINE}; stroke-width: 1; }}
.ring {{ fill: none; stroke: #3A3128; stroke-width: 1.5; opacity: 0; transform-origin: 980px 170px; animation: ringIn 1.2s {EASE_CSS} .4s forwards; }}
.core {{ transform-origin: 980px 170px; animation: corePop 1s cubic-bezier(.34,1.56,.64,1) .3s both; }}
.ping {{ transform-origin: 980px 170px; animation: ping 2.8s {EASE_CSS} 1.4s infinite; opacity: 0; }}
.spin {{ transform-origin: 980px 170px; animation: spin linear infinite; }}
.breathe {{ transform-origin: 980px 170px; animation: breathe 6s ease-in-out infinite alternate; }}
.shine {{ opacity: 0; animation: shine 3.2s ease-in-out 2.2s infinite; }}
.chip {{ opacity: 0; animation: chipIn .8s cubic-bezier(.34,1.56,.64,1) forwards; transform-box: fill-box; transform-origin: center; }}
.chip rect {{ fill: {AMBER}; }}
.chip text {{ font: 700 14px {SANS}; fill: {INK}; text-anchor: middle; }}
.chip.ghost rect {{ fill: none; stroke: #4A4035; stroke-width: 1.5; }}
.chip.ghost text {{ fill: {MUTED}; font-weight: 500; }}
.pulse {{ transform-origin: 928px 392px; animation: pulse 2.2s ease-in-out infinite; }}
@keyframes drift0 {{ to {{ transform: translate(var(--dx), var(--dy)); }} }}
@keyframes drift1 {{ to {{ transform: translate(calc(var(--dx) * -1), var(--dy)); }} }}
@keyframes drift2 {{ to {{ transform: translate(var(--dx), calc(var(--dy) * -1)); }} }}
@keyframes drift3 {{ to {{ transform: translate(calc(var(--dx) * -.6), calc(var(--dy) * -.6)); }} }}
@keyframes slideIn {{ from {{ opacity: 0; transform: translateX(-18px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes floor {{ from {{ transform: translateY(0) scaleX(1); opacity: 0; }} 20% {{ opacity: 1; }} to {{ transform: translateY(140px) scaleX(2.2); opacity: .2; }} }}
@keyframes ringIn {{ from {{ opacity: 0; transform: scale(.86); }} to {{ opacity: 1; transform: scale(1); }} }}
@keyframes corePop {{ from {{ transform: scale(.6); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}
@keyframes ping {{ 0% {{ transform: scale(1); opacity: .7; }} 100% {{ transform: scale(3.4); opacity: 0; }} }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
@keyframes breathe {{ from {{ transform: scale(.92); opacity: .7; }} to {{ transform: scale(1.06); opacity: 1; }} }}
@keyframes shine {{ 0% {{ transform: translateX(0); opacity: 0; }} 15% {{ opacity: 1; }} 60% {{ transform: translateX(440px); opacity: 0; }} 100% {{ transform: translateX(440px); opacity: 0; }} }}
@keyframes chipIn {{ from {{ opacity: 0; transform: translateY(10px) scale(.92); }} to {{ opacity: 1; transform: none; }} }}
@keyframes pulse {{ 0%, 100% {{ transform: scale(1); opacity: 1; }} 50% {{ transform: scale(1.7); opacity: .35; }} }}
"""
    return svg(W, H, body, style, "Mayank Tiwari, AI full-stack developer and motion designer. LovHack S2 winner, AMPlified national finalist #6. Available for work.")


# ── Proof tiles ───────────────────────────────────────────────────────
def proof() -> str:
    W, H = 1200, 190
    tiles = [
        ("WINNER", "LovHack Season 2", "with PARITY", "trophy"),
        ("#6", "National finalist", "AMPlified Season 1", "ring"),
        ("14+", "Products shipped", "AI apps · games · 3D sites", "bars"),
        ("CI ✓", "Green builds", "on every push", "check"),
    ]
    tw, gap = 282, 24
    parts = []
    for i, (big, label, sub, icon) in enumerate(tiles):
        x = i * (tw + gap)
        d = 0.15 * i
        cx, cy = x + 52, 95
        if icon == "ring":
            ic = (f'<circle cx="{cx}" cy="{cy}" r="22" class="track"/>'
                  f'<circle cx="{cx}" cy="{cy}" r="22" class="arc" style="animation-delay:{d + .5:.2f}s" transform="rotate(-90 {cx} {cy})"/>')
        elif icon == "trophy":
            ic = (f'<g class="bob" style="animation-delay:{d:.2f}s"><path d="M{cx-14} {cy-18}h28v10a14 14 0 0 1-28 0z" fill="{AMBER}"/>'
                  f'<rect x="{cx-4}" y="{cy+4}" width="8" height="8" fill="{AMBER_DEEP}"/><rect x="{cx-11}" y="{cy+12}" width="22" height="5" rx="2" fill="{AMBER}"/>'
                  f'<path d="M{cx-14} {cy-14}h-7a7 7 0 0 0 7 9M{cx+14} {cy-14}h7a7 7 0 0 1-7 9" stroke="{AMBER}" stroke-width="3" fill="none"/></g>'
                  f'<circle cx="{cx+16}" cy="{cy-20}" r="2.5" fill="{CREAM}" class="twinkle" style="animation-delay:{d + 1:.2f}s"/>')
        elif icon == "bars":
            ic = "".join(
                f'<rect x="{cx - 20 + k * 11}" y="{cy + 18 - hgt}" width="8" height="{hgt}" rx="2" fill="{AMBER}" class="bar" style="animation-delay:{d + .4 + k * .12:.2f}s"/>'
                for k, hgt in enumerate([14, 24, 18, 34])
            )
        else:
            ic = (f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{GREEN}" stroke-width="3" opacity=".35"/>'
                  f'<path d="M{cx-10} {cy}l7 7 13-14" class="tick" style="animation-delay:{d + .6:.2f}s"/>')
        parts.append(f"""
<g class="tile" style="animation-delay:{d:.2f}s">
  <rect x="{x + 1}" y="10" width="{tw - 2}" height="170" rx="18" class="card"/>
  <rect x="{x + 1}" y="10" width="{tw - 2}" height="170" rx="18" class="edge" style="animation-delay:{d + 1:.2f}s"/>
  {ic}
  <text x="{x + 96}" y="98" class="big">{big}</text>
  <text x="{x + 96}" y="126" class="lab">{label}</text>
  <text x="{x + 96}" y="148" class="sub">{sub}</text>
</g>""")
    style = f"""
.card {{ fill: {INK}; stroke: {LINE}; stroke-width: 1.5; }}
.edge {{ fill: none; stroke: {AMBER}; stroke-width: 1.5; stroke-dasharray: 120 900; stroke-dashoffset: 0; opacity: .8; animation: edge 6s linear infinite; }}
.tile {{ opacity: 0; animation: up .9s {EASE_CSS} forwards; }}
.big {{ font: 800 34px {SANS}; fill: {CREAM}; letter-spacing: -.5px; }}
.lab {{ font: 600 16px {SANS}; fill: {AMBER}; }}
.sub {{ font: 400 13px {SANS}; fill: {DIM}; }}
.track {{ fill: none; stroke: #3A3128; stroke-width: 5; }}
.arc {{ fill: none; stroke: {AMBER}; stroke-width: 5; stroke-linecap: round; stroke-dasharray: 138; stroke-dashoffset: 138; animation: arc 1.6s {EASE_CSS} forwards; }}
.bar {{ transform-box: fill-box; transform-origin: bottom; transform: scaleY(0); animation: grow 1s cubic-bezier(.34,1.56,.64,1) forwards; }}
.tick {{ fill: none; stroke: {GREEN}; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 40; stroke-dashoffset: 40; animation: arc .9s {EASE_CSS} forwards; }}
.bob {{ transform-box: fill-box; transform-origin: center bottom; animation: bob 3s ease-in-out infinite; }}
.twinkle {{ transform-box: fill-box; transform-origin: center; animation: twinkle 2.4s ease-in-out infinite; }}
@keyframes up {{ from {{ opacity: 0; transform: translateY(16px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes edge {{ to {{ stroke-dashoffset: -1020; }} }}
@keyframes arc {{ to {{ stroke-dashoffset: 26; }} }}
.tick {{ animation-name: tick; }}
@keyframes tick {{ to {{ stroke-dashoffset: 0; }} }}
@keyframes grow {{ to {{ transform: scaleY(1); }} }}
@keyframes bob {{ 0%, 100% {{ transform: translateY(0) rotate(0); }} 50% {{ transform: translateY(-4px) rotate(-3deg); }} }}
@keyframes twinkle {{ 0%, 100% {{ transform: scale(.4); opacity: .2; }} 50% {{ transform: scale(1.2); opacity: 1; }} }}
"""
    return svg(W, H, "".join(parts), style, "Winner of LovHack Season 2 with PARITY. Rank 6 national finalist at AMPlified Season 1. 14 plus products shipped. Green CI builds on every push.")


# ── Project cards ─────────────────────────────────────────────────────
CARDS = [
    ("parity", "PARITY", "AI voice debate arena · 5 rounds · AI judge", "WINNER · LOVHACK S2", ["Gemini", "Web Speech", "WebSockets"]),
    ("career-pathfinder", "Career PathFinder", "Explainable AI learning-path engine", "#6 NATIONAL FINALIST", ["FastAPI", "scikit-learn", "Gemini"]),
    ("backstop", "BackStop", "Policy-gated AI payment recovery for Razorpay", "RAZORPAY BUILDATHON", ["FastAPI", "React 19", "pytest"]),
    ("aevra", "AÉVRA", "Cinematic watch-restoration site + AI intake", "LIVE · LOVABLE HACKATHON", ["React", "GSAP", "R3F"]),
    ("snap", "S.N.A.P.", "Meeting transcripts → decisions and action items", "LIVE ON GOOGLE CLOUD", ["React", "Three.js", "Gemini"]),
    ("ecoops", "ECO-OPS", "Skips wasted CI jobs and reports CO₂ avoided", "GITLAB AI HACKATHON", ["Python", "GitLab CI", "Gemini"]),
]


def card(slug: str, title: str, desc: str, badge: str, tags: list[str]) -> str:
    W, H = 600, 380
    img = base64.b64encode((ROOT / "assets" / "projects" / f"{slug}.jpg").read_bytes()).decode()
    x = 24
    pills = []
    for t in tags:
        w = 16 + len(t) * 8
        pills.append(f'<g><rect x="{x}" y="326" width="{w}" height="28" rx="14" class="pill"/><text x="{x + w / 2}" y="345" class="pt">{t}</text></g>')
        x += w + 8
    bw = 34 + len(badge) * 9.4
    bx = W - 24 - bw
    body = f"""
<defs>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <linearGradient id="shade" x1="0" y1="0" x2="0" y2="1">
    <stop offset=".25" stop-color="{INK}" stop-opacity="0"/>
    <stop offset=".72" stop-color="{INK}" stop-opacity=".92"/>
    <stop offset="1" stop-color="{INK}"/>
  </linearGradient>
  <linearGradient id="gleam" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".16"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
</defs>
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <image href="data:image/jpeg;base64,{img}" x="0" y="0" width="{W}" height="338" preserveAspectRatio="xMidYMid slice" class="kb"/>
  <rect width="{W}" height="{H}" fill="url(#shade)"/>
  <rect x="-200" y="0" width="160" height="{H}" fill="url(#gleam)" class="gleam" transform="skewX(-18)"/>
  <g class="badge"><rect x="{bx:.0f}" y="22" width="{bw:.0f}" height="30" rx="15" fill="{AMBER}"/>
    <circle cx="{bx + 16:.0f}" cy="37" r="4" fill="{INK}" class="dot"/><text x="{bx + 28:.0f}" y="42" class="bt">{badge}</text></g>
  <text x="24" y="270" class="t">{escape(title)}</text>
  <text x="24" y="300" class="d">{escape(desc)}</text>
  {''.join(pills)}
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="19" class="frame"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="19" class="run"/>"""
    style = f"""
.kb {{ transform-origin: 300px 170px; animation: kb 14s ease-in-out infinite alternate; }}
.gleam {{ animation: gleam 5.5s {EASE_CSS} 1s infinite; }}
.badge {{ opacity: 0; animation: drop .8s cubic-bezier(.34,1.56,.64,1) .3s forwards; }}
.bt {{ font: 700 12.5px {MONO}; fill: {INK}; letter-spacing: 1px; }}
.dot {{ transform-box: fill-box; transform-origin: center; animation: blink 1.8s ease-in-out infinite; }}
.t {{ font: 800 32px {SANS}; fill: {CREAM}; letter-spacing: -.5px; opacity: 0; animation: rise .9s {EASE_CSS} .45s forwards; }}
.d {{ font: 400 16px {SANS}; fill: {MUTED}; opacity: 0; animation: rise .9s {EASE_CSS} .6s forwards; }}
.pill {{ fill: {INK2}; stroke: #3A3128; stroke-width: 1; }}
.pt {{ font: 600 12.5px {MONO}; fill: {AMBER}; text-anchor: middle; }}
.frame {{ fill: none; stroke: {LINE}; stroke-width: 2; }}
.run {{ fill: none; stroke: {AMBER}; stroke-width: 2; stroke-dasharray: 140 1800; animation: run 7s linear infinite; }}
@keyframes kb {{ from {{ transform: scale(1); }} to {{ transform: scale(1.09) translate(-8px, -4px); }} }}
@keyframes gleam {{ 0% {{ transform: skewX(-18deg) translateX(0); }} 45%, 100% {{ transform: skewX(-18deg) translateX(1000px); }} }}
@keyframes drop {{ from {{ opacity: 0; transform: translateY(-12px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes run {{ to {{ stroke-dashoffset: -1940; }} }}
"""
    return svg(W, H, body, style, escape(f"{title}: {desc}. {badge}."))


# ── Tech marquee ──────────────────────────────────────────────────────
def marquee() -> str:
    W, H = 1200, 132
    rows = [
        ["React", "TypeScript", "Next.js", "Three.js", "React Three Fiber", "GSAP", "Lenis", "Tailwind", "Vite", "Rive", "SVGator", "WGSL"],
        ["Python", "FastAPI", "Flask", "scikit-learn", "Gemini", "Claude", "MCP servers", "Ollama", "Node.js", "GCP Cloud Run", "Vercel", "GitHub Actions"],
    ]
    groups = []
    for r, items in enumerate(rows):
        x, pills = 0, []
        for it in items * 2:
            w = 30 + len(it) * 9.2
            hot = it in ("Three.js", "Rive", "Gemini", "FastAPI", "GSAP", "MCP servers")
            pills.append(
                f'<g transform="translate({x:.0f} 0)"><rect width="{w:.0f}" height="40" rx="20" class="{"hot" if hot else "p"}"/>'
                f'<text x="{w / 2:.0f}" y="26" class="{"ht" if hot else "tx"}">{it}</text></g>'
            )
            x += w + 12
        half = x / 2
        groups.append(
            f'<g transform="translate(0 {14 + r * 56})"><g class="row{r}" style="--half:-{half:.0f}px">{"".join(pills)}</g></g>'
        )
    body = f"""
<defs>
  <linearGradient id="fade" x1="0" x2="1">
    <stop offset="0" stop-color="{INK}"/><stop offset=".08" stop-color="{INK}" stop-opacity="0"/>
    <stop offset=".92" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}"/>
  </linearGradient>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="{INK}"/>{"".join(groups)}<rect width="{W}" height="{H}" fill="url(#fade)"/></g>"""
    style = f"""
.p {{ fill: {INK2}; stroke: #3A3128; stroke-width: 1.2; }}
.hot {{ fill: {AMBER}; }}
.tx {{ font: 600 15px {SANS}; fill: {MUTED}; text-anchor: middle; }}
.ht {{ font: 700 15px {SANS}; fill: {INK}; text-anchor: middle; }}
.row0 {{ animation: m 38s linear infinite; }}
.row1 {{ animation: m 46s linear infinite reverse; }}
@keyframes m {{ from {{ transform: translateX(0); }} to {{ transform: translateX(var(--half)); }} }}
"""
    return svg(W, H, body, style, "Stack: React, TypeScript, Next.js, Three.js, React Three Fiber, GSAP, Lenis, Tailwind, Vite, Rive, SVGator, WGSL, Python, FastAPI, Flask, scikit-learn, Gemini, Claude, MCP servers, Ollama, Node.js, GCP Cloud Run, Vercel, GitHub Actions.")


# ── Terminal ──────────────────────────────────────────────────────────
def terminal() -> str:
    W, H = 1200, 300
    lines = [
        ("$ whoami", "cmd"),
        ("mayank tiwari · ai full-stack developer & motion designer · lucknow, in", "out"),
        ("$ now --building", "cmd"),
        ("client work on contra · rive + svg motion · ai agents that log their reasoning", "out"),
        ("$ hire --me", "cmd"),
        ("→ contra.com/mayank_tiwari_a4vkcjsh   open for new projects ✓", "ok"),
    ]
    t, defs, rows = 0.6, [], []
    for i, (txt, kind) in enumerate(lines):
        y = 104 + i * 30
        w = len(txt) * 10.2 + 10
        dur = max(0.5, len(txt) * (0.045 if kind == "cmd" else 0.012))
        rows.append(f'<text x="44" y="{y}" class="{kind}">{escape(txt)}</text>'
                    + cover(40, y - 22, w, 30, t, dur, steps=len(txt) if kind == "cmd" else 12))
        t += dur + (0.35 if kind == "cmd" else 0.6)
    caret_y = 104 + (len(lines) - 1) * 30
    body = f"""
<defs>{"".join(defs)}<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="46" fill="{INK2}"/>
  <circle cx="30" cy="23" r="7" fill="#E5675B"/><circle cx="54" cy="23" r="7" fill="#E8B04B"/><circle cx="78" cy="23" r="7" fill="{GREEN}"/>
  <text x="600" y="29" class="bar">nika619 — zsh — 120×24</text>
  {"".join(rows)}
  <rect x="44" y="{caret_y + 14}" width="11" height="20" fill="{AMBER}" class="caret"/>
  <rect y="0" width="{W}" height="3" fill="{AMBER}" opacity=".08" class="scan"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="{LINE}" stroke-width="2"/>"""
    style = f"""
.cmd {{ font: 600 18px {MONO}; fill: {CREAM}; }}
.out {{ font: 400 17px {MONO}; fill: {MUTED}; }}
.ok {{ font: 600 17px {MONO}; fill: {AMBER}; }}
.bar {{ font: 500 13px {MONO}; fill: {DIM}; text-anchor: middle; }}
.caret {{ animation: blink 1.05s steps(1) infinite; }}
{WIPE}
.scan {{ animation: scan 7s linear infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
@keyframes scan {{ from {{ transform: translateY(46px); }} to {{ transform: translateY(300px); }} }}
"""
    return svg(W, H, body, style, "Terminal: whoami, Mayank Tiwari, AI full-stack developer and motion designer in Lucknow. Now building client work on Contra, Rive and SVG motion, AI agents. Hire me at contra.com/mayank_tiwari_a4vkcjsh.")


# ── Divider ───────────────────────────────────────────────────────────
def divider() -> str:
    W, H = 1200, 48
    pts = " ".join(f"{x},{24 + 10 * __import__('math').sin(x / 38):.1f}" for x in range(0, 2401, 12))
    body = f"""
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset=".5" stop-color="{AMBER}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient></defs>
<g class="wave"><polyline points="{pts}" fill="none" stroke="url(#g)" stroke-width="2"/></g>
<g class="wave slow" opacity=".35"><polyline points="{pts}" fill="none" stroke="{CREAM}" stroke-width="1" transform="translate(0 4)"/></g>
<circle cx="600" cy="24" r="4" fill="{AMBER}" class="bead"/>"""
    style = f"""
.wave {{ animation: flow 9s linear infinite; }}
.slow {{ animation-duration: 15s; animation-direction: reverse; }}
.bead {{ transform-box: fill-box; transform-origin: center; animation: bead 2.6s ease-in-out infinite; }}
@keyframes flow {{ to {{ transform: translateX(-239px); }} }}
@keyframes bead {{ 0%, 100% {{ transform: scale(1); opacity: 1; }} 50% {{ transform: scale(1.8); opacity: .4; }} }}
"""
    return svg(W, H, body, style, "Section divider")


# ── Footer ────────────────────────────────────────────────────────────
def footer() -> str:
    W, H = 1200, 240
    bars = "".join(
        f'<rect x="{40 + k * 28}" y="150" width="16" height="70" rx="8" class="eq" style="animation-delay:{-(k * 0.17) % 1.6:.2f}s; animation-duration:{1.1 + (k % 5) * .18:.2f}s"/>'
        for k in range(40)
    )
    body = f"""
<defs>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="20"/></clipPath>
  <linearGradient id="eqg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{AMBER}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>
</defs>
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g opacity=".22">{bars}</g>
  <text x="600" y="92" class="cta">Let's build something people remember.</text>
  {cover(170, 44, 860, 64, 0.3, 1.3)}
  <text x="600" y="130" class="sub">contra.com/mayank_tiwari_a4vkcjsh  ·  portfolio-mayankk1720.vercel.app</text>
</g>"""
    style = f"""
.cta {{ font: 800 44px {SANS}; fill: {CREAM}; text-anchor: middle; letter-spacing: -1px; }}
.sub {{ font: 500 16px {MONO}; fill: {AMBER}; text-anchor: middle; opacity: 0; animation: in 1s {EASE_CSS} 1.2s forwards; }}
{WIPE}
.eq {{ fill: url(#eqg); transform-box: fill-box; transform-origin: bottom; animation: eq ease-in-out infinite alternate; }}
@keyframes in {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes eq {{ from {{ transform: scaleY(.15); }} to {{ transform: scaleY(1); }} }}
"""
    return svg(W, H, body, style, "Let's build something people remember. contra.com/mayank_tiwari_a4vkcjsh, portfolio-mayankk1720.vercel.app")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {"hero.svg": hero(), "proof.svg": proof(), "marquee.svg": marquee(),
             "terminal.svg": terminal(), "divider.svg": divider(), "footer.svg": footer()}
    for slug, *rest in CARDS:
        files[f"card-{slug}.svg"] = card(slug, *rest)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        assert "<script" not in content and "http" not in content.split("<style>")[1].split("</style>")[0]
        print(f"{name:28s} {len(content) // 1024:4d} KB")


if __name__ == "__main__":
    main()
