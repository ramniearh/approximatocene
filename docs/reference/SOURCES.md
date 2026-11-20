# Source register and ingest plan

Fifteen sources are registered in `atlas.json`. **Zero are ingested.** Everything
currently rendering is placeholder.

Sources are ordered below by what I would actually do first, which is not the
same as by importance. The ordering is: cheap-and-authoritative before
expensive-and-contested, and anything that changes the *architecture* before
anything that merely adds records.

---

## Tier 1 — do these first

These are small, stable, openly licensed, and each one replaces a whole lane.

### ICS chart → `geo` lane
- **Gives:** every boundary age in the geological column, with official colours.
- **Format:** the chart is published as PDF plus machine-readable versions;
  there are maintained JSON/CSV mirrors.
- **Licence:** CC BY.
- **Effort:** an afternoon. Mostly transcription and a colour lookup.
- **Gotcha:** boundary ages carry published uncertainties (`± n Ma`) that the
  current data file throws away. They should become `lo`/`hi` on each endpoint.
  This is the one lane where real uncertainty figures are readily available, so
  it is a good test of whether the fade encoding reads correctly at scale.

### Smithsonian Human Origins → `hominins` lane
- **Gives:** species ranges with first/last appearance dates.
- **Format:** HTML pages, no API. Hand transcription, ~20 species.
- **Licence:** educational use — check before redistributing values verbatim.
- **Effort:** a day, including cross-checking against primary literature for the
  contested taxa.
- **Gotcha:** the disputed ones (*habilis*, *heidelbergensis*, Denisovans,
  *naledi*) need their dispute recorded in `note`, not silently resolved. Where
  specialists disagree, the atlas should say so rather than pick.

### HYDE 3.3 → `pop` lane
- **Gives:** population from 10,000 BCE, the standard source.
- **Format:** NetCDF and ASCII grids. Needs `xarray`/`netCDF4` and a spatial sum
  to get global totals; the gridded structure is also what would later feed real
  regional lanes.
- **Licence:** CC BY 4.0.
- **Effort:** a day for global totals; longer if you want regional breakdowns.
- **Gotcha:** HYDE publishes lower/upper estimates. Use them. Do not collapse to
  the central value — the band *is* the point of the lane.

### Our World in Data → `pop`, `energy`, emissions
- **Gives:** cleaned, well-documented aggregations with visible provenance.
- **Format:** CSV downloads and an API. The easiest ingest here by a distance.
- **Licence:** CC BY 4.0.
- **Effort:** hours.
- **Gotcha:** it is an aggregator. Cite the underlying source, not OWID, wherever
  OWID itself names one.

---

## Tier 2 — the climate lane, which is a project of its own

The `climate` lane is currently **sine waves**. It is the most dishonest thing in
the build and should either be fixed properly or deleted until it can be.

Doing it properly means splicing four records with different units, resolutions,
and error structures:

| Record | Covers | Measures |
|---|---|---|
| CENOGRID (Westerhold 2020) | 66 Ma | benthic δ¹⁸O + δ¹³C, astronomically tuned |
| LR04 (Lisiecki & Raymo) | 5.3 Ma | benthic δ¹⁸O stack |
| EPICA Dome C | 800 ka | ice-core CO₂ and temperature |
| PAGES 2k | 2 ka | multiproxy surface temperature |

- **Effort:** several days, mostly on the joins.
- **The hard part is not loading them.** These records measure different
  quantities in different units, and stitching them into one apparently
  continuous "temperature" curve is a scientific claim, not a formatting step.
  **The splice points should be visible in the chart** — a marked handover
  showing which record you are looking at. That is the honest design and it is
  also more interesting than a smooth line.

---

## Tier 3 — the evidence lane, computed rather than asserted

Currently the bottom strip is hand-set step values. It is an opinion drawn as if
it were data, which is exactly what the rest of the design tries to avoid.

**p3k14c** (Bird et al. 2022, CC BY, ~180,000 archaeological radiocarbon dates)
would turn it into a measurement: dated sites per millennium, per region,
becomes a real curve of how much evidence exists.

- **Effort:** two or three days.
- **Gotchas, and they are serious:**
  - Calibrated vs uncalibrated. Never mix. Use IntCal20 via a calibration
    library rather than rolling your own.
  - The dataset is heavily biased toward regions where archaeology is
    well-funded. A raw count would show "Europe is better known", which is true,
    but it must be *labelled* as a statement about archaeology rather than about
    the past.
  - Taphonomic bias: older material survives less, so a decay curve is built in.
    Worth showing rather than correcting away.

This is the lane most worth getting right, because it is the one that makes the
atlas's central claim — that confidence varies enormously across the axis — into
something the reader can check rather than something they have to take on trust.

---

## Tier 4 — contested and expensive

### Seshat → `polity` lane
Rich, and methodologically contested in published exchanges about coding
practice and inter-coder reliability. CC BY-NC, which may matter depending on
what this becomes.

**But the prior question is whether the `polity` lane should exist.** It
currently draws a smooth stacked ribbon of "share of humanity under each
political form". Nobody has those numbers for any period before the last two
centuries, the categories (especially "chiefdom") are contested constructs, and
the visual smoothness implies a precision that does not exist. It is the
prettiest lane and the least defensible.

Three options, in my order of preference:
1. **Reframe as explicitly schematic** — coarse blocks, visible seams, labelled
   as an argument about political forms rather than a measurement of them.
2. **Replace with something countable** — e.g. largest polity size over time,
   which is genuinely estimable and nearly as interesting.
3. Keep it and source it from Seshat, surfacing the methodological dispute.

### Maddison Project → economic lanes
Solid, well-documented, 1 CE onward. Straightforward ingest. Deep pre-modern
figures are reconstructions with wide error bars that the published data
documents honestly — carry that through rather than flattening it.

### Morris energy index → `energy` lane
Published as book tables, under copyright. Figures must be re-keyed by hand and
attributed; do not scrape. Consider whether OWID's energy series plus a simpler
derivation would serve better and cite more cleanly.

---

## Sequenced plan

**Step 1 — schema hardening (before any bulk ingest).**
Fix the entity/dating separation described at the end of `SCHEMA.md`, add the
`14C BP` unit that refuses to auto-convert, and add per-sample date uncertainty
to `series`. Retrofitting these after a few thousand records exist is
significantly worse than doing them now against 123.

**Step 2 — Tier 1 ingest.** ICS, Smithsonian, HYDE, OWID. Four lanes stop being
fictional. Write one small ingest script per source, each emitting a JSON
fragment that the build merges, so a source can be re-run when it updates.

**Step 3 — decide the `polity` lane's fate.** This is a judgement call about the
project's purpose, not a data task, and it blocks nothing else — but it will
feel worse the more polished everything around it becomes.

**Step 4 — climate lane, with visible splices.**

**Step 5 — evidence lane from p3k14c.**

**Step 6 — regional expansion.** Only after the entity/dating fix, or you will
be duplicating labels across dozens of regions.

---

## One thing to decide early

Every source above will be revised. ICS boundary ages move, hominin dates move a
lot, HYDE releases new versions. Either pin versions and state them in the UI,
or build a refresh path. Pinning is easier and more honest for an atlas —
"boundary ages as of ICS 2023" is a fact a reader can check, while a silently
updating chart is not reproducible.
