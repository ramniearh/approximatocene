# Project notes

Background and current state, so a new session (human or Claude) can pick up without the earlier chat history. Keep this short and update it when something is decided.

## Purpose

- An interactive timeline of human history and deep time, with one commitment above all: **uncertainty is drawn, not hidden.**
- Uses: light use in undergraduate classes (showing a view, stepping through a story), a home page to share the project, and something to tweak for fun.
- Scale of ambition: informal. Earlier rounds of planning went deep into specifications (staged roadmaps, schema hardening, per-source dossiers). That was more than this project needs. The aim now is a page that works and gets better a little at a time.

## History in brief

- **v0.1–v0.2 (Aug 2026):** a structural pilot, a single page that draws everything from one data file. A review found real bugs (the time axis showed only one label, a source was cited that had never been loaded, and some lanes were invented without saying so) and produced a long technical plan. Most of that plan has been set aside. The original data-format and sources notes are in `docs/reference/` for background.
- **v0.3 (Nov 2026):** the current page, which became the project's home page. It has four tabs:
  - **Human time** (opens first): the last million years. One population line with a fuzzy range around it; markers for fire, language, out of Africa, the end of the last ice age, farming, first cities, writing and the industrial revolution; strips for geological time and hominin species underneath.
  - **Full atlas:** every lane of the pilot, from the formation of the Earth to now.
  - **Stories:** five short step-through stories for class (how to read the chart, periodisation schemes, other human species, people and the ice, the Anthropocene vote). They have arrow-key navigation and a full-screen button.
  - **About:** what the page is, how uncertainty is drawn, and the list of sources (registered but none loaded yet).
- Several bugs from the pilot review were fixed along the way: axis labels, sources no longer claimed before they are loaded, the "no data" region, steadier dragging, and text contrast.

## Decisions so far (Human time tab)

- The view can zoom in freely but never out past about 1 million years.
- Time axis: logarithmic by default, with a linear option. Population axis: logarithmic by default, with a linear option. On linear the curve goes nearly vertical at the end, which is intended.
- Clicking a marker shows everything from just before that marker up to the present.
- Population: the line is Our World in Data's central estimate from 10,000 BCE (dashed while it is a HYDE reconstruction). Before that only a placeholder haze is shown, with no line (see "Sourced data on the page").
- Before 300,000 years ago there is no population estimate. A faint dotted line runs low there to say "small, thousands to tens of thousands", and the page labels it as not a figure.
- Geology strip: Pleistocene and Holocene, with the Early, Middle (Chibanian) and Late Pleistocene, the three Holocene ages, and a hatched "Anthropocene?" for the 2024 rejection.
- The hominin strip shows species (several of them contested), not subspecies. Disputed ones are hatched.
- Placeholder warnings stay visible until real data replaces them.

## Data status

- **Most values are placeholders** written from memory to make the page work. The exceptions are geology, hominin species and population from 10,000 BCE (see "Sourced data on the page").
- Fixed: the population list had two samples at the same date ("5000 b2k" and "3000 BCE" are the same year). The first was moved to 7000 b2k (5000 BCE), which seemed to be the intent. This needs confirming when real figures go in.
- Some lanes in the Full atlas are invented outright and labelled that way. Energy per person has made-up numbers (temperature was sine waves until Nov 2026; it is now sourced). The political-forms lane is a speculative impression.
- Sources to start with, when real data goes in: Our World in Data or HYDE 3.3 for population, the International Chronostratigraphic Chart for geological dates, and the Smithsonian Human Origins pages for hominin species. Candidate sources are listed in `docs/reference/SOURCES.md` and in `data/atlas.json` under `sources`.

## Reference datasets

