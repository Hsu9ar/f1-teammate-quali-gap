# F1 Teammate Median Qualifying Gap

English | [日本語](./README.ja.md) | [简体中文](./README.zh.md)

[**Launch App**](https://hsu9ar.github.io/f1-teammate-quali-gap/)

An interactive browser tool for comparing two Formula 1 teammates' qualifying pace across a season. It uses the **median qualifying gap** to reduce the influence of outlier sessions such as crashes, yellow flags, technical issues, or heavily compromised laps.

## What This Tool Does

- Loads F1 qualifying results from the free Jolpica-F1 API.
- Lets users choose a season, constructor, and two teammates.
- Calculates per-race percentage gaps, season median, season mean, head-to-head score, and sample size.
- Visualizes every race in a bar chart with a focus view for extreme outliers.
- Lets users exclude unrepresentative rounds by clicking a chart bar or table row.
- Supports English, Japanese, and Simplified Chinese UI.

## How To Use It

1. Open the app from the launch link above.
2. Select a season, constructor, Driver A, and Driver B.
3. Read the summary cards for median gap, mean gap, head-to-head score, and valid race count.
4. Use the chart to inspect round-by-round variation.
5. Click a bar or table row to exclude wet, crashed, or otherwise unrepresentative sessions.
6. Toggle **Focus view** to switch between a readable outlier-clipped chart and the full chart scale.

## How To Read The Metric

The gap is calculated from Driver A's lap time relative to Driver B's lap time:

```text
gap% = (t_A - t_B) / t_B * 100
```

- Positive value: Driver A was slower than Driver B.
- Negative value: Driver A was faster than Driver B.
- Median: the typical season gap after sorting all valid per-race gaps.
- Mean: useful as a reference, but more sensitive to extreme sessions.

## Calculation Method

For each qualifying session:

1. Find the highest qualifying segment both drivers reached: Q3, then Q2, then Q1.
2. Take each driver's fastest lap in that shared segment.
3. Convert the lap-time difference into a percentage.
4. Compute the season median from all included rounds.

This avoids comparing a Q3 lap against a Q1 lap and makes gaps comparable across tracks of different lengths.

## Data Source

The app uses the free [Jolpica-F1 API](https://github.com/jolpica/jolpica-f1), the community successor to the Ergast API. No API key is required.

## Limitations

- The source data does not label wet and dry sessions.
- Deleted laps, traffic, yellow flags, and mechanical issues may still require manual exclusion.
- The metric reflects qualifying and single-lap pace only. It does not measure race pace, tyre management, or strategy execution.
- The app depends on live API availability.

## Project Structure

```text
index.html                   # GitHub Pages entry point
f1-teammate-quali-gap.html   # Static web app
README.md                    # English documentation
README.ja.md                 # Japanese documentation
README.zh.md                 # Simplified Chinese documentation
```

## License

MIT
