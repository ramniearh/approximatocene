# Atlas data model

The whole visualisation is generated from `data/atlas.json`. Adding a species, a
region, a periodisation scheme or an entire lane is a data edit, not a code edit.
This document is the contract.

## 1. Time

**One canonical unit: years before 2000 CE (`b2k`). Positive is past.**

The present is a *negative* number (about −26 in 2026). This is deliberate. If
the origin were "now", every stored value would silently change meaning each
year, and any cached or exported figure would drift.

Every date in the source file is written as a **string with an explicit unit**.
There are no bare numbers. This is the single most important rule in the schema:
conflating BP-1950 with b2k, or uncalibrated with calibrated radiocarbon, is the
classic way this kind of project acquires errors nobody can later find.

| Written | Means | Canonical |
|---|---|---|
| `"4.6 Ga"` | 4.6 billion years ago | `4600000000` |
| `"66.0 Ma"` | 66 million years ago | `66000000` |
| `"11.7 ka"` | 11,700 years ago | `11700` |
| `"11700 b2k"` | before 2000 CE | `11700` |
| `"12000 BP"` | before 1950 CE | `12050` |
| `"3300 BCE"` | calendar, BCE | `5300` |
| `"1750 CE"` | calendar, CE | `250` |
| `"now"` | the present | `-26` |
| `"200 yr"` | a *duration*, not a date | `200` |

The parser lives in exactly one place (`parseTime`) and throws on anything it
does not recognise. The build script runs the same check offline, so unit errors
fail the build rather than surfacing as a bar in the wrong millennium.

**Still to add:** radiocarbon dates need `"3200 14C BP"` as a distinct unit that
refuses to convert without a calibration curve. Do not let uncalibrated dates in
under the `BP` label.

## 2. Time points and uncertainty

Any field named `t0` or `t1` is a **time point**, and may be either form:

```json
"t0": "1750 CE"

"t0": { "est": "315 ka", "lo": "350 ka", "hi": "260 ka", "note": "…" }
```

`lo` and `hi` are the **oldest** and **youngest** plausible dates, written as
ordinary time strings so nobody has to think about sign conventions. After
parsing they are normalised to `{ est, older, younger, certain }`.

`t0` is always the older endpoint of an interval, `t1` the younger.

Uncertainty is therefore attached **per endpoint**, not per record. An interval
can have a firmly dated start and a vague end, which is the normal case in
archaeology and was not expressible in the v0.1 pilot.

The renderer draws this literally: the bar is fully opaque between
`t0.younger` and `t1.older`, and fades out across each endpoint's plausible
range. A reader can see the shape of the uncertainty without reading a number.

## 3. Record types

Five dataset kinds, each with a matching `encoding` in the lane definition.

### `intervals` / `ranked-intervals` / `grouped-intervals`
```json
{
  "id": "h-sapiens",
  "label": "H. sapiens",
  "t0": { "est": "315 ka", "lo": "350 ka", "hi": "260 ka" },
  "t1": "now",
  "rank": 3,                       // ranked-intervals only: nesting depth
  "region": "africa",              // grouped-intervals only: sub-row key
  "color": "#fdf9d4",
  "status": "disputed",            // accepted | disputed | proposed | rejected | inapplicable
  "conf": "dated",                 // vocab.confidence id
  "src": ["smithsonian"],
  "note": "…"
}
```

### `series`
```json
{
  "kind": "series",
  "unit": "people",
  "yScale": "log",
  "yDomain": [1000, 10000000000],
  "coverage": [["300 ka", "now"]],
  "samples": [ { "t": "12 ka", "lo": 1000000, "hi": 10000000 } ]
}
```
`lo`/`hi` here are **value** bounds, not date bounds. Outside `coverage` the
renderer draws the explicit "no data — not zero" region. That distinction is
load-bearing: a population line that runs to the left edge at a low value tells
a lie about what is known.

*Not yet supported and needed:* per-sample date uncertainty, and multiple
competing series for the same quantity (e.g. HYDE vs Maddison vs McEvedy) shown
as separate lines rather than merged into one fake consensus band.

### `stack`
Composition over time. Bands with keyframes `[time, weight]`, normalised to 1 at
each pixel column.

### `schemes`
The periodisation comparison. Each scheme has rows, each row is a region or
tradition, each row has intervals. A row may carry `"appliesTo": false` and an
item with `"status": "inapplicable"`, which is how Australia appears under the
Three-age system — visible, hatched, and labelled as a category error rather
than quietly omitted.

### `evidence`
Step values for how much is actually known per era. Currently asserted by hand.
**This should be computed** — see `SOURCES.md`.

## 4. Lanes

Lanes are declared in data:

```json
{ "id": "hominins", "label": "Hominin species", "dataset": "hominins",
  "encoding": "intervals", "height": 148, "minSpan": 0, "maxSpan": 25000000 }
```

`minSpan` / `maxSpan` are the visible time-span window in which the lane exists,
in years. This is the semantic zoom. `maxSpan: null` means always. A lane
outside its window does not fade to a hint of itself — it is gone, because a
regional strip at 100 Ma is not faint, it is meaningless.

## 5. Provenance

Every dataset carries `src` (ids into the `sources` registry), or
`defaultSrc` inherited by its records, or `wouldUse` naming the source that
*should* supply it. The readout panel surfaces whichever applies, so a reader
tapping a bar can tell the difference between a figure with a citation and a
figure someone invented for layout.

`vocab.confidence` runs: measured, recorded, dated, estimated, modelled,
inferred, speculative, disputed, **fabricated**. The last one exists so that
placeholder content is self-declaring, and the build can count it. Nothing
tagged `fabricated` should survive to a public release, and the status line at
the top of the page names those lanes out loud.

## 6. Build

```
data/atlas.json  +  src/atlas.template.html  --build/build.py-->  deep-time-atlas.html
```

Authoring stays split so the data diffs cleanly in version control; the
deliverable is a single portable file. `build.py --strict` fails on validation
problems.

## 7. Known limits of this schema

- **No entity/dating separation.** "Bronze Age" appears three times under
  Three-age, once per region, with duplicated labels. It should be one entity
  with three regional datings. Worth fixing before regional coverage expands,
  and painful to retrofit after.
- **No source-level date provenance.** A record cites a source but not a page,
  table, or query. For anything contested that is not enough.
- **No versioning of contested values.** When a date is revised, the old value
  should be retrievable, because "the date changed in 2016" is itself one of the
  interesting facts this atlas could show.
- **Series cannot express competing reconstructions.** See above.
- **No spatial component at all.** Regions are text labels. Real regional
  coverage eventually wants geometry.