- Decided Nov 2026: sourced reference data goes in `data/reference/` as plain CSV files, one per dataset, with a `source` column on every row. Values are copied as the source gives them (including `~` and `±`), not cleaned up. The page doesn't read them yet.
- `geologic_time_ics.csv`: all 178 units (eons to stages) from the ICS chart v2024/12, read from stratigraphy.org/chart on 2026-11-20. Ages are in millions of years ago (Ma); `top_ma` is the younger boundary and `base_ma` the older one. The chart is not fully consistent with itself in a few places (for example, the base of the Neogene is 23.03 but the top of the Paleogene is 23.04), and the file keeps those as published.
- `hominin_species_smithsonian.csv`: the 21 species on the Smithsonian Human Origins species list, read 2026-11-20. `when_lived` is the Smithsonian's own wording, and `oldest_ya` / `youngest_ya` are those same numbers in years ago. Where the page gives a single date ("about 4.4 million years ago"), both columns hold it. Two species have no discovery year on their page, so that cell is blank.
- Three groups shown on the Human time tab are not on the Smithsonian list and have no sourced dates yet: Denisovans, *H. antecessor* and *H. luzonensis*. A second source would be needed for them.
- `world_population_owid.csv`: world population from Our World in Data's long-run series (`population_historical`, last updated by OWID 2024-07-15, read 2026-11-20). There are 261 rows, from 10,000 BCE to 2023. Years are as OWID gives them: negative means BCE, and there is a year 0. OWID stitches three sources together, and the `underlying_source` column says which applies to each row: HYDE 3.3 before 1800, Gapminder v7 summed over countries for 1800–1949, and UN WPP 2024 from 1950. OWID warns of possible breaks where the sources meet. Citation: HYDE (2023); Gapminder (2022); UN WPP (2024), with major processing by Our World in Data.
- The OWID series is a single central estimate with **no range**. Before 10,000 BCE it has nothing. The haze on the Human time tab can't come from this file. A range would need a second source, such as rival reconstructions (open question).
- `polities_cliopatria.csv` and `largest_polity_by_century_cliopatria.csv` are made from Cliopatria v0.2.1 (Seshat Global History Databank, CC BY 4.0, released 2026-10-03; github.com/Seshat-Global-History-Databank/cliopatria). The source is a 46 MB zipped map file. It is not in the repo; the CSVs are tables computed from it.
  - The polity list has one row per polity (1,587 in all) with its first and last year, its largest mapped area in km² and when that was, and its Wikipedia, Wikidata and Seshat links. The 50 "relations" (alliances and similar) are left out.
  - Names in brackets, such as "(British Empire)", are Cliopatria's composites, made up of member polities that are also listed on their own. They are marked `composite`.
  - `gaps_in_coverage` means Cliopatria has no rows for some years between a polity's first and last year.
  - The largest-polity table checks every 100th year from 3400 BCE to 2000 CE, plus 2024 (there is no year 0). It gives the polity with the largest mapped area and how many polities Cliopatria maps that year. **It can miss short peaks:** the Mongol Empire (about 27 million km² around 1280, ending 1293 in Cliopatria) falls between samples. Checking every year would fix that if it matters.
  - Areas are the area of the drawn borders, rounded to whole km². Cliopatria itself says borders, names and dates are one version among disputed ones. "Polities present" counts what Cliopatria maps, which is far from every polity, especially in early periods.
- **Climate and carbon (read 2026-11-21).** These are for the Temperature lane, plus a possible carbon lane (Eduardo asked for one). Ages stay in each source's own units, given in the column name: `age_ma`, `age_ka`, `age_yr_bp1950` (years before 1950, *not* before 2000 or 2023), or `year_ce`. Values are copied as published, and blank means the source has no value. All are open (CC BY or public NOAA data).
  - `benthic_d18o_cenogrid.csv`: CENOGRID (Westerhold et al. 2020, *Science*), 0–67.1 Ma, 23,629 rows. It is the S34 table (binned splice plus LOESS-smoothed curves), not the raw 24,000-sample splice. **This is δ¹⁸O of deep-sea shells, not temperature.** It mixes deep-ocean temperature with ice volume, and higher δ¹⁸O means colder or more ice. The source gives no temperature conversion and none was applied. 3.8 MB.
  - `benthic_d18o_lr04.csv`: the LR04 stack (Lisiecki & Raymo 2005), 0–5,320 ka in 1–5 kyr steps, with the source's standard error. Also δ¹⁸O, not temperature. It overlaps CENOGRID for the last 5.3 Myr; the two use different age models and calibrations.
  - `antarctic_temperature_epica.csv`: EPICA Dome C (Jouzel et al. 2007), 0–802 ka, on the EDC3 age scale. Temperature is the source's estimate of the **difference from the last 1,000 years at Dome C, Antarctica**. It is local, not global, and polar swings are roughly twice the global ones. The top few samples have no deuterium or temperature value.
  - `global_temperature_pages2k.csv`: PAGES 2k Consortium (2019) global mean temperature, 1–2000 CE, with the median and 2.5–97.5% range of the 7,000-member ensemble, raw and 31-year filtered, in °C relative to 1961–1990. The instrumental target (Cowtan & Way) runs to 2017.
  - `co2_ice_cores_bereiter.csv`: the Antarctic CO₂ composite (Bereiter et al. 2015), from 2001 CE back to 805 ka, in ppm with 1σ. The `underlying_record` column says which ice core each row is from, following the source's own list. Where that list overlaps (105–115 ka) or skips (611–612 ka), the column says so instead of picking. Ages are AICC2012 except for Law Dome, WAIS and Siple Dome.
  - `co2_mauna_loa_noaa.csv`: NOAA GML / Scripps Mauna Loa annual means, 1959–2025 (file created 2026-11-19). The last year may still be revised, and Dec 2022–Jul 2023 was measured at Maunakea after the eruption.
  - `co2_proxies_cenco2pip.csv`: CO₂ before the ice cores, as **individual proxy estimates, not a curve** (Eduardo's choice, Nov 2026). From the CenCO2PIP Consortium (2023, *Science*, doi:10.1126/science.adi5177) data product v1.02 (Zenodo 14537923, Dec 2024, CC BY 4.0), which is 137 spreadsheets, one per study. There are 6,088 estimates from 0 to 455 Ma (most are Cenozoic), each with its age and CO₂ uncertainty, proxy type, study DOI and the CenCO2PIP flags.
    - `category` is the project's own grading. **1** means high quality with the uncertainty fully worked out; **2** means high quality, but the uncertainty is not yet fully constrained; **3** means an outdated method or an uncertainty that can't be fully quantified. `category_reason` gives their wording. The project also marks values as superseded or quarantined. 3,712 estimates are category 1–2 and neither superseded nor quarantined. A page lane would most likely show only those, but that is a choice still to make.
    - Rows with no CO₂ value (1,815, marked "NA" in the source) are left out. The names and emails of the people who entered the data are left out too.
    - Kept as published, though they look odd: 9 estimates are zero or negative CO₂ (paleosol and boron studies). Some DOIs in a few files count upward row by row (for example `10.1130/G36467.38`), which looks like an Excel fill error in the source. The `product_file` column still identifies the study.
    - One fix: in `boron_isotopes_guillermic_2022` the first few cells of each row sit two columns to the left of their headers. Proxy, author and year were read from where they actually are. Age and CO₂ were already in place.
    - CenCO2PIP's own smoothed 66-million-year curve (in the paper's supplement) is not used.

