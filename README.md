# skills.akshayjoshi.dev

Source for [skills.akshayjoshi.dev](https://skills.akshayjoshi.dev): an index of my agent skills, with each skill's own site under `/<name>/`.

| Path | Built from |
|---|---|
| `/` | `build_index.py` + `skills.json` (this repo) |
| `/course-studio/` | [akshaypjoshi/course-studio](https://github.com/akshaypjoshi/course-studio) `site/build.py` |
| `/course-lab/` | [akshaypjoshi/course-lab](https://github.com/akshaypjoshi/course-lab) `site/build.py` |

## How it publishes

`.github/workflows/pages.yml` builds the index, then clones each repo listed in `skills.json` and runs its `build` script into `_site/<name>/`, and deploys the result to GitHub Pages. It runs on every push here, daily at 03:17 UTC, on manual dispatch, and on a `skill-updated` repository dispatch (so a skill repo can trigger a redeploy when its `main` changes).

## Add a skill

1. Give the skill repo a script that takes an output directory and writes a self-contained site into it (see course-studio's `site/build.py`).
2. Add an entry to `skills.json` (`name`, `title`, `repo`, `build`, `summary`, `tags`, `glyph`, colours).
3. Push. The skill appears at `skills.akshayjoshi.dev/<name>/`.

## Local preview

```bash
python3 build_index.py _site
git clone --depth 1 https://github.com/akshaypjoshi/course-studio /tmp/cs && python3 /tmp/cs/site/build.py _site/course-studio
python3 -m http.server -d _site 8000
```

## Domain

Custom domain `skills.akshayjoshi.dev`, set in the repository's Pages settings. DNS: a `CNAME` record `skills` → `akshaypjoshi.github.io` (Cloudflare, DNS only).
