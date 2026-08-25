# AmeriDocs — Online Sources for United States History

A directory of freely accessible primary source collections for US history,
inspired by [EuroDocs](https://eudocs.lib.byu.edu/) at Brigham Young University.

**2,700+ verified collections** across 95+ pages, organized five ways:

- **States & Territories** — 50 states, 6 territories, plus a federal/national page
- **Themes** — 15 pages from Immigration to Foodways to US–Latin America relations
- **Eras** — 8 chronological pages, Colonial America through Recent America
- **Regions** — 8 pages complementing the state pages with cross-state collections
- **Sources by Form** — objects & material culture, built environment, maps, photographs & film, oral history

Plus client-side **search** over every collection (`search.html`), a site-wide
browse bar, prev/next paging, and computed related-pages links.

## Architecture

Static HTML, no build step required to serve. Shared assets:

- `style.css` — single stylesheet (navy/gold academic design)
- `nav.js` — browse bar, dropdowns, pager (generated)
- `related.js` — related-pages boxes (generated)
- `sources.js` — search index of every collection (generated)

## Regenerating the generated files

After adding or editing pages, run from the repo root:

```
python3 tools/build_index.py    # rebuilds sources.js (search index)
python3 tools/gen_nav.py        # rebuilds nav.js (site map + browse bar)
python3 tools/gen_related.py    # rebuilds related.js (TF-IDF related pages)
```

Requires Python 3 with `beautifulsoup4`. New pages are picked up automatically;
new states/themes/eras/forms must be added to the slug lists at the top of
`gen_nav.py`, `build_index.py`, and `gen_related.py`.

Note: the `tools/` scripts contain absolute paths from the original build
environment; adjust the `SITE` constant if running elsewhere.

## Link policy

Every external link was verified in August 2026. All linked collections are
free to access — no subscriptions or paywalls. Link-check artifacts
(`check_links.py`, `*.csv`) document the audit trail.