## Sourced data on the page

- **Geology (Nov 2026):** both the Human time strip (`HGEO` in `src/page.html`) and the Full atlas geology lane (`geo` in `data/atlas.json`) now take their dates from `geologic_time_ics.csv`. Where the ICS gives "±", the bar end fades across that range. The Human time strip uses the chart's own names (Gelasian, Calabrian, Chibanian, Upper Pleistocene) instead of "Early/Middle/Late Pleistocene". Years that the chart doesn't give (when units were ratified, and so on) were removed from the period notes. The Anthropocene is not on the chart, so it stays hatched and is marked as an unsourced placeholder. The ICS source now shows as "ingested", and the status lines on every tab say geology is sourced and the rest isn't.
- **Hominin species (Nov 2026):** the species lane (`hominins` in `data/atlas.json`, shared by Full atlas and Stories, and used by the Human time strip) now holds the 21 Smithsonian species, with dates from `hominin_species_smithsonian.csv`. Each species' details box quotes the Smithsonian's wording. Notes kept from earlier lost any years no source gives.
  - The Ardipithecus and Paranthropus genus bars are gone; their species replace them.
  - Five species are labelled and drawn full size: *Au. afarensis*, *P. boisei*, *H. erectus*, *H. neanderthalensis* and *H. sapiens*. This is an editorial pick (agreed with Eduardo), and the About tab says so. The rest are thin and faint, and show their details on tap.
  - Bars are solid between the Smithsonian's dates and then fade over a fixed 12 pixels past each end (none at "now"). This is a reminder that species outlive their fossils, not data; the About legend and each details box say so.
  - Earlier "disputed" flags (hatching) were kept for *Sahelanthropus*, *H. habilis* and *H. heidelbergensis*. They are editorial judgments, not from the source.
  - Denisovans, *H. antecessor* and *H. luzonensis* keep their placeholder dates and say "No source yet. Placeholder."
