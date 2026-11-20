# Deep Time Atlas

An interactive timeline of human history and deep time, from the formation of the Earth to now, built around one idea: **uncertainty is drawn, not hidden.** Uncertain dates fade across their plausible range, disputed categories are hatched, and "no data" is drawn differently from zero.

**Status:** early working version (v0.3). The structure works; the data does not yet. Every value is a placeholder that hasn't been checked against a source, and the page says so.

## View it

Open `index.html` in any browser, or visit the GitHub Pages site for this repository. There are four tabs:

- **Human time:** the last million years, with world population, key thresholds (fire, language, out of Africa, end of the last ice age, farming, cities, writing, industry), geological periods and hominin species.
- **Full atlas:** every lane, across all of time.
- **Stories:** short step-through views for teaching.
- **About:** how to read the chart, and the list of sources.

## Change it

- Edit the page in `src/page.html` and the data in `data/atlas.json`.
- Run `python3 build.py` to regenerate `index.html`.
- Background and decisions are in `docs/notes.md`.

The page is a single self-contained HTML file. It uses no libraries; it loads only web fonts.

---

*This README and the page's explanatory text were drafted with AI assistance (Claude).*
