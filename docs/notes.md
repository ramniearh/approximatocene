# Project notes

Background and current state, so a new session (human or Claude) can pick up without the earlier chat history. Keep this short and update it when something is decided.

## Purpose

- An interactive timeline of human history and deep time, with one commitment above all: **uncertainty is drawn, not hidden.**
- Uses: light use in undergraduate classes (showing a view, stepping through a story), a home page to share the project, and something to tweak for fun.
- Scale of ambition: informal. Earlier rounds of planning went deep into specifications (staged roadmaps, schema hardening, per-source dossiers). That was more than this project needs. The aim now is a page that works and gets better a little at a time.

## History in brief

- **v0.1–v0.2 (Aug 2026):** a structural pilot, a single page that draws everything from one data file. A review found real bugs (the time axis showed only one label, a source was cited that had never been loaded, and some lanes were invented without saying so) and produced a long technical plan. Most of that plan has been set aside. The original data-format and sources notes are in `docs/reference/` for background.
- **v0.3 (Nov 2026):** the current page, which became the project's home page. It follows the browser's light or dark setting; a ◐ button at the right of the tab row switches it, and the browser remembers the choice. It has four tabs:
  - **Human time** (opens first): the last million years. One population line with a fuzzy range around it; markers for fire, language, out of Africa, the end of the last ice age, farming, first cities, writing and the industrial revolution; strips for geological time and hominin species underneath.
  - **Deep time** (called "Full atlas" until Nov 2026): every row of the pilot, from the formation of the Earth to now. In these notes "lane" means a row of that chart; the page itself says "row".
  - **Stories:** five short step-through stories for class (how to read the chart, periodisation schemes, other human species, people and the ice, the Anthropocene vote). They have arrow-key navigation and a full-screen button.
  - **About:** what the page is, how uncertainty is drawn, and the list of sources, saying which are in use.
- Several bugs from the pilot review were fixed along the way: axis labels, sources no longer claimed before they are loaded, the "no data" region, steadier dragging, and text contrast.

## Decisions so far (Human time tab)