- **Population (Nov 2026):** from 10,000 BCE to 2023 the population line (`population` in `data/atlas.json`, used by all three chart tabs) is the OWID series from `world_population_owid.csv`, all 261 rows, each tagged with its underlying source. OWID gives no range, so there is no haze over that stretch. Instead the line is **dashed where the figures are HYDE 3.3 model reconstructions (to 1790) and solid from 1800** (Gapminder, then UN). Both choices were Eduardo's.
  - Hovering shows the nearest published figure and its year and source, not an interpolated value.
  - **Kept, at Eduardo's choice:** the placeholder range from 300,000 years ago to 10,000 BCE (`population.placeholder`). It is drawn as haze only, with no line, and labelled "placeholder range, not sourced". Before 300,000 years ago it still says "not estimated".
  - **"Now" is fixed at 2023** (Nov 2026, Eduardo's call), the last year in the OWID series, so the line reaches the right edge. "Years ago" counts back from 2023 everywhere on the page, and the About tab says so. If newer population data is added, move `NOW` in `src/page.html` with it.
  - Wording for the unsourced stretches (Eduardo's, deliberately vague for now): 300,000 years ago to 10,000 BCE is "probably a range of guesses (not sourced)"; before 300,000 years ago it's "not estimated. Presumably there were some humans here and there". The old "thousands to tens of thousands" text is gone. The faint dotted line is still drawn at the same low height, though, so it still hints at a size.
  - OWID's year 0 is entered as "0 CE", so its BCE years are read at face value (−1000 → 1000 BCE). At this scale a one-year shift wouldn't show.

- **Climate and CO₂ (Nov 2026, Full atlas only).** The sine-wave "Temperature" lane is gone. In its place are two lanes, with data in `climate` and `co2` in `data/atlas.json`, copied from the reference CSVs. Large series are stored as compact `rows` with one `ageUnit` per block, and `build.py` stops if a block has no unit.
  - **Climate** is a set of separate strips, one per record, each on its own fixed vertical scale. They are not joined (Eduardo's choice). The strips are CENOGRID deep-sea δ¹⁸O (the source's LOESS line, flipped so up = warmer or less ice, and captioned "not a temperature"), EPICA Dome C Antarctic temperature, and PAGES 2k global temperature (the source's 31-year smoothed median with its 95% range, plus the yearly instrumental line to 2017). A strip shows only when at least 40 px of its time span is in view. Outside a record's span the strip is greyed "no data — not zero". LR04 is not drawn because it overlaps CENOGRID.
  - **Carbon dioxide** is on a log ppm scale. CenCO2PIP proxy estimates appear as dots with their published uncertainty bars: filled for category 1, hollow for category 2. Category 3, superseded and quarantined estimates are not shown (Eduardo's choice), which leaves 3,712 of 6,088. The Bereiter ice-core composite is a line, and Mauna Loa (1959–2023) is a darker line. Proxy CO₂ is rounded to 0.1 ppm on the page. Proxy ages in ka are read as before 2000; the 50-year offset can't show.
  - Hovering shows the nearest published value and its source, not an interpolated value. When fewer than about 40 samples are in view, each sample is marked with a dot, so a straight stretch of line isn't read as data.
  - Long series are drawn as one min–max column per pixel, so no peaks are dropped. The data makes the page about 836 KB, up from about 155 KB.
  - LR04, the Human time tab and Stories are unchanged. On phones the lane captions are cut short, but tapping a lane gives the full explanation.

## Open questions (Eduardo's call)

- Should the political-forms lane stay? Nobody has these numbers. The options are to keep it as a clearly labelled impression, to replace it with something countable (such as the size of the largest polity over time), or to drop it. A sourced "largest polity over time" now exists in `data/reference/` (from Cliopatria), so the countable option is ready if wanted.
- Population: Our World in Data is now on the page (Nov 2026). Still open: whether to add rival reconstructions to show where they disagree and to give the line a range, and what source (if any) to use for 300,000 years ago to 10,000 BCE, where the placeholder haze remains.
- **To revisit: population before 10,000 BCE.** Both unsourced stretches are left vague on purpose for now. Decide later (1) whether the "range of guesses" from 300,000 years ago to 10,000 BCE gets a real source (for example published Palaeolithic population estimates or effective-population-size studies, which measure something different), stays as an openly labelled guess, or is removed, and (2) whether the dotted line before 300,000 years ago should go, since its height still suggests a size.

- Climate and CO₂: should the "People and the ice" or Anthropocene stories use the new lanes? And should category 3 CO₂ estimates ever be shown, for example faded?

## Ideas, not yet done

Suggested markers for Human time, held back for now:
- art and ornament (ochre engravings about 75,000 years ago; cave art about 45,000–50,000 years ago)
- settlement of Sahul and of the Americas (the Americas date is disputed)
- money: the unit of account in Mesopotamia versus Lydian coinage. Which date you mark is itself a theoretical choice.
- the Great Acceleration (about 1950)
- a claimed genetic bottleneck about 900,000 years ago. It is contested, and it measures breeding population, not head count, so it belongs as a marker and shouldn't bend the population line.

Other ideas:
- Eduardo's direction (Nov 2026): separate tabs for specific timelines or questions (for example one for humans and one for polities), alongside one big page with all of deep history. Build the reference datasets first, then restructure the tabs.
- more stories for class
- shareable links to specific views

*Drafted with AI assistance (Claude) from earlier project conversations.*
