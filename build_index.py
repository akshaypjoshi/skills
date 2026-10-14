#!/usr/bin/env python3
"""Render the hub (index.html, 404.html, favicon) from skills.json into <out-dir>.

    python3 build_index.py <out-dir>
"""
import html
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
esc = html.escape

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@800;900&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
:root {{ --paper:#F0EBE3; --card:#F9F7F2; --ink:#1A1916; --ink-2:#4A4740; --ink-3:#8A857B; --rule:#DDD6CA;
  --display:"Inter Tight","Inter",system-ui,sans-serif; --body:"Inter",system-ui,sans-serif; --mono:"JetBrains Mono",ui-monospace,Menlo,monospace; color-scheme:light; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --paper:#161512; --card:#1E1C18; --ink:#F1ECE3; --ink-2:#C4BDB0; --ink-3:#8C8577; --rule:#34302A; color-scheme:dark; }} }}
:root[data-theme="dark"] {{ --paper:#161512; --card:#1E1C18; --ink:#F1ECE3; --ink-2:#C4BDB0; --ink-3:#8C8577; --rule:#34302A; color-scheme:dark; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--paper); color:var(--ink); font:16.5px/1.65 var(--body); -webkit-font-smoothing:antialiased; }}
a {{ color:inherit; }}
.wrap {{ max-width:1080px; margin:0 auto; padding:0 16px; }}
.nav {{ display:flex; justify-content:space-between; gap:16px; padding:18px 0; font:13px var(--mono); color:var(--ink-3); }}
.nav a {{ color:var(--ink-3); text-decoration:none; }} .nav a:hover {{ color:var(--ink); }}
h1 {{ font:900 clamp(44px,8vw,84px)/.95 var(--display); letter-spacing:-.035em; margin:56px 0 16px; }}
.lead {{ color:var(--ink-2); font-size:clamp(17px,2vw,20px); max-width:620px; margin:0 0 44px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; }}
.skill {{ --a:var(--al); --t:var(--tl); display:flex; flex-direction:column; text-decoration:none; background:var(--card); border:1px solid var(--rule); border-radius:18px; overflow:hidden; transition:transform .15s; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) .skill {{ --a:var(--ad); --t:var(--td); }} }}
:root[data-theme="dark"] .skill {{ --a:var(--ad); --t:var(--td); }}
.skill:hover {{ transform:translateY(-2px); }}
.skill:focus-visible {{ outline:2px solid var(--a); outline-offset:3px; }}
.art {{ position:relative; height:170px; background:var(--t); overflow:hidden; }}
.art span {{ position:absolute; right:-6px; bottom:-.2em; font:900 150px/.8 var(--display); letter-spacing:-.06em; color:var(--a); }}
.body {{ padding:18px 22px 22px; }}
.body h2 {{ font:800 24px/1.15 var(--display); letter-spacing:-.01em; margin:0 0 8px; }}
.body p {{ margin:0 0 14px; color:var(--ink-2); font-size:15px; }}
.tags {{ display:flex; flex-wrap:wrap; gap:6px; }}
.tags span {{ font:500 11px var(--mono); padding:4px 8px; border:1px solid var(--rule); border-radius:999px; color:var(--ink-2); }}
footer {{ margin:88px 0 0; padding:24px 0 40px; border-top:1px solid var(--rule); font-size:14px; color:var(--ink-3); display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; }}
footer a {{ color:var(--ink-2); }}
@media (prefers-reduced-motion: reduce) {{ .skill {{ transition:none; }} .skill:hover {{ transform:none; }} }}
</style>
</head>
<body>
<div class="wrap">
"""

FOOT = """<footer><span>Skills by Akshay Joshi. Each skill is open source.</span>
<span><a href="https://akshayjoshi.dev">akshayjoshi.dev</a> · <a href="https://github.com/akshaypjoshi">GitHub</a></span></footer>
</div>
</body>
</html>
"""


def card(s):
    style = f"--al:{s['accent']};--tl:{s['tint']};--ad:{s.get('accentDark', s['accent'])};--td:{s.get('tintDark', s['tint'])}"
    tags = "".join(f"<span>{esc(t)}</span>" for t in s.get("tags", []))
    return (f'<a class="skill" href="/{esc(s["name"])}/" style="{style}">'
            f'<div class="art" aria-hidden="true"><span>{esc(s.get("glyph", s["name"][:2].upper()))}</span></div>'
            f'<div class="body"><h2>{esc(s["title"])}</h2><p>{esc(s["summary"])}</p><div class="tags">{tags}</div></div></a>')


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    skills = json.loads((HERE / "skills.json").read_text())
    desc = "Agent skills by Akshay Joshi, for Claude Code and other coding agents."
    index = (HEAD.format(title="Skills by Akshay Joshi", desc=desc)
             + '<nav class="nav"><span>skills.akshayjoshi.dev</span><a href="https://github.com/akshaypjoshi">GitHub</a></nav>'
             + '<h1>Skills</h1><p class="lead">Agent skills for Claude Code and other coding agents. Each one installs with a single command and ships with its own page and live demo.</p>'
             + f'<div class="grid">{"".join(card(s) for s in skills)}</div>' + FOOT)
    (out / "index.html").write_text(index, encoding="utf-8")
    nf = (HEAD.format(title="Not found", desc=desc)
          + '<nav class="nav"><a href="/">skills.akshayjoshi.dev</a></nav>'
          + '<h1>Not found</h1><p class="lead">That page doesn\'t exist. <a href="/">See all skills</a>.</p>' + FOOT)
    (out / "404.html").write_text(nf, encoding="utf-8")
    shutil.copy2(HERE / "favicon.svg", out / "favicon.svg")
    print(f"hub built in {out}: {len(skills)} skill(s)")


if __name__ == "__main__":
    main()
