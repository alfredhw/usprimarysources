#!/usr/bin/env python3
"""Generate nav.js (site map + browse bar) and wire it into every AmeriDocs page."""
import json, os, re
from bs4 import BeautifulSoup

SITE = "/sessions/cool-nifty-allen/mnt/americandocs"

STATES = sorted([
    "alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware",
    "florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky",
    "louisiana","maine","maryland","massachusetts","michigan","minnesota","mississippi",
    "missouri","montana","nebraska","nevada","new-hampshire","new-jersey","new-mexico",
    "new-york","north-carolina","north-dakota","ohio","oklahoma","oregon","pennsylvania",
    "rhode-island","south-carolina","south-dakota","tennessee","texas","utah","vermont",
    "virginia","washington","west-virginia","wisconsin","wyoming"
])
TERRITORIES = ["american-samoa","district-of-columbia","guam","northern-mariana-islands",
               "puerto-rico","us-virgin-islands"]
REGIONS = ["new-england","mid-atlantic","southeast","midwest","great-plains","mountain-west",
           "southwest","pacific"]
# homepage listing order
THEMES = ["immigration","native-nations","slavery-abolition","westward-expansion","labor",
          "womens-history","military","economic-history","religious-history","gender-sexuality",
          "foodways","entertainment-sports","hispanic-latino","asian-american","us-latin-america",
          "african-american","environment-conservation","science-technology"]
# chronological order
ERAS = ["colonial","revolution-early-republic","antebellum","civil-war-reconstruction",
        "gilded-age-progressive","depression-world-wars","cold-war","recent-america"]
# sources by form
FORMS = ["material-culture","built-environment","maps-land","photographs-film","oral-history"]

def display_name(slug):
    """Read the breadcrumb <strong> text from the page."""
    path = os.path.join(SITE, slug + ".html")
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    nav = soup.find("nav")
    if nav and nav.find("strong"):
        t = re.sub(r"\s+", " ", nav.find("strong").get_text()).strip()
        # breadcrumb on subpages is the page name; on index it's "You are here:" - skip
        if t and not t.lower().startswith("you are here"):
            return t
    return slug.replace("-", " ").title()

sitemap = {
    "states":      [{"s": s, "n": display_name(s)} for s in STATES],
    "territories": [{"s": s, "n": display_name(s)} for s in TERRITORIES],
    "regions":     [{"s": s, "n": display_name(s)} for s in REGIONS],
    "themes":      [{"s": s, "n": display_name(s)} for s in THEMES],
    "eras":        [{"s": s, "n": display_name(s)} for s in ERAS],
    "forms":       [{"s": s, "n": display_name(s)} for s in FORMS],
}

