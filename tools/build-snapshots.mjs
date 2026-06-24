#!/usr/bin/env node
/**
 * build-snapshots.mjs — generate the bundled offline fallback data.
 *
 * Fetches qualifying results from the Jolpica-F1 API and writes one file per
 * season to ../data/quali-<year>.json, in the exact processed shape the app
 * consumes ({ year, rounds:[{ round, raceName, results:[...] }] }).
 *
 * The app uses these files only as a last resort, when the live API and the
 * CORS-proxy fallbacks are all unreachable (e.g. API maintenance). Run this
 * locally whenever you want to refresh the offline snapshots, then commit the
 * updated data/ files.
 *
 * Node has no CORS restriction, so this works even when the in-browser fetch
 * is blocked by CORS. Requires Node 18+ (global fetch).
 *
 * Usage:
 *   node tools/build-snapshots.mjs              # default seasons
 *   node tools/build-snapshots.mjs 2023 2024 2025
 */
import { writeFile, mkdir, access } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const API = 'https://api.jolpi.ca/ergast/f1';
const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, '..', 'data');

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function fetchJSON(url, tries = 5) {
  let lastErr = null;
  for (let i = 0; i < tries; i++) {
    if (i > 0) await sleep(800 * 2 ** (i - 1));
    let r;
    try { r = await fetch(url, { headers: { Accept: 'application/json' } }); }
    catch (e) { lastErr = e; continue; }
    if (r.status === 429) {                       // rate limited
      const ra = parseInt(r.headers.get('Retry-After'), 10);
      await sleep((isNaN(ra) ? 5 : Math.min(ra, 10)) * 1000);
      lastErr = new Error('rate limited'); continue;
    }
    if (!r.ok) throw new Error(`HTTP ${r.status} for ${url}`);
    return r.json();
  }
  throw lastErr || new Error('failed: ' + url);
}

async function buildSeason(year) {
  const byRound = new Map();
  let offset = 0, total = Infinity;
  while (offset < total) {
    const j = await fetchJSON(`${API}/${year}/qualifying/?format=json&limit=100&offset=${offset}`);
    const md = j.MRData; total = parseInt(md.total, 10);
    const races = md.RaceTable.Races || [];
    for (const race of races) {
      if (!byRound.has(race.round)) byRound.set(race.round, { round: race.round, raceName: race.raceName, results: [] });
      const bucket = byRound.get(race.round);
      for (const q of (race.QualifyingResults || [])) {
        bucket.results.push({
          driverId: q.Driver.driverId,
          code: q.Driver.code || q.Driver.familyName.slice(0, 3).toUpperCase(),
          name: q.Driver.familyName,
          constructorId: q.Constructor.constructorId,
          constructorName: q.Constructor.name,
          Q1: q.Q1 || '', Q2: q.Q2 || '', Q3: q.Q3 || '',
        });
      }
    }
    offset += 100;
    if (races.length === 0) break;
    await sleep(300);                             // stay well under the rate limit
  }
  const rounds = [...byRound.values()].sort((a, b) => +a.round - +b.round);
  return { year: String(year), rounds };
}

// Default: every season with the Q1/Q2/Q3 format (2006) through the current year.
const FIRST_SEASON = 2006;
function defaultYears() {
  const now = new Date().getFullYear();
  const out = [];
  for (let y = FIRST_SEASON; y <= now; y++) out.push(String(y));
  return out;
}
// Flags: --force re-fetches even seasons that already have a file.
const args = process.argv.slice(2);
const force = args.includes('--force');
const yearArgs = args.filter(a => /^\d{4}$/.test(a));
const years = yearArgs.length ? yearArgs : defaultYears();
const CURRENT = new Date().getFullYear();

const exists = async p => { try { await access(p); return true; } catch { return false; } };

await mkdir(DATA_DIR, { recursive: true });
for (const y of years) {
  const file = join(DATA_DIR, `quali-${y}.json`);
  // Past seasons never change — skip if already saved (unless --force). Always refresh the current season.
  if (!force && +y < CURRENT && await exists(file)) { console.log(`Skipping ${y} (already saved).`); continue; }
  process.stdout.write(`Fetching ${y}… `);
  try {
    const data = await buildSeason(y);
    if (!data.rounds.length) { console.log('no data, skipped.'); continue; }
    await writeFile(file, JSON.stringify(data));
    console.log(`saved ${data.rounds.length} rounds -> data/quali-${y}.json`);
  } catch (e) {
    console.log(`FAILED (${e.message})`);
  }
}
console.log('Done. Commit the data/ files to ship them as offline fallback.');
