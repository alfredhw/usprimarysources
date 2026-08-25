#!/usr/bin/env python3
"""Generate related.js: structural (state<->region) + TF-IDF content-similarity related pages."""
import json, math, os, re
from collections import Counter, defaultdict
from bs4 import BeautifulSoup

SITE = "/sessions/cool-nifty-allen/mnt/outputs/americandocs"

REGION_STATES = {
    "new-england":   ["connecticut","massachusetts","maine","new-hampshire","rhode-island","vermont"],
    "mid-atlantic":  ["delaware","maryland","new-jersey","new-york","pennsylvania"],
    "southeast":     ["alabama","arkansas","florida","georgia","kentucky","louisiana","mississippi",
                      "north-carolina","south-carolina","tennessee","virginia","west-virginia"],
    "midwest":       ["iowa","illinois","indiana","michigan","minnesota","missouri","ohio","wisconsin"],
    "great-plains":  ["kansas","nebraska","north-dakota","oklahoma","south-dakota"],
    "mountain-west": ["colorado","idaho","montana","nevada","utah","wyoming"],
    "southwest":     ["arizona","new-mexico","texas"],
    "pacific":       ["alaska","california","hawaii","oregon","washington"],
}
STATE_REGION = {s: r for r, ss in REGION_STATES.items() for s in ss}
assert len(STATE_REGION) == 50

THEMES = {"immigration","native-nations","slavery-abolition","westward-expansion","labor",
          "womens-history","military","economic-history","religious-history","gender-sexuality",
          "foodways","entertainment-sports","hispanic-latino","asian-american","us-latin-america"}
TERRITORIES = {"american-samoa","district-of-columbia","guam","northern-mariana-islands",
               "puerto-rico","us-virgin-islands"}
ERAS = {"colonial","revolution-early-republic","antebellum","civil-war-reconstruction",
        "gilded-age-progressive","depression-world-wars","cold-war","recent-america"}
FORMS = {"material-culture","built-environment","maps-land","photographs-film","oral-history"}
REGIONS = set(REGION_STATES)

STOP = set("""a an and are as at be but by for from has have in into is it its of on or that the
their this to was were with within also across more most other over under between during against
new all one two through university library collection collections digital archive archives online
history historical american america united states us state records documents papers materials
sources primary including items pages photographs manuscripts century""".split())

def tokens(text):
    return [w for w in re.findall(r"[a-z]{3,}", text.lower()) if w not in STOP]

# ---- load per-page text from sources.js ----
with open(os.path.join(SITE, "sources.js"), encoding="utf-8") as f:
    data = json.loads(re.search(r"= (\[.*\]);", f.read(), re.S).group(1))

page_text = defaultdict(list)
page_name = {}
for e in data:
    page_text[e["s"]].extend(tokens(e["t"] + " " + e["d"] + " " + e["x"]))
    page_name[e["s"]] = e["p"]

slugs = sorted(page_text)
N = len(slugs)

# ---- TF-IDF vectors ----
df = Counter()
tf = {}
for s in slugs:
    c = Counter(page_text[s])
    tf[s] = c
    for w in c:
        df[w] += 1

vecs = {}
for s in slugs:
    total = sum(tf[s].values())
    v = {w: (cnt / total) * math.log(N / df[w]) for w, cnt in tf[s].items() if df[w] > 1}
    norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
    vecs[s] = {w: x / norm for w, x in v.items()}

def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())