NAV_JS = """// AmeriDocs site navigation — generated file, edit gen_nav.py instead
(function () {
  var SITE = __SITEMAP__;
  var GROUPS = [
    ["states", "States"],
    ["territories", "Territories"],
    ["regions", "Regions"],
    ["themes", "Themes"],
    ["eras", "Eras"],
    ["forms", "By Form"]
  ];

  var here = (location.pathname.split("/").pop() || "index.html").replace(".html", "");
  if (here === "") here = "index";

  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  // which group is the current page in, and where?
  var curGroup = null, curIdx = -1;
  GROUPS.forEach(function (g) {
    var idx = SITE[g[0]].findIndex(function (p) { return p.s === here; });
    if (idx >= 0) { curGroup = g[0]; curIdx = idx; }
  });

  // ---- build the browse bar ----
  var bar = document.createElement("div");
  bar.className = "browse-bar";
  var html = "";

  GROUPS.forEach(function (g) {
    var key = g[0], label = g[1];
    var isCur = key === curGroup;
    html += '<details class="dd' + (isCur ? " current" : "") + '"><summary>' + label + '</summary>' +
      '<div class="dd-panel' + (key === "states" ? " cols" : "") + '">' +
      SITE[key].map(function (p) {
        return '<a href="' + p.s + '.html"' + (p.s === here ? ' class="here"' : "") + '>' + esc(p.n) + '</a>';
      }).join("") + '</div></details>';
  });

  html += '<a class="bar-link' + (here === "federal" ? " here" : "") + '" href="federal.html">Federal</a>';

  // "On this page" section menu from h2s
  var h2s = Array.prototype.slice.call(document.querySelectorAll("h2"));
  if (h2s.length >= 3) {
    var seen = {};
    var items = h2s.map(function (h) {
      var txt = h.textContent.replace(/\\s+/g, " ").trim();
      var id = h.id;
      if (!id) {
        id = txt.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
        while (seen[id]) id += "-2";
        h.id = id;
      }
      seen[id] = true;
      return '<a href="#' + id + '">' + esc(txt) + '</a>';
    });
    html += '<details class="dd on-page"><summary>On this page</summary><div class="dd-panel">' +
      items.join("") + '</div></details>';
  }

  // compact search
  html += '<form class="bar-search" action="search.html" method="get">' +
    '<input type="search" name="q" placeholder="Search collections&hellip;" aria-label="Search collections">' +
    '</form>';

  bar.innerHTML = html;

  var nav = document.querySelector("nav");
  if (nav) nav.parentNode.insertBefore(bar, nav.nextSibling);
  else document.body.insertBefore(bar, document.body.firstChild);

  // close other dropdowns when one opens; close all on outside click / Escape
  bar.addEventListener("toggle", function (ev) {
    if (ev.target.open) {
      bar.querySelectorAll("details.dd[open]").forEach(function (d) {
        if (d !== ev.target) d.open = false;
      });
    }
  }, true);
  document.addEventListener("click", function (ev) {
    if (!bar.contains(ev.target)) {
      bar.querySelectorAll("details.dd[open]").forEach(function (d) { d.open = false; });
    }
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") {
      bar.querySelectorAll("details.dd[open]").forEach(function (d) { d.open = false; });
    }
  });

  // ---- prev / next paging within the current group ----
  if (curGroup) {
    var list = SITE[curGroup];
    var prev = curIdx > 0 ? list[curIdx - 1] : null;
    var next = curIdx < list.length - 1 ? list[curIdx + 1] : null;
    var pager = document.createElement("div");
    pager.className = "pager";
    pager.innerHTML =
      (prev ? '<a class="pager-prev" href="' + prev.s + '.html">&larr; ' + esc(prev.n) + '</a>' : "<span></span>") +
      (next ? '<a class="pager-next" href="' + next.s + '.html">' + esc(next.n) + ' &rarr;</a>' : "<span></span>");
    var footer = document.querySelector("footer");
    if (footer) footer.parentNode.insertBefore(pager, footer);
  }
})();
"""

with open(os.path.join(SITE, "nav.js"), "w", encoding="utf-8") as f:
    f.write(NAV_JS.replace("__SITEMAP__", json.dumps(sitemap, ensure_ascii=False)))

# ---- wire the script into every page (idempotent) ----
wired = already = 0
for fname in sorted(os.listdir(SITE)):
    if not fname.endswith(".html"):
        continue
    path = os.path.join(SITE, fname)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if 'src="nav.js"' in html:
        already += 1
        continue
    new = html.replace('<link rel="stylesheet" href="style.css">',
                       '<link rel="stylesheet" href="style.css">\n  <script src="nav.js" defer></script>', 1)
    if new == html:
        print(f"WARN: no stylesheet link found in {fname}")
        continue
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    wired += 1

print(f"nav.js generated: {sum(len(v) for v in sitemap.values())} pages in site map "
      f"({len(sitemap['states'])} states, {len(sitemap['territories'])} territories, "
      f"{len(sitemap['regions'])} regions, {len(sitemap['themes'])} themes)")
print(f"script tag wired into {wired} pages ({already} already had it)")
