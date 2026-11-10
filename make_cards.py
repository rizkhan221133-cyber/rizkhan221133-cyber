"""Banner and project cards for a GitHub profile README.

Edit the PROFILE and PROJECTS sections below, then run:

    python make_cards.py

It writes assets/banner-dark.svg, assets/banner-light.svg and one card per
project (assets/<slug>.svg, dark) plus assets/<slug>-light.svg.
"""
import os
from html import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# ------------------------------------------------------------------ edit me
PROFILE = {
    "name": "Rizwan Khan",
    "kicker": "SOFTWARE DEVELOPER · PAKISTAN",
    "bio": ["I build apps that are simple to use,", "look good, and solve real problems."],
    "tags": ["React", "TypeScript", "Node.js", "Python", "Flutter"],
    # lines in the little code window: (key, value)
    "about": [("based", '"Pakistan"'), ("builds", '["web", "mobile"]'),
              ("loves", '"unicorns"'), ("learning", '"every day"'), ("ships", "true")],
}

# accent: any hex colour. status: "Live demo", "In progress", "Open source" ...
PROJECTS = [
    {"slug": "project-one", "title": "Project One", "subtitle": "Short tagline here",
     "desc": "One or two sentences about what this project does and who it helps. Keep it short.",
     "tags": ["React", "TypeScript", "Firebase"], "status": "Live demo", "accent": "#EC4899"},
    {"slug": "project-two", "title": "Project Two", "subtitle": "Short tagline here",
     "desc": "One or two sentences about what this project does and who it helps. Keep it short.",
     "tags": ["Flutter", "Dart"], "status": "Open source", "accent": "#8B5CF6"},
    {"slug": "project-three", "title": "Project Three", "subtitle": "Short tagline here",
     "desc": "One or two sentences about what this project does and who it helps. Keep it short.",
     "tags": ["Python", "FastAPI", "PostgreSQL"], "status": "In progress", "accent": "#06B6D4"},
    {"slug": "project-four", "title": "Project Four", "subtitle": "Short tagline here",
     "desc": "One or two sentences about what this project does and who it helps. Keep it short.",
     "tags": ["Node.js", "MongoDB"], "status": "Live demo", "accent": "#F59E0B"},
]
# --------------------------------------------------------------------------

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg1="#0B0A1A", bg2="#141029", border="#2A2347", kicker="#A78BFA",
                 bio="#B8B3CC", chip="#1D1834", chipb="#352D57", chipt="#E4DEF7",
                 win="#110E22", winb="#2E2650", key="#E6E1F5", fname="#6F6890",
                 card1="#120F24", card2="#0C0A19", title="#F5F3FF", sub="#8D86A8",
                 desc="#B8B3CC", glow=0.32),
    "light": dict(bg1="#FFFFFF", bg2="#F6F2FF", border="#E4DCF7", kicker="#7C3AED",
                  bio="#4B4563", chip="#F3EEFF", chipb="#DDD2FA", chipt="#3B2F66",
                  win="#1A1630", winb="#2E2650", key="#E6E1F5", fname="#8B84A8",
                  card1="#FFFFFF", card2="#F8F5FF", title="#1E1838", sub="#6B6488",
                  desc="#4B4563", glow=0.18),
}

# rough average glyph width ratio, good enough to size chips
def text_w(s, size, bold=False):
    return len(s) * size * (0.58 if bold else 0.54)


