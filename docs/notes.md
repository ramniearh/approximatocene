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
- Population: one clear line through the middle of each range, with the range as a soft haze around it. **The line is the geometric midpoint of a placeholder range, not a sourced estimate.** When real data arrives (HYDE 3.3 or Our World in Data, which publish central estimates), the line should switch to those.
- Before 300,000 years ago there is no population estimate. A faint dotted line runs low there to say "small, thousands to tens of thousands", and the page labels it as not a figure.
- Geology strip: Pleistocene and Holocene, with the Early, Middle (Chibanian) and Late Pleistocene, the three Holocene ages, and a hatched "Anthropocene?" for the 2024 rejection.
- The hominin strip shows species (several of them contested), not subspecies. Disputed ones are hatched.
- Placeholder warnings stay visible until real data replaces them.

## Data status

- **Everything is a placeholder** written from memory to make the page work. Nothing has been checked against a source.
- Fixed: the population list had two samples at the same date ("5000 b2k" and "3000 BCE" are the same year). The first was moved to 7000 b2k (5000 BCE), which seemed to be the intent. This needs confirming when real figures go in.
- Some lanes in the Full atlas are invented outright and labelled that way. Temperature is sine waves and energy per person has made-up numbers. The political-forms lane is a speculative impression.
- Sources to start with, when real data goes in: Our World in Data or HYDE 3.3 for population, the International Chronostratigraphic Chart for geological dates, and the Smithsonian Human Origins pages for hominin species. Candidate sources are listed in `docs/reference/SOURCES.md` and in `data/atlas.json` under `sources`.

## Reference datasets

- Decided Nov 2026: sourced reference data goes in `data/reference/` as plain CSV files, one per dataset, with a `source` column on every row. Values are copied as the source gives them (including `~` and `±`), not cleaned up. The page doesn't read them yet.
- `geologic_time_ics.csv`: all 178 units (eons to stages) from the ICS chart v2024/12, read from stratigraphy.org/chart on 2026-11-20. Ages are in millions of years ago (Ma); `top_ma` is the younger boundary and `base_ma` the older one. The chart is not fully consistent with itself in a few places (for example, the base of the Neogene is 23.03 but the top of the Paleogene is 23.04), and the file keeps those as published.
- `hominin_species_smithsonian.csv`: the 21 species on the Smithsonian Human Origins species list, read 2026-11-20. `when_lived` is the Smithsonian's own wording, and `oldest_ya` / `youngest_ya` are those same numbers in years ago. Where the page gives a single date ("about 4.4 million years ago"), both columns hold it. Two species have no discovery year on their page, so that cell is blank.
- Three groups shown on the Human time tab are not on the Smithsonian list and have no sourced dates yet: Denisovans, *H. antecessor* and *H. luzonensis*. A second source would be needed for them.

## Open questions (Eduardo's call)

- Should the political-forms lane stay? Nobody has these numbers. The options are to keep it as a clearly labelled impression, to replace it with something countable (such as the size of the largest polity over time), or to drop it.
- Which population source to use first, and whether to show more than one reconstruction where they disagree.

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