- The view can zoom in freely but never out past about 1 million years.
- Time axis: logarithmic by default, with a linear option. Population axis: linear by default since Nov 2026 (Eduardo), with a logarithmic option. On linear the curve goes nearly vertical at the end, which is intended.
- Clicking a marker shows everything from just before that marker up to the present.
- Population: the line is Our World in Data's central estimate from 10,000 BCE (dashed while it is a HYDE reconstruction). Before that only a placeholder haze is shown, with no line (see "Sourced data on the page").
- Before 300,000 years ago there is no population estimate. A faint dotted line runs low there to say "small, thousands to tens of thousands", and the page labels it as not a figure.
- Geology strip: Pleistocene and Holocene, with the Early, Middle (Chibanian) and Late Pleistocene, the three Holocene ages, and a hatched "Anthropocene?" for the 2024 rejection.
- The hominin strip shows species (several of them contested), not subspecies. Disputed ones are hatched.
- Placeholder warnings stay visible until real data replaces them.
- The marker buttons have a "Jump to:" label, and the first one reads "The whole million years" (Nov 2026).
- A "Fossil fuels" marker (button: "Fossil fuels overtake wood"), 1900–1910, shaded with no line (Eduardo, Nov 2026). Same calculation as the Deep time highlight: the decade in which coal, oil and gas together passed traditional biomass in OWID/Smil's ten-year figures.
- A last, slightly tongue-in-cheek marker, "Large language models" (2022, the public release of ChatGPT), says the page itself was drafted with one (Eduardo's idea, Nov 2026).

## Data status

- **Most values are placeholders** written from memory to make the page work. The exceptions are geology, hominin species, population from 10,000 BCE, and the Full atlas climate and CO₂ lanes (see "Sourced data on the page").
- Fixed: the population list had two samples at the same date ("5000 b2k" and "3000 BCE" are the same year). The first was moved to 7000 b2k (5000 BCE), which seemed to be the intent. This needs confirming when real figures go in.
- Some lanes in the Full atlas are invented outright and labelled that way. Energy per person had made-up numbers until Nov 2026 (it is now sourced from 1800; see below), and temperature was sine waves until Nov 2026 (also now sourced). The political-forms impression was replaced by the sourced largest-polity lane in Nov 2026.
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
  - The largest-polity table checks every 100th year from 3400 BCE to 2000 CE, plus 2024 (there is no year 0). It gives the polity with the largest mapped area and how many polities Cliopatria maps that year. **It can miss short peaks:** the Mongol Empire (about 27 million km² around 1280, ending 1293 in Cliopatria) falls between samples. Superseded by the yearly table below.
  - `largest_polity_by_year_cliopatria.csv` (Nov 2026) has the same columns, for every year from −3400 to 2024 (5,425 rows), computed from the same v0.2.1 map file (re-downloaded 2026-11-21). The map file does have a year 0, and years are kept as given. At every 100th year it matches the century table exactly. It catches the Mongol Empire (largest from 1216 to 1293, peaking at 27.4 million km² in 1279). The largest overall is "(British Empire)", 29.3 million km² in 1918. The lead changes hands 66 times. As before, composites in brackets compete with single polities.
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
  - *Ar. ramidus*, *K. platyops* and *Au. garhi* are tagged "estimated", not "dated" (Nov 2026). The Smithsonian gives each a single date with no range, and "dated" means a stated interval.
- **Population (Nov 2026):** from 10,000 BCE to 2023 the population line (`population` in `data/atlas.json`, used by all three chart tabs) is the OWID series from `world_population_owid.csv`, all 261 rows, each tagged with its underlying source. OWID gives no range, so there is no haze over that stretch. Instead the line is **dashed where the figures are HYDE 3.3 model reconstructions (to 1790) and solid from 1800** (Gapminder, then UN). Both choices were Eduardo's.
  - Hovering shows the nearest published figure and its year and source, not an interpolated value.
  - In the About sources table HYDE 3.3 shows as "used via Our World in Data", since its figures reach the page only through OWID.
  - **Kept, at Eduardo's choice:** the placeholder range from 300,000 years ago to 10,000 BCE (`population.placeholder`). It is drawn as haze only, with no line, and labelled "placeholder range, not sourced". Before 300,000 years ago it still says "not estimated".
  - **"Now" is fixed at 2023** (Nov 2026, Eduardo's call), the last year in the OWID series, so the line reaches the right edge. "Years ago" counts back from 2023 everywhere on the page, and the About tab says so. If newer population data is added, move `NOW` in `src/page.html` with it.
  - Wording for the unsourced stretches (Eduardo's, deliberately vague for now): 300,000 years ago to 10,000 BCE is "probably a range of guesses (not sourced)"; before 300,000 years ago it's "not estimated. Presumably there were some humans here and there". The old "thousands to tens of thousands" text is gone. The faint dotted line is still drawn at the same low height, though, so it still hints at a size.
  - OWID's year 0 is entered as "0 CE", so its BCE years are read at face value (−1000 → 1000 BCE). At this scale a one-year shift wouldn't show.

- **Climate and CO₂ (Nov 2026, Full atlas only).** The sine-wave "Temperature" lane is gone. In its place are two lanes, with data in `climate` and `co2` in `data/atlas.json`, copied from the reference CSVs. Large series are stored as compact `rows` with one `ageUnit` per block, and `build.py` stops if a block has no unit.
  - **Climate** is a set of separate strips, one per record, each on its own fixed vertical scale. They are not joined (Eduardo's choice). The strips are CENOGRID deep-sea δ¹⁸O (the source's LOESS line, flipped so up = warmer or less ice, and captioned "not a temperature"), EPICA Dome C Antarctic temperature, and PAGES 2k global temperature (the source's 31-year smoothed median with its 95% range, plus the yearly instrumental line to 2017). A strip shows only when at least 40 px of its time span is in view. Outside a record's span the strip is greyed "no data — not zero". LR04 is not drawn because it overlaps CENOGRID.
  - **Carbon dioxide** is on a log ppm scale. CenCO2PIP proxy estimates appear as dots with their published uncertainty bars: filled for category 1, hollow for category 2. Category 3, superseded and quarantined estimates are not shown (Eduardo's choice), which leaves 3,712 of 6,088. The Bereiter ice-core composite is a line, and Mauna Loa (1959–2023) is a darker line. Proxy CO₂ is rounded to 0.1 ppm on the page. Proxy ages in ka are read as before 2000; the 50-year offset can't show.
  - Hovering shows the nearest published value and its source, not an interpolated value. When fewer than about 40 samples are in view, each sample is marked with a dot, so a straight stretch of line isn't read as data.
  - Long series are drawn as one min–max column per pixel, so no peaks are dropped. The data made the page about 836 KB, up from about 155 KB; with the later lanes it is about 1 MB (Nov 2026).
  - LR04, the Human time tab and Stories are unchanged. On phones the lane captions are cut short, but tapping a lane gives the full explanation.

- **Largest polity (Nov 2026, Full atlas).** This replaces the "political forms" stack, a Histomap-style impression of the share of people under bands, tribes, chiefdoms and so on, with no numbers behind it; that impression is gone from the data. The lane (`largestPolity` in `data/atlas.json`) draws the yearly table as a log km² line, with a bar underneath showing which polity held the lead, in alternating shades. Hovering gives the polity, its area, the year and how many polities Cliopatria maps that year. Before 3400 BCE it says "no data — not zero". The caption says area is not population and borders are disputed. The Stories scene that used the old lane as its example of an invented lane now uses the energy lane, which is still invented.

- **Polity population (Nov 2026, Full atlas, Eduardo's request and choice of source).** This is a new lane just below "Largest polity" (`polityPop` in `data/atlas.json`).
  - It shows every polity population estimate in Seshat's Polaris2026 release (`polity_population_seshat.csv`, below) exactly as published. Where Seshat gives a low and a high figure, the mark is a vertical bar; where it gives one figure, a dot. Estimates tied to a year are drawn at that year. Estimates Seshat gives for a polity as a whole are drawn as faint bars across the polity's dates. Disputed estimates are hatched. No line joins the estimates, and nothing is interpolated.
  - Seshat covers a sample of polities, not all of them. So the top edge of the marks is "largest in Seshat's sample". The caption and hover say so. In 1938, for example, Seshat's largest is the British Empire (531 million), and China isn't in its sample for that year.
  - From 1950 a dark line shows the most populous country (`largest_country_population_owid.csv`): China, then India from 2022.
- `polity_population_seshat.csv` (read 2026-11-21) holds all 577 `polity_population` rows from Seshat's Polaris2026 spreadsheet (github.com/Seshat-Global-History-Databank/build_polaris_dataset), with each polity's name, region and dates from the same file.
  - Licence: Seshat's terms put its public data under **CC BY-SA 4.0**, so anything built from it must keep that licence. The 2020 Equinox release on Zenodo is CC BY, but it has fewer estimates (395).
  - 118 rows have no number and are not drawn. 282 have no year, meaning they apply to the whole polity. 16 are marked disputed and 4 uncertain.
  - Two rows have their high figure entered first (Early Illinois Confederation; East Roman Empire). They are kept as given, and the page draws the range between the two figures.
- `largest_country_population_owid.csv` (read 2026-11-21): for each year 1950–2023, the country with the largest population in OWID's `population_historical` series (UN WPP 2024 from 1950). Only 3-letter country codes count, so aggregates are excluded.

- **Life (Nov 2026, Full atlas, Eduardo's request).** This is a new lane after carbon dioxide (`life` in `data/atlas.json`).
  - **Bars:** the number of animal (Metazoa) genera known from fossils in each geological stage, from 538.8 Ma, taken from the Paleobiology Database's own diversity tool (`animal_genus_diversity_pbdb.csv`, below). Each bar is the range-through count, the sum of PBDB's X_Ft, X_bL, X_FL and X_bt fields (Foote 2000). Hover also gives the number of genera actually found in that stage and the number of fossil records behind it. The caption and note say this counts what has been found and recorded, not everything that lived. Before 538.8 Ma the lane says "no data — not zero".
  - **Shaded marks:** the five largest mass extinctions, at ICS dates already in `geologic_time_ics.csv`. End-Ordovician spans the Hirnantian stage. Late Devonian is at the Frasnian–Famennian boundary. End-Permian, end-Triassic and end-Cretaceous are at the Permian–Triassic, Triassic–Jurassic and Cretaceous–Paleogene boundaries. Pairing each extinction with its boundary is a standard convention, not part of the ICS chart, and each mark's note says so.
  - **Early milestones (top row, Nov 2026, sources approved by Eduardo):**
    - Signs of life in hot-spring deposits, "ca. 3.48 Ga" (Djokic et al. 2017). The paper gives no error range, so the mark is a single line.
    - The Great Oxidation Event (Gumsley et al. 2017): onset "between ca. 2,460 and 2,426 Ma", with oscillations "until ≤2,250–2,240 Ma". It is drawn as a span whose two ends fade across those ranges. No midpoint is invented; the hover quotes the paper's wording.
    - The oldest multicellular eukaryotes, "~1635 Ma" (Miao et al. 2024). The fade is the ±6.9 Myr error of the ash-bed date 40 m above the fossils.
  - **Living groups (bottom rows):** 12 crown groups from Benton et al. 2015 (Palaeontologia Electronica 18.1.1FC): animals, bilaterians, arthropods, molluscs, vertebrates, jawed vertebrates, tetrapods, amniotes, mammals, modern birds, primates and the chimpanzee–human split. Each bar fades from the paper's soft maximum to its minimum age (the oldest fossil firmly in the living group), with a thin line from there to now. Crown groups start later than their earliest relatives, and the hover says so. The paper text was read from its PDF with pypdf in a scratch folder (not a project dependency).
  - All values, with the paper's own wording, are in `data/reference/life_milestones.csv`. The four papers are registered as sources (`djokic2017`, `gumsley2017`, `miao2024`, `benton2015`). Djokic and Miao are CC BY 4.0, Gumsley is PNAS open access, and Benton is open access. Only dates are used, with citations.
  - Still missing: plants (land plants, flowering plants), which Benton et al. does not cover, and the oldest *single-celled* eukaryotes.
  - **Not used: PBDB's first-appearance dates for major groups.** They are computed from every record in the database, misidentified ones included, so several are badly off: flowering plants (Angiospermae) in the Carboniferous (about 359–347 Ma), amniotes in the Devonian, and land plants (Embryophyta) in the Ediacaran. Benton et al. 2015 is used instead for animals (above); plants still need a curated source.
- `animal_genus_diversity_pbdb.csv` (read 2026-11-21) is PBDB data service 1.2, `occs/diversity` with `base_name=Metazoa`, `count=genera` and `time_reso=stage`, using the default settings (no `recent`, so living genera are not extended to the present). It has 99 stages, kept exactly as PBDB returns them, including its own stage boundaries, which differ slightly from ICS 2024 in places. The Přídolí stage has no row. The last Holocene stages have almost no records (Greenlandian has one), so their counts are tiny. The data service gives the licence as **CC0**, not CC BY as first registered. With `base_name=Eukaryota`, PBDB returned *fewer* genera than for animals alone, so that query was not used.

- **Energy per person (Nov 2026, Full atlas, Eduardo's choice of "option B").** The invented Morris-shaped band from 300,000 years ago is gone. The lane (`energy` in `data/atlas.json`) now shows world energy use per person, 1800–2023, in kWh per person per year (the source's unit, not converted to kcal).
  - It is **calculated here**, not published: OWID's world energy use by source (all ten sources, including traditional biomass) divided by OWID's world population for the same year (`world_population_owid.csv`), rounded to whole kWh. OWID's own per-person series was not used because it leaves out traditional biomass, which was 98% of the total in 1800, half in 1900 and 6% in 2023.
  - Before 1965 the figures are Vaclav Smil's estimates (2017, *Energy Transitions*) at ten-year steps, so the line is dashed there. From 1965 they come from the Energy Institute's Statistical Review (2026), except traditional biomass, which is Smil's World-only estimate and which OWID holds at its 2015 value from 2016 on. No range is given, so the line is faded throughout. Hover shows the nearest figure, not an interpolated one.
  - It counts fuels and electricity, not food or animal feed, so it is not "energy capture" in Ian Morris's sense; the caption says so. Before 1800 the lane says "no data — not zero", and the lane shows only when at least 40 px of 1800–2023 is in view.
  - Rough values: about 5,750 kWh in 1800, 7,400 in 1900, 11,200 in 1950 and 21,300 in 2023.
  - The Stories scene that used this lane as its example of an invented lane now uses the regions lane. The energy lane still appears in the Anthropocene story (1720 to now).
- **Radiocarbon (read 2026-11-24, for the evidence row).** Neither raw input is in the repo.
  - `radiocarbon_counts_p3k14c.csv` has one row per 500 calendar years, from 0 to 55,000 cal BP (years before 1950). It gives the number of archaeological radiocarbon dates, in total and by continent. It was made by `make_radiocarbon_counts.py`, a plain-Python script, from two inputs:
    - p3k14c version 2022.01: `p3k14c_scrubbed_fuzzed.csv` (179,689 dates), taken from the authors' Zenodo archive 5597795 (`people3k/p3k14c-1.0.0.zip`, 35.9 MB). It is also on tDAR, but that copy needs a login.
    - IntCal20, copied as published to `intcal20.csv`.
  - How dates are calibrated: each date is calibrated on a 5-year grid, with variance equal to lab error² plus curve error². Each date then counts once in total, shared across the bins its calibrated range covers. Counts are expected values, rounded to 0.1.
  - IntCal20 is used for every date. Strictly, southern-hemisphere dates need SHCal20 and shells need Marine20; at 500-year bins this shifts little.
  - Skipped: 382 dates younger than the curve (modern) and 31 older than it.
  - Checks: 10,000 ± 50 radiocarbon years calibrates to a median of about 11,480 cal BP, and 40,000 ± 500 to about 43,270.
  - Licence: the paper is CC BY 4.0. The archive's licence file covers only its code (MIT), and the tDAR data licence was not checked.
  - p3k14c has **no Australian dates older than 15,000 radiocarbon years**. Europe and North America hold about 79% of all dates.
- `highlight_dates.csv` (Nov 2026): one row per Deep time highlight, with the date as the source gives it and the citation (see "Highlights" below).
- `world_energy_owid.csv` (read 2026-11-22): the 78 World rows (1800–2025) of OWID's `global-energy-substitution` chart, in TWh, ten columns as published, with an `underlying_source` column. OWID's metadata contradicts itself on biomass (the chart note says it is included; the column note says it is not part of "total energy supply"); the World rows do carry it as its own column.

- **No stated uncertainty is not certainty (Nov 2026, Eduardo).** The new lanes had drifted toward false certainty: uncertainty was drawn only where a source published numbers for it. The rule now: where a source gives no uncertainty, the mark is dashed, faded or soft-topped, never crisp. The About legend explains this.
  - Dashed: the largest-polity line, the UN "most populous country" line, the extinction marks, and milestones with no published range (early life).
  - Faded: the CENOGRID and EPICA lines (no error band or age uncertainty in the files) and the milestone spans.
  - Soft-topped: the fossil diversity bars.
  - Confidence tags corrected: extinctions and the Benton groups are now "estimated" (they had been tagged "dated"), and the milestones "inferred" (also previously "dated"), with a note that each is one paper's dating.
  - The UN line's note says India has held no census since 2011, so the 2022 crossover with China is uncertain.
  - Lanes that already draw a published range (PAGES 2k, CO₂ proxies, Seshat ranges, Benton soft maxima) are unchanged.
  - **Applied everywhere (Nov 2026, Eduardo).**
    - The population line on all three chart tabs is faded throughout, because OWID gives no range. It is still dashed where HYDE's figures are model reconstructions. This replaces the earlier "solid from 1800".
    - Species bars on both tabs: the fixed 12 px fade now straddles each Smithsonian date (it starts 12 px outside and reaches full strength 6 px inside), instead of starting at the date. The Smithsonian gives no range for these dates.
    - Faded: Seshat estimates given as a single figure, CO₂ proxy estimates published with no uncertainty, and the PAGES 2k instrumental line.
    - Geology is unchanged. Every boundary the ICS chart marks as approximate (~) also has a ± range, which the page already fades across. The rest are boundaries the chart gives as defined values.
    - Placeholder lanes (energy, regions, periodisation, evidence, Human time markers) are unchanged; they are already labelled as unsourced. The highlights were sourced later (see below).

- **What has been dated (Nov 2026, Deep time; formerly "What we actually know").** The hand-drawn steps are gone. The row (`evidence` in `data/atlas.json`) now shows archaeological radiocarbon dates per 500 years from `radiocarbon_counts_p3k14c.csv`, calibrated with IntCal20. Eduardo chose calibration (over raw radiocarbon years) and "hard to say" before about 50,000 years (over keeping the hand-drawn steps as labelled opinion).
  - Drawing: bars on a log scale (10 to 10,000), soft-topped because the counts carry no stated uncertainty. Before 50,000 cal BP and after 1950 the row shows the usual "hard to say" shading. Hover gives the number of dates and each continent's share.
  - The caption and note say it is a record of archaeology, not of people: it reflects excavation, funding and survival.
  - The count falls in the last few thousand years because radiocarbon is less needed once there are written records, not because less is known. On a log axis, the stretch from 1950 to now takes up a lot of the row's width as "hard to say".
  - Also changed: the Writing highlight no longer says the strip "steps up" there; the "How to read this chart" story describes the new row; and the story status line counts it as sourced.

- **Highlights (Nov 2026, Deep time, Eduardo approved the recommended options).** All seven overlays in `overlays.highlights` now cite a source in their details box; values and wording are in `data/reference/highlight_dates.csv`.
  - Holocene: 11700 b2k (ICS). The old unused, unsourced "fuzz: 200 yr" is gone.
  - Out of Africa: 60,000–40,000 years ago (Bergström 2021), matching Human time. Soft edges, no line.
  - Last Glacial Maximum: 26.5 ka (no range given, so soft) to 20–19 ka (Clark 2009). The unsourced "sea level roughly 120 m lower" became "far lower".
  - Writing: fades in across Uruk IV, 3350–3200 BCE (CDLI), no line, then runs to now.
  - Agricultural revolution: starts across 12,000–11,000 BP and ends softly at 4,200 BP, the end of the second wave of domestication in Larson et al. 2014, *PNAS* 111:6139 (main text and figure captions read; per-centre dates in the SI not read). It names at least 11 independent centres. The Human time "Farming" marker is still a placeholder; this source could serve it too.
  - Fossil fuel era: 1900–1910 CE, **calculated here** from `world_energy_owid.csv`: the decade in which coal, oil and gas together passed traditional biomass (Smil's ten-year estimates).
  - Toba: 73.88 ± 0.32 ka (Storey et al. 2012, *PNAS* 109:18684), with a line at the date and a fade across 1σ. The note cites Mark et al. 2014 (75.0 ± 0.9 ka) and Smith et al. 2018 (*Nature* 555:511: people kept living at two South African coastal sites through it). Not used: a search summary mentions a later Mark et al. 2017 age of 73.7 ± 0.3 ka; unverified.
  - Drawing: shading now fades across each published range. Where a source gives a figure with no range (`"soft": true` in the data), the edge fades over 16 px. Dashed lines appear only where the source gives a central figure. Labels stay clickable when pushed away from a narrow span at the edge.

## Open questions (Eduardo's call)

- Political forms: decided (Nov 2026, Eduardo), replaced by "largest polity by mapped area, every year". Still open: should composites such as "(British Empire)" count, or only single polities? The population lane uses Seshat (decided Nov 2026).
- Population: Our World in Data is now on the page (Nov 2026). Still open: whether to add rival reconstructions to show where they disagree and to give the line a range, and what source (if any) to use for 300,000 years ago to 10,000 BCE, where the placeholder haze remains.
- **To revisit: population before 10,000 BCE.** Both unsourced stretches are left vague on purpose for now. Decide later (1) whether the "range of guesses" from 300,000 years ago to 10,000 BCE gets a real source (for example published Palaeolithic population estimates or effective-population-size studies, which measure something different), stays as an openly labelled guess, or is removed, and (2) whether the dotted line before 300,000 years ago should go, since its height still suggests a size.

- Climate and CO₂: should the "People and the ice" or Anthropocene stories use the new lanes? And should category 3 CO₂ estimates ever be shown, for example faded?

## Markers and extra species: sources (approved by Eduardo, Nov 2026, now on the page)

Read from abstracts, publisher pages and summaries, not full papers. Each marker and species now cites its source in its details box, and all are registered in `data/atlas.json` under `sources`. Where a source gives a window and no central date (Out of Africa, writing, the industrial revolution, the start of deglaciation), no line is drawn: only the shaded window. Farming and first cities are still placeholders; language still has no source.

Changes against the earlier placeholders: Out of Africa is now 60,000–40,000 years ago (was 90,000–40,000); *H. antecessor* is the TD6 tooth's date range, 949,000–772,000 (was 1.3 million–770,000); Denisovans are 194,400–122,700 to 76,000–52,000 (Denisova Cave only); *H. luzonensis* 67,000–50,000 as minimum ages. The IUGS statement of 20 March 2024 (read from its PDF) confirms the rejection; the 1952 start of the proposal is from news reports.

Original list as found:

- *H. luzonensis*: Détroit et al. 2019, *Nature* 568:181–186. Callao Cave fossils, minimum ages of 67,000 (foot bone) and 50,000 (tooth) years, by uranium-series. A later re-examination (reported by the Natural History Museum, London) suggests they may be much older, perhaps 130,000+; not drawn, but a good case for "dates moving over time".
- *H. antecessor*: Duval et al. 2018, *Quaternary Geochronology* 47:120–137 (doi:10.1016/j.quageo.2018.05.001). TD6 tooth, 772,000–949,000 years ago (ESR plus palaeomagnetism). The current placeholder reaches back to 1.2 million years, which this does not support.
- Denisovans: Douka et al. 2019, *Nature*. Oldest Denisova Cave fossil about 195,000 years ago; youngest 52,000–76,000. (Jacobs et al. 2019, same issue, dates the cave sediments rather than the fossils.)
- Anthropocene: rejected by the Subcommission on Quaternary Stratigraphy in March 2024 (reported as 12 against, 4 for, 2 abstaining), part of the International Union of Geological Sciences (IUGS); the proposed start was 1952 (Crawford Lake). Still need the IUGS's own statement rather than news reports.
- Control of fire: Berna et al. 2012, *PNAS* 109:E1215 (Wonderwerk Cave, burning about 1.0 million years ago); Roebroeks & Villa 2011, *PNAS* 108:5209 (habitual use in Europe from about 400,000–300,000 years ago). Contested by Sandgathe et al. 2011, who argue for much later habitual use.
- Out of Africa: Bergström et al. 2021, *Nature* 590:229 (review). Worldwide spread about 60,000–40,000 years ago.
- End of the last ice age: Clark et al. 2009, *Science* 325:710. Ice sheets at their maximum 26,500 to 20,000–19,000 years ago, retreat from 20,000–19,000. The Holocene start (11,700 b2k) is already in the ICS file.
- Writing: the Cuneiform Digital Library Initiative (CDLI) dates the Uruk IV period, the first phase of proto-cuneiform, to about 3350–3200 BCE.
- Industrial revolution: Britannica gives 1760–1830 as the conventional span; other accounts run to about 1840 (Toynbee) or start in the 1780s (Hobsbawm).
- Farming: Larson et al. 2014, *PNAS* 111:6139 looks right but its dates weren't confirmed from the abstract. First cities: no source found yet.
- Language: no source gives a defensible date. Keep it hatched as disputed with no line.

## Ways to show unknowns (ideas, Nov 2026)

The page already draws the first layer: a published range fades, and where no uncertainty is given the mark is dashed, faded or soft. Ideas for the deeper layers:
- **Dates moving over time (Eduardo likes this one).** Faint "ghost" marks where something used to be dated, such as Out of Africa or *H. antecessor*, to show that today's figures are this decade's estimates. It needs sourced past estimates too (which paper, which year, which date), so it is a sourcing job as much as a drawing one.
- Disagreement between sources: rival estimates side by side, such as several population reconstructions. The spread shows how far any one source's stated error can be trusted.
- How much evidence there is: done for radiocarbon (Nov 2026, "What has been dated" row, p3k14c). Other dating methods are not counted.
- What kind of knowledge each mark is: a small coloured tick for measured, dated, estimated, guessed or placeholder.

Fixed (Nov 2026): the life lane's fossil bars stop about 8,200 years ago (the end of PBDB's data), and the stretch after that is now drawn as no data instead of blank.

## Ghost dates (Nov 2026, Eduardo's pick of four cases)

On the Human time tab, a small hollow ring on the top edge of a row marks where an earlier (or later) study put a date, joined by a dotted line to where the bar starts now. Tapping the ring gives the published figure, the year of that view and its source. The data is `GHOSTS` in `src/page.html`; sources are registered in `data/atlas.json`.
- Holocene start: 10,000 radiocarbon years BP (Mangerud et al. 1974, as cited in later literature), drawn where readers of the time put it, about 10,000 years ago. Today's boundary is 11,700 b2k (Walker et al. 2009).
- Anthropocene start: late 18th century, Watt's steam engine of 1784 (Crutzen 2002), against the later 1952 proposal.
- Oldest *Homo sapiens* fossils: about 130,000 years (Omo, before 2005, as reported by McDougall et al. 2005) and 195,000 ± 5,000 (McDougall et al. 2005). The bar itself starts at the Smithsonian's date; Jebel Irhoud (315,000 ± 34,000, Hublin et al. 2017) is mentioned in the note.
- *H. luzonensis*: at least 134,000 years (Grün and Stringer 2023, figure as reported by the Natural History Museum; paper not read). Here the ghost is a later, older estimate; the bar still shows the 2019 minimum ages.
- Not yet on the Deep time tab.

## Human time labels (Nov 2026, Eduardo)

The chart's marker labels went back to the short plain names: Fire, Language, Out of Africa, End of ice age, Farming, Cities, Writing, Industrial revolution (plus LLMs). The buttons above keep the more technical names. The header line is just "Deep Time Atlas · v0.3", and the data note under the chart runs the full width.

## Wording (Nov 2026, Eduardo)

- Aim: closer to the technical literature, readable at undergraduate or early postgraduate level, with some of the cheeky tone kept.
- "Lane" is gone from the page: it meant nothing to readers. The chart's parts are "rows".
- The Deep time tab's heading is "The last 4.6 billion years", and its intro now mirrors the Human time one.
- "No data — not zero" now reads "hard to say — some number, for sure" (it only shows where it fits).
- Marker button names: "Habitual use of fire", "End of the last glacial period" (strictly, the ice age has not ended), "Origins of farming", "Writing (proto-cuneiform)", "Industrial revolution". The labels on the chart itself stay short (see above).
- Calendar years print without a thousands comma (1760 CE, not 1,760 CE).

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