def banner(theme):
    t, p = THEMES[theme], PROFILE
    chips, x = [], 72
    for tag in p["tags"]:
        w = text_w(tag, 15, True) + 30
        chips.append(
            f'<g transform="translate({x:.1f},300)"><rect width="{w:.1f}" height="36" rx="18" '
            f'fill="{t["chip"]}" stroke="{t["chipb"]}"/><text x="{w/2:.1f}" y="23.5" '
            f'text-anchor="middle" font-size="15" font-weight="600" fill="{t["chipt"]}">'
            f'{escape(tag)}</text></g>')
        x += w + 10
    var = p["name"].split()[0].lower()
    code = [f'<tspan fill="#C792EA">const </tspan><tspan fill="#82AAFF">{escape(var)}</tspan>'
            f'<tspan fill="#89DDFF"> = {{</tspan>']
    for k, v in p["about"]:
        col = "#F78C6C" if v in ("true", "false") else "#C3E88D"
        code.append(f'<tspan fill="{t["key"]}">  {escape(k)}: </tspan><tspan fill="{col}">'
                    f'{escape(v)}</tspan><tspan fill="#89DDFF">,</tspan>')
    code.append('<tspan fill="#89DDFF">};</tspan>')
    lines = "\n".join(
        f'      <text x="28" y="{78 + i*26}" font-family="{MONO}" font-size="15.5" class="cl" '
        f'style="animation-delay:{0.5 + i*0.12:.2f}s" xml:space="preserve">{c}</text>'
        for i, c in enumerate(code))
    cur_y = 78 + (len(code) - 1) * 26 - 15
    bio = "\n".join(f'  <text x="72" y="{232 + i*30}" font-size="22" fill="{t["bio"]}">{escape(b)}</text>'
                    for i, b in enumerate(p["bio"]))
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="{o}" class="tw" style="animation-delay:{d}s"/>'
                    for x, y, r, o, d in [(690, 60, 1.6, .7, 0), (735, 360, 1.2, .5, .8), (1235, 56, 1.4, .6, 1.6),
                                          (640, 250, 1, .4, 2.4), (1240, 372, 1.6, .6, .4)]) if theme == "dark" else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="420" viewBox="0 0 1280 420" font-family="{FONT}">
  <title>{escape(p["name"])}</title>
  <style>
    .cl {{ opacity: 0; animation: fade .5s ease-out forwards; }}
    .glow {{ animation: drift 14s ease-in-out infinite alternate; }}
    .cur {{ animation: blink 1.1s steps(1) infinite; }}
    .tw {{ animation: tw 3s ease-in-out infinite; }}
    .rb {{ stroke-dasharray: 1500; stroke-dashoffset: 1500; animation: draw 3s cubic-bezier(.3,.6,.2,1) forwards; }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes drift {{ from {{ transform: translate(0,0); }} to {{ transform: translate(-60px, 24px); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes tw {{ 50% {{ opacity: .1; }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .cl {{ animation: none; opacity: 1; }} .rb {{ animation: none; stroke-dashoffset: 0; }} .glow, .cur, .tw {{ animation: none; }} }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>
    <radialGradient id="ga"><stop offset="0" stop-color="#EC4899" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="#EC4899" stop-opacity="0"/></radialGradient>
    <radialGradient id="gb"><stop offset="0" stop-color="#8B5CF6" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/></radialGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F472B6"/><stop offset=".35" stop-color="#FB923C"/><stop offset=".65" stop-color="#A78BFA"/><stop offset="1" stop-color="#38BDF8"/></linearGradient>
    <clipPath id="clip"><rect width="1280" height="420" rx="24"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="1280" height="420" fill="url(#bg)"/>
    <ellipse class="glow" cx="1020" cy="70" rx="420" ry="300" fill="url(#ga)"/>
    <ellipse class="glow" cx="160" cy="420" rx="420" ry="260" fill="url(#gb)" style="animation-delay:-7s"/>
    <g fill="none" stroke-width="5" stroke-linecap="round" opacity=".55">
      <path class="rb" d="M-20,404 C260,330 520,400 760,350 S1120,250 1300,300" stroke="#F472B6"/>
      <path class="rb" d="M-20,412 C260,338 520,408 760,358 S1120,258 1300,308" stroke="#FBBF24" style="animation-delay:.1s"/>
      <path class="rb" d="M-20,420 C260,346 520,416 760,366 S1120,266 1300,316" stroke="#34D399" style="animation-delay:.2s"/>
      <path class="rb" d="M-20,428 C260,354 520,424 760,374 S1120,274 1300,324" stroke="#60A5FA" style="animation-delay:.3s"/>
      <path class="rb" d="M-20,436 C260,362 520,432 760,382 S1120,282 1300,332" stroke="#A78BFA" style="animation-delay:.4s"/>
    </g>
    {stars}
  </g>
  <rect x="0.5" y="0.5" width="1279" height="419" rx="24" fill="none" stroke="{t["border"]}"/>

  <text x="72" y="118" font-size="14" font-weight="700" letter-spacing="2.4" fill="{t["kicker"]}">{escape(p["kicker"])}</text>
  <text x="70" y="186" font-size="62" font-weight="800" letter-spacing="-1.6" fill="url(#name)">{escape(p["name"])}</text>
{bio}
  {"".join(chips)}

  <g transform="translate(790,82)">
    <rect width="420" height="256" rx="16" fill="{t["win"]}" stroke="{t["winb"]}"/>
    <circle cx="26" cy="26" r="6" fill="#FF5F57"/><circle cx="46" cy="26" r="6" fill="#FEBC2E"/><circle cx="66" cy="26" r="6" fill="#28C840"/>
    <text x="394" y="31" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{t["fname"]}">about.ts</text>
{lines}
    <rect class="cur" x="52" y="{cur_y}" width="9" height="19" fill="#F472B6"/>
  </g>
</svg>
'''


def wrap(text, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, size) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines[:3]


def card(pr, theme):
    t, a = THEMES[theme], pr["accent"]
    desc = "\n".join(f'  <text x="32" y="{120 + i*26}" font-size="17" fill="{t["desc"]}">{escape(l)}</text>'
                     for i, l in enumerate(wrap(pr["desc"], 17, 476)))
    chips, x = [], 32.0
    for tag in pr["tags"]:
        w = text_w(tag, 13, True) + 24
        chips.append(f'<g transform="translate({x:.1f},212)"><rect width="{w:.1f}" height="28" rx="14" fill="{a}" '
                     f'fill-opacity="0.13" stroke="{a}" stroke-opacity="0.4"/><text x="{w/2:.1f}" y="18.5" '
                     f'text-anchor="middle" font-size="13" font-weight="600" fill="{a}">{escape(tag)}</text></g>')
        x += w + 8
    sw = text_w(pr["status"], 12.5, True) + 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="540" height="270" viewBox="0 0 540 270" font-family="{FONT}">
  <title>{escape(pr["title"])} — {escape(pr["desc"])}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["card1"]}"/><stop offset="1" stop-color="{t["card2"]}"/></linearGradient>
    <radialGradient id="glow" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{a}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
    <clipPath id="c"><rect width="540" height="270" rx="20"/></clipPath>
  </defs>
  <g clip-path="url(#c)">
    <rect width="540" height="270" fill="url(#bg)"/>
    <rect width="540" height="270" fill="url(#glow)"/>
  </g>
  <rect x="0.5" y="0.5" width="539" height="269" rx="20" fill="none" stroke="{t["border"]}"/>
  <rect x="32" y="30" width="48" height="48" rx="13" fill="{a}"/>
  <text x="56" y="62" text-anchor="middle" font-size="22" font-weight="800" fill="#FFFFFF">{escape(pr["title"][:1])}</text>
  <text x="96" y="52" font-size="23" font-weight="750" letter-spacing="-0.4" fill="{t["title"]}">{escape(pr["title"])}</text>
  <text x="96" y="73" font-size="13.5" font-weight="500" fill="{t["sub"]}">{escape(pr["subtitle"])}</text>
  <g transform="translate({508 - sw:.1f},36)">
    <rect width="{sw:.1f}" height="28" rx="14" fill="#22C55E" fill-opacity="0.12" stroke="#22C55E" stroke-opacity="0.35"/>
    <circle cx="15" cy="14" r="4" fill="#22C55E"/>
    <text x="26" y="18.5" font-size="12.5" font-weight="650" fill="#16A34A">{escape(pr["status"])}</text>
  </g>
{desc}
  {"".join(chips)}
</svg>
'''


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for th in ("dark", "light"):
        open(os.path.join(OUT, f"banner-{th}.svg"), "w", encoding="utf-8").write(banner(th))
        for pr in PROJECTS:
            name = pr["slug"] + ("" if th == "dark" else "-light")
            open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8").write(card(pr, th))
    print("wrote banner + %d project cards to %s" % (len(PROJECTS), OUT))
