# F1 Teammate Qualifying Gap

English | [日本語](./README.ja.md)

An interactive, single-file web app that compares two teammates' **single-lap (qualifying) pace** across an F1 season using the **median qualifying gap** — a metric that is robust to crashes, yellow flags, and mechanical failures.

🔗 **Live demo:** _(enable GitHub Pages, then put your URL here, e.g. `https://<your-username>.github.io/<repo>/f1-teammate-quali-gap.html`)_

![screenshot](docs/screenshot.png)

## Why median, not mean?

Qualifying gaps are full of contaminated samples: a crash, a lap deleted under yellow, a Q1 knockout with only one timed run. These produce extreme values that drag the **mean** away from reality. The **median** ignores outliers, so it reflects the typical gap between two drivers far more reliably.

## How the metric is computed

For every round of the season:

1. Take each driver's fastest lap in the **highest qualifying session both reached** (Q3 > Q2 > Q1) — so the comparison is always like-for-like.
2. Compare as a **percentage**, not raw seconds, to remove track-length differences:
   `gap% = (t_A − t_B) / t_B × 100`
3. Take the **median** of those per-round percentages over the season.

Caveats: dry/wet sessions are not separated by the data source — exclude wet rounds manually (click the bar or table row). The metric measures qualifying/single-lap pace only, not race pace.

## Features

- Pick **season → constructor → two drivers**; everything recomputes instantly.
- **Median / mean / head-to-head / sample size** summary cards.
- Per-race bar chart with a robust y-axis that **clips extreme outliers** (their true value is labelled on the bar) so normal gaps stay readable. Toggle it off to see the full range.
- **Click any bar or table row to exclude** that round; the median recomputes live.
- UI in **English / 日本語 / 中文** (switcher, top-right).
- **Local-first data**: works offline / in regions where the live API is unreachable.

## Data source

Free [Jolpica-F1 API](https://github.com/jolpica/jolpica-f1) (the successor to the deprecated Ergast API). No API key required.

## Running it

It's a single static HTML file — just open `f1-teammate-quali-gap.html` in a browser.

The page tries to load local data first (`data/quali-<year>.json`) and falls back to the live API. If the live API is unreachable (network / CORS / region block), generate local data once:

```bash
python build_data.py 2024            # one season
python build_data.py 2021 2022 2023 2024   # several
```

This writes `data/quali-<year>.json`. Refresh the page — it now runs offline.

### Optional: richer data via FastF1

`build_data.py` includes a `build_with_fastf1()` example. [FastF1](https://docs.fastf1.dev/) is a Python library (not a browser API) that can pull telemetry, tyre, and practice data. Install with `pip install fastf1` and switch the call in `main()` if you want to extend the dataset.

## Deploy on GitHub Pages

1. Create a repository and push these files (see below).
2. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch `main`, folder `/ (root)`, **Save**.
3. After a minute your page is live at `https://<your-username>.github.io/<repo>/f1-teammate-quali-gap.html`.

## Project structure

```
f1-teammate-quali-gap.html   # the app (HTML + CSS + JS, single file)
build_data.py                # Jolpica → data/quali-<year>.json (FastF1 optional)
data/                        # generated JSON (optional, for offline use)
README.md / README.ja.md     # docs
```

## License

MIT
