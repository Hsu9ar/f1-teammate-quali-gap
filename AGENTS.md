# AGENTS.md

## Project Goal

Build a static, browser-based F1 data analysis tool that compares two teammates' qualifying pace across a season using median qualifying gap. The project is intended to be easy to open from GitHub Pages and understandable from the README alone.

## Current Progress

The core app is implemented as a single HTML/CSS/JavaScript file. It fetches live qualifying data from the free Jolpica-F1 API, calculates teammate gaps, visualizes per-race variation, and supports English, Japanese, and Simplified Chinese UI.

## Key Files

- `index.html`: GitHub Pages entry point. Redirects to the main app.
- `f1-teammate-quali-gap.html`: Main static app, including UI, i18n, data fetching, calculations, chart, and table.
- `README.md`: English project documentation.
- `README.ja.md`: Japanese project documentation.
- `README.zh.md`: Simplified Chinese project documentation.
- `.gitignore`: Ignores local cache and OS files.

## Important Conventions

- Keep the app static. Do not introduce a build step unless explicitly requested.
- Keep the primary app in `f1-teammate-quali-gap.html`.
- Use `index.html` only as the GitHub Pages entry point.
- The app uses live Jolpica-F1 API data only. Do not reintroduce local JSON preloading or `build_data.py` unless explicitly requested.
- Chinese documentation and UI should use Simplified Chinese.
- In Chinese, the metric should be called `中位排位差`.
- Avoid adding personal instructions, portfolio notes, or owner-specific setup text to public README files.

## Completed Items

- Interactive season, constructor, and teammate selectors.
- Highest-common-session comparison logic: Q3, then Q2, then Q1.
- Percentage gap calculation: `(t_A - t_B) / t_B * 100`.
- Median, mean, head-to-head, and sample-size summary cards.
- Per-race bar chart with focus view for clipped outliers.
- Click-to-exclude behavior for chart bars and table rows.
- Readable detail table with high-contrast time and gap columns.
- English, Japanese, and Simplified Chinese UI.
- English, Japanese, and Simplified Chinese README files.
- GitHub Pages root entry via `index.html`.

## Unfinished Items

- Confirm the deployed GitHub Pages URL after pushing `index.html`.
- Optionally add a screenshot or short GIF to the README after the UI is final.
- Optionally improve API error handling if Jolpica is unavailable or rate-limited.
- Optionally add tests for calculation helpers if the app grows beyond a single file.

## Next Actions

1. Run syntax checks after any JavaScript edit.
2. Commit changed files, including `index.html` and `AGENTS.md`.
3. Push to GitHub.
4. Enable or verify GitHub Pages on the `main` branch and root folder.
5. Open `https://hsu9ar.github.io/f1-teammate-quali-gap/` to verify one-click launch.

## Common Commands

```bash
# Extract and syntax-check the app script
python3 -c "import re; html=open('f1-teammate-quali-gap.html',encoding='utf-8').read(); open('/tmp/f1_app.js','w',encoding='utf-8').write(re.findall(r'<script>(.*?)</script>', html, re.S)[-1])"
node --check /tmp/f1_app.js

# Check repository status
git status --short --branch

# Commit normal project changes
git add .gitignore index.html f1-teammate-quali-gap.html README.md README.ja.md README.zh.md AGENTS.md
git commit -m "Refine app launch and project documentation"
git push
```

## Notes

- `AGENTS.md` is intended for Claude Cowork / Codex context and may be committed if the repository should preserve agent instructions.
- The app depends on the live Jolpica-F1 API and browser access to the Chart.js CDN.
- If Chart.js CDN access is a problem, vendor the library locally or replace the chart with native canvas/SVG rendering.
- Avoid broad refactors while the project is still a small portfolio-style static app.