# ---- build related lists ----
MIN_SIM = 0.025   # low floor; selection is rank-based
# editorial additions the vocabulary can't see (kept minimal & explicit)
EXTRA_THEMES = {
    "utah": ["religious-history"],
}
related = {}
for s in slugs:
    entries = []
    used = {s}

    # structural relations first
    if s in STATE_REGION:
        r = STATE_REGION[s]
        entries.append({"s": r, "n": page_name[r], "g": "Region"})
        used.add(r)
    elif s in REGIONS:
        for st in REGION_STATES[s]:
            used.add(st)  # don't repeat member states in similarity picks

    # similarity picks: themes and eras — structural links cover the rest
    theme_sims = sorted(((cosine(vecs[s], vecs[o]), o) for o in slugs
                         if o not in used and o in THEMES and o != s),
                        key=lambda x: -x[0])
    picked = [o for sim, o in theme_sims[:3] if sim >= MIN_SIM]
    for o in EXTRA_THEMES.get(s, []):
        if o not in picked:
            picked.append(o)
    for o in picked:
        entries.append({"s": o, "n": page_name[o], "g": "Theme"})

    era_sims = sorted(((cosine(vecs[s], vecs[o]), o) for o in slugs
                       if o not in used and o in ERAS and o != s),
                      key=lambda x: -x[0])
    for sim, o in era_sims[:2]:
        if sim >= MIN_SIM:
            entries.append({"s": o, "n": page_name[o], "g": "Era"})

    # form pages cross-link to each other; other pages get at most one strong form pick
    form_sims = sorted(((cosine(vecs[s], vecs[o]), o) for o in slugs
                        if o not in used and o in FORMS and o != s),
                       key=lambda x: -x[0])
    form_limit = 3 if s in FORMS else 1
    form_floor = MIN_SIM if s in FORMS else 0.06
    for sim, o in form_sims[:form_limit]:
        if sim >= form_floor:
            entries.append({"s": o, "n": page_name[o], "g": "Form"})

    # regions list their member states explicitly (compact group)
    if s in REGIONS:
        entries.append({"s": "", "n": "", "g": "States",
                        "list": [{"s": st, "n": page_name[st]} for st in REGION_STATES[s]]})

    related[s] = entries

RELATED_JS = """// AmeriDocs related pages — generated file, edit gen_related.py instead
(function () {
  var REL = __DATA__;
  var here = (location.pathname.split("/").pop() || "index.html").replace(".html", "");
  var rel = REL[here];
  if (!rel || !rel.length) return;

  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function link(p) { return '<a href="' + p.s + '.html">' + esc(p.n) + '</a>'; }

  var groups = {};
  var order = [];
  rel.forEach(function (e) {
    var g = e.g;
    if (!groups[g]) { groups[g] = []; order.push(g); }
    if (e.list) e.list.forEach(function (p) { groups[g].push(link(p)); });
    else groups[g].push(link(e));
  });

  var LABEL = { "Region": "Region", "Theme": "Related themes", "States": "States in this region",
                "State": "Related states", "Territory": "Related territories", "Federal": "See also",
                "Era": "Related eras", "Form": "By form" };

  var html = '<h3>Related Pages</h3>' + order.map(function (g) {
    return '<div class="related-row"><span class="related-label">' + (LABEL[g] || g) +
           ':</span> ' + groups[g].join(' <span class="rel-sep">&middot;</span> ') + '</div>';
  }).join("");

  var box = document.createElement("div");
  box.className = "related-box";
  box.innerHTML = html;

  var anchor = document.querySelector(".pager") || document.querySelector("footer");
  if (anchor) anchor.parentNode.insertBefore(box, anchor);
})();
"""

with open(os.path.join(SITE, "related.js"), "w", encoding="utf-8") as f:
    f.write(RELATED_JS.replace("__DATA__", json.dumps(related, ensure_ascii=False)))

# ---- wire script tag (idempotent, after nav.js) ----
wired = already = 0
for fname in sorted(os.listdir(SITE)):
    if not fname.endswith(".html"):
        continue
    path = os.path.join(SITE, fname)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if 'src="related.js"' in html:
        already += 1
        continue
    new = html.replace('<script src="nav.js" defer></script>',
                       '<script src="nav.js" defer></script>\n  <script src="related.js" defer></script>', 1)
    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        wired += 1

print(f"related.js: {len(related)} pages mapped; script wired into {wired} pages ({already} already)")
# preview a few
for s in ["georgia", "utah", "southeast", "gender-sexuality", "puerto-rico", "california"]:
    print(f"  {s}: " + "; ".join(
        (e["g"] + "=" + (e["n"] or ",".join(p["n"] for p in e.get("list", [])[:3]) + "...")) for e in related[s]))
