// AmeriDocs site navigation — generated file, edit gen_nav.py instead
(function () {
  var SITE = {"states": [{"s": "alabama", "n": "Alabama"}, {"s": "alaska", "n": "Alaska"}, {"s": "arizona", "n": "Arizona"}, {"s": "arkansas", "n": "Arkansas"}, {"s": "california", "n": "California"}, {"s": "colorado", "n": "Colorado"}, {"s": "connecticut", "n": "Connecticut"}, {"s": "delaware", "n": "Delaware"}, {"s": "florida", "n": "Florida"}, {"s": "georgia", "n": "Georgia"}, {"s": "hawaii", "n": "Hawaii"}, {"s": "idaho", "n": "Idaho"}, {"s": "illinois", "n": "Illinois"}, {"s": "indiana", "n": "Indiana"}, {"s": "iowa", "n": "Iowa"}, {"s": "kansas", "n": "Kansas"}, {"s": "kentucky", "n": "Kentucky"}, {"s": "louisiana", "n": "Louisiana"}, {"s": "maine", "n": "Maine"}, {"s": "maryland", "n": "Maryland"}, {"s": "massachusetts", "n": "Massachusetts"}, {"s": "michigan", "n": "Michigan"}, {"s": "minnesota", "n": "Minnesota"}, {"s": "mississippi", "n": "Mississippi"}, {"s": "missouri", "n": "Missouri"}, {"s": "montana", "n": "Montana"}, {"s": "nebraska", "n": "Nebraska"}, {"s": "nevada", "n": "Nevada"}, {"s": "new-hampshire", "n": "New Hampshire"}, {"s": "new-jersey", "n": "New Jersey"}, {"s": "new-mexico", "n": "New Mexico"}, {"s": "new-york", "n": "New York"}, {"s": "north-carolina", "n": "North Carolina"}, {"s": "north-dakota", "n": "North Dakota"}, {"s": "ohio", "n": "Ohio"}, {"s": "oklahoma", "n": "Oklahoma"}, {"s": "oregon", "n": "Oregon"}, {"s": "pennsylvania", "n": "Pennsylvania"}, {"s": "rhode-island", "n": "Rhode Island"}, {"s": "south-carolina", "n": "South Carolina"}, {"s": "south-dakota", "n": "South Dakota"}, {"s": "tennessee", "n": "Tennessee"}, {"s": "texas", "n": "Texas"}, {"s": "utah", "n": "Utah"}, {"s": "vermont", "n": "Vermont"}, {"s": "virginia", "n": "Virginia"}, {"s": "washington", "n": "Washington"}, {"s": "west-virginia", "n": "West Virginia"}, {"s": "wisconsin", "n": "Wisconsin"}, {"s": "wyoming", "n": "Wyoming"}], "territories": [{"s": "american-samoa", "n": "American Samoa"}, {"s": "district-of-columbia", "n": "District of Columbia"}, {"s": "guam", "n": "Guam"}, {"s": "northern-mariana-islands", "n": "Northern Mariana Islands"}, {"s": "puerto-rico", "n": "Puerto Rico"}, {"s": "us-virgin-islands", "n": "U.S. Virgin Islands"}], "regions": [{"s": "new-england", "n": "New England"}, {"s": "mid-atlantic", "n": "Mid-Atlantic"}, {"s": "southeast", "n": "Southeast"}, {"s": "midwest", "n": "Midwest"}, {"s": "great-plains", "n": "Great Plains"}, {"s": "mountain-west", "n": "Mountain West"}, {"s": "southwest", "n": "Southwest"}, {"s": "pacific", "n": "Pacific"}], "themes": [{"s": "immigration", "n": "Immigration & Migration"}, {"s": "native-nations", "n": "Native Nations & Indigenous History"}, {"s": "slavery-abolition", "n": "Slavery, Abolition & the African American Experience"}, {"s": "westward-expansion", "n": "Westward Expansion & the Frontier"}, {"s": "labor", "n": "Labor & Industry"}, {"s": "womens-history", "n": "Women’s History"}, {"s": "military", "n": "Military & Wartime"}, {"s": "economic-history", "n": "Economic & Commercial History"}, {"s": "religious-history", "n": "American Religious History"}, {"s": "gender-sexuality", "n": "Gender & Sexuality"}, {"s": "foodways", "n": "American Foodways"}, {"s": "entertainment-sports", "n": "Entertainment & Sports"}, {"s": "hispanic-latino", "n": "Hispanic & Latino American Experience"}, {"s": "asian-american", "n": "Asian American & Pacific Islander Experience"}, {"s": "us-latin-america", "n": "The United States & Latin America"}, {"s": "african-american", "n": "African American History"}, {"s": "environment-conservation", "n": "Environment & Conservation"}, {"s": "science-technology", "n": "Science & Technology"}], "eras": [{"s": "colonial", "n": "Colonial America, 1492–1763"}, {"s": "revolution-early-republic", "n": "Revolution & Early Republic, 1763–1815"}, {"s": "antebellum", "n": "Antebellum America, 1815–1861"}, {"s": "civil-war-reconstruction", "n": "Civil War & Reconstruction, 1861–1877"}, {"s": "gilded-age-progressive", "n": "Gilded Age & Progressive Era, 1877–1917"}, {"s": "depression-world-wars", "n": "World Wars & Depression, 1917–1945"}, {"s": "cold-war", "n": "Cold War America, 1945–1991"}, {"s": "recent-america", "n": "Recent America, 1991–Present"}], "forms": [{"s": "material-culture", "n": "Objects & Material Culture"}, {"s": "built-environment", "n": "Built Environment & Historic Places"}, {"s": "maps-land", "n": "Maps & the Land"}, {"s": "photographs-film", "n": "Photographs & Film"}, {"s": "oral-history", "n": "Oral History"}]};
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
      var txt = h.textContent.replace(/\s+/g, " ").trim();
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
