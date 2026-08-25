#!/usr/bin/env python3
"""Extract every source entry from AmeriDocs pages into a JS search index."""
import json, os, re
from bs4 import BeautifulSoup

SITE = "/sessions/cool-nifty-allen/mnt/outputs/americandocs"

STATES = {
    "alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware",
    "florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky",
    "louisiana","maine","maryland","massachusetts","michigan","minnesota","mississippi",
    "missouri","montana","nebraska","nevada","new-hampshire","new-jersey","new-mexico",
    "new-york","north-carolina","north-dakota","ohio","oklahoma","oregon","pennsylvania",
    "rhode-island","south-carolina","south-dakota","tennessee","texas","utah","vermont",
    "virginia","washington","west-virginia","wisconsin","wyoming"
}
TERRITORIES = {"american-samoa","district-of-columbia","guam","northern-mariana-islands",
               "puerto-rico","us-virgin-islands"}
REGIONS = {"new-england","mid-atlantic","southeast","midwest","great-plains","mountain-west",
           "southwest","pacific"}
ERAS = {"colonial","revolution-early-republic","antebellum","civil-war-reconstruction",
        "gilded-age-progressive","depression-world-wars","cold-war","recent-america"}
FORMS = {"material-culture","built-environment","maps-land","photographs-film","oral-history"}

def page_type(slug):
    if slug in STATES: return "state"
    if slug in TERRITORIES: return "territory"
    if slug in REGIONS: return "region"
    if slug in ERAS: return "era"
    if slug in FORMS: return "form"
    if slug == "federal": return "federal"
    return "theme"

def clean(s):
    return re.sub(r"\s+", " ", s).strip()

entries = []
for fname in sorted(os.listdir(SITE)):
    if not fname.endswith(".html") or fname in ("index.html", "search.html"):
        continue
    slug = fname[:-5]
    with open(os.path.join(SITE, fname), encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    # page display name from the breadcrumb <strong>
    nav = soup.find("nav")
    page_name = clean(nav.find("strong").get_text()) if nav and nav.find("strong") else slug
    # walk the body tracking current h2/h3
    h2 = h3 = ""
    body = soup.find("body")
    for el in body.descendants:
        if el.name == "h2":
            h2, h3 = clean(el.get_text()), ""
        elif el.name == "h3":
            h3 = clean(el.get_text())
        elif el.name == "li":
            a = el.find("a", href=True)
            if not a or not a["href"].startswith("http"):
                continue
            desc_el = el.find("span", class_="desc")
            desc = clean(desc_el.get_text()) if desc_el else ""
            # strip cross-reference tails like "(See also X.)"
            desc = re.sub(r"\s*\(See also [^)]*\.?\)\s*$", "", desc)
            section = h2 + (" › " + h3 if h3 else "")
            entries.append({
                "t": clean(a.get_text()),        # title
                "u": a["href"],                   # url
                "d": desc,                        # description
                "p": page_name,                   # page display name
                "s": slug,                        # page slug
                "c": page_type(slug),             # category
                "x": section,                     # section within page
            })

# dedupe identical (url, page) pairs, keep first
seen = set()
deduped = []
for e in entries:
    key = (e["u"], e["s"], e["t"])
    if key in seen: continue
    seen.add(key)
    deduped.append(e)

js = "// AmeriDocs search index — generated " + \
     __import__("datetime").date.today().isoformat() + "\n" + \
     "const AMERIDOCS_SOURCES = " + json.dumps(deduped, ensure_ascii=False, separators=(",", ":")) + ";\n"
with open(os.path.join(SITE, "sources.js"), "w", encoding="utf-8") as f:
    f.write(js)

from collections import Counter
c = Counter(e["c"] for e in deduped)
print(f"{len(deduped)} sources indexed from {len(set(e['s'] for e in deduped))} pages")
print(dict(c))
