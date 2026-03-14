import urllib.request
import urllib.parse
import json
import os
import re


RESTCOUNTRIES = "https://restcountries.com/v3.1"
OPEN_METEO    = "https://api.open-meteo.com/v1/forecast"
WIKI_API      = "https://en.wikipedia.org/api/rest_v1/page/summary"

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TravelApp/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception:
        return {}

def fetch_list(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TravelApp/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception:
        return []

def get_weather(lat, lon):
    url = (f"{OPEN_METEO}?latitude={lat}&longitude={lon}"
           f"&current=temperature_2m,weathercode,windspeed_10m,relative_humidity_2m"
           f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
           f"&timezone=auto&forecast_days=5")
    return fetch(url)

def get_wiki_summary(topic):
    encoded = urllib.parse.quote(topic.replace(" ","_"))
    data = fetch(f"{WIKI_API}/{encoded}")
    return data.get("extract","")[:500] if data else ""

# ─────────────────────────────────────────
# DATA CONSTANTS (unchanged from original)
# ─────────────────────────────────────────
WMO_CODES = {
    0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",
    45:"Foggy",48:"Icy fog",51:"Light drizzle",53:"Drizzle",55:"Heavy drizzle",
    61:"Slight rain",63:"Moderate rain",65:"Heavy rain",
    71:"Slight snow",73:"Moderate snow",75:"Heavy snow",
    80:"Rain showers",81:"Moderate showers",82:"Violent showers",
    95:"Thunderstorm",96:"Thunderstorm w/ hail",99:"Heavy thunderstorm",
}

WMO_ICONS = {
    0:"☀️",1:"🌤️",2:"⛅",3:"☁️",45:"🌫️",48:"🌫️",
    51:"🌦️",53:"🌦️",55:"🌧️",61:"🌧️",63:"🌧️",65:"🌧️",
    71:"🌨️",73:"❄️",75:"❄️",80:"🌦️",81:"🌧️",82:"⛈️",
    95:"⛈️",96:"⛈️",99:"⛈️",
}

# Featured regions with Unsplash photos
REGIONS = [
    {"name":"Europe",     "icon":"🏰","img":"https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=500&q=85&auto=format&fit=crop","countries":["France","Italy","Spain","Greece","Germany"]},
    {"name":"Asia",       "icon":"🏯","img":"https://images.unsplash.com/photo-1464817739973-0128fe77aaa1?w=500&q=85&auto=format&fit=crop","countries":["Japan","Thailand","India","China","Vietnam"]},
    {"name":"Americas",   "icon":"🗽","img":"https://images.unsplash.com/photo-1485738422979-f5c462d49f74?w=500&q=85&auto=format&fit=crop","countries":["United States","Brazil","Mexico","Canada","Argentina"]},
    {"name":"Africa",     "icon":"🦁","img":"https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=500&q=85&auto=format&fit=crop","countries":["Morocco","Egypt","Kenya","South Africa","Tanzania"]},
    {"name":"Oceania",    "icon":"🦘","img":"https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=500&q=85&auto=format&fit=crop","countries":["Australia","New Zealand","Fiji","Papua New Guinea"]},
    {"name":"Middle East","icon":"🕌","img":"https://images.unsplash.com/photo-1518684079-3c830dcef090?w=500&q=85&auto=format&fit=crop","countries":["UAE","Saudi Arabia","Jordan","Turkey","Israel"]},
]

POPULAR_COUNTRIES = [
    {"name":"France",      "cca2":"FR","flag":"🇫🇷","img":"https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&q=85&auto=format&fit=crop"},
    {"name":"Japan",       "cca2":"JP","flag":"🇯🇵","img":"https://images.unsplash.com/photo-1513407030348-c983a97b98d8?w=600&q=85&auto=format&fit=crop"},
    {"name":"Italy",       "cca2":"IT","flag":"🇮🇹","img":"https://images.unsplash.com/photo-1534445967719-8ae7b972b1a5?w=600&q=85&auto=format&fit=crop"},
    {"name":"Thailand",    "cca2":"TH","flag":"🇹🇭","img":"https://images.unsplash.com/photo-1528181304800-259b08848526?w=600&q=85&auto=format&fit=crop"},
    {"name":"UAE",         "cca2":"AE","flag":"🇦🇪","img":"https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&q=85&auto=format&fit=crop"},
    {"name":"Greece",      "cca2":"GR","flag":"🇬🇷","img":"https://images.unsplash.com/photo-1533105079780-92b9be482077?w=600&q=85&auto=format&fit=crop"},
    {"name":"Morocco",     "cca2":"MA","flag":"🇲🇦","img":"https://images.unsplash.com/photo-1590595906931-81f04f0ccebb?w=600&q=85&auto=format&fit=crop"},
    {"name":"Australia",   "cca2":"AU","flag":"🇦🇺","img":"https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=600&q=85&auto=format&fit=crop"},
    {"name":"Brazil",      "cca2":"BR","flag":"🇧🇷","img":"https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=600&q=85&auto=format&fit=crop"},
    {"name":"India",       "cca2":"IN","flag":"🇮🇳","img":"https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&q=85&auto=format&fit=crop"},
    {"name":"Turkey",      "cca2":"TR","flag":"🇹🇷","img":"https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=600&q=85&auto=format&fit=crop"},
    {"name":"Peru",        "cca2":"PE","flag":"🇵🇪","img":"https://images.unsplash.com/photo-1526392060635-9d6019884377?w=600&q=85&auto=format&fit=crop"},
]

CLIMATE_TYPES = [
    {"name":"Tropical",  "icon":"🌴","desc":"Hot & humid year-round"},
    {"name":"Desert",    "icon":"🏜️","desc":"Dry & sunny, extreme temps"},
    {"name":"Temperate", "icon":"🌿","desc":"Mild seasons, rain likely"},
    {"name":"Arctic",    "icon":"❄️","desc":"Cold, snow & northern lights"},
    {"name":"Mountain",  "icon":"🏔️","desc":"Cool, fresh alpine air"},
    {"name":"Coastal",   "icon":"🌊","desc":"Breezy, beachy, refreshing"},
]

ATTRACTION_TYPES = [
    {"name":"Beaches",        "icon":"🏖️"},
    {"name":"Mountains",      "icon":"⛰️"},
    {"name":"Ancient Ruins",  "icon":"🏛️"},
    {"name":"Food & Cuisine", "icon":"🍜"},
    {"name":"Nightlife",      "icon":"🌃"},
    {"name":"Wildlife",       "icon":"🦒"},
    {"name":"Architecture",   "icon":"🕌"},
    {"name":"Nature & Parks", "icon":"🌲"},
]

def get_weather(lat, lon):
    url = (f"{OPEN_METEO}?latitude={lat}&longitude={lon}"
           f"&current=temperature_2m,weathercode,windspeed_10m,relative_humidity_2m"
           f"&daily=temperature_2m_max,temperature_2m_min,weathercode"
           f"&timezone=auto&forecast_days=5")
    return fetch(url)

def get_country_data(name):
    encoded = urllib.parse.quote(name)
    data = fetch_list(f"{RESTCOUNTRIES}/name/{encoded}?fullText=false")
    if not data or isinstance(data, dict):
        return None
    # prefer exact match
    exact = [c for c in data if c.get("name",{}).get("common","").lower() == name.lower()]
    return (exact or data)[0]

def get_wiki_summary(topic):
    encoded = urllib.parse.quote(topic.replace(" ","_"))
    data = fetch(f"{WIKI_API}/{encoded}")
    return data.get("extract","")[:500] if data else ""

def get_attractions(country_name):
    """Return curated tourist spots based on country."""
    attractions_db = {
        "France":      [{"name":"Eiffel Tower","city":"Paris","type":"Landmark","img":"https://images.unsplash.com/photo-1511739001486-6bfe10ce785f?w=500&q=85&auto=format&fit=crop"},{"name":"Louvre Museum","city":"Paris","type":"Museum","img":"https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=500&q=85&auto=format&fit=crop"},{"name":"French Riviera","city":"Nice","type":"Beach","img":"https://images.unsplash.com/photo-1533929736458-ca588d08c8be?w=500&q=85&auto=format&fit=crop"}],
        "Japan":       [{"name":"Mount Fuji","city":"Shizuoka","type":"Nature","img":"https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?w=500&q=85&auto=format&fit=crop"},{"name":"Fushimi Inari","city":"Kyoto","type":"Temple","img":"https://images.unsplash.com/photo-1478436127897-769e1b3f0f36?w=500&q=85&auto=format&fit=crop"},{"name":"Shibuya Crossing","city":"Tokyo","type":"Landmark","img":"https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=500&q=85&auto=format&fit=crop"}],
        "Italy":       [{"name":"Colosseum","city":"Rome","type":"Ancient Ruins","img":"https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=500&q=85&auto=format&fit=crop"},{"name":"Venice Canals","city":"Venice","type":"Landmark","img":"https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=500&q=85&auto=format&fit=crop"},{"name":"Amalfi Coast","city":"Amalfi","type":"Beach","img":"https://images.unsplash.com/photo-1534430480872-3498386e7856?w=500&q=85&auto=format&fit=crop"}],
        "UAE":         [{"name":"Burj Khalifa","city":"Dubai","type":"Landmark","img":"https://images.unsplash.com/photo-1582672060674-bc2bd808a8b5?w=500&q=85&auto=format&fit=crop"},{"name":"Sheikh Zayed Mosque","city":"Abu Dhabi","type":"Architecture","img":"https://images.unsplash.com/photo-1548813397-26a7e41b82eb?w=500&q=85&auto=format&fit=crop"},{"name":"Dubai Desert","city":"Dubai","type":"Nature","img":"https://images.unsplash.com/photo-1518684079-3c830dcef090?w=500&q=85&auto=format&fit=crop"}],
        "Thailand":    [{"name":"Grand Palace","city":"Bangkok","type":"Temple","img":"https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=500&q=85&auto=format&fit=crop"},{"name":"Phi Phi Islands","city":"Krabi","type":"Beach","img":"https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=500&q=85&auto=format&fit=crop"},{"name":"Chiang Mai Temples","city":"Chiang Mai","type":"Temple","img":"https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=500&q=85&auto=format&fit=crop"}],
        "Greece":      [{"name":"Acropolis","city":"Athens","type":"Ancient Ruins","img":"https://images.unsplash.com/photo-1555993539-1732b0258235?w=500&q=85&auto=format&fit=crop"},{"name":"Santorini","city":"Thira","type":"Scenic","img":"https://images.unsplash.com/photo-1533105079780-92b9be482077?w=500&q=85&auto=format&fit=crop"},{"name":"Meteora Monasteries","city":"Meteora","type":"Landmark","img":"https://images.unsplash.com/photo-1504214208698-ea446addba98?w=500&q=85&auto=format&fit=crop"}],
        "Morocco":     [{"name":"Medina of Fez","city":"Fez","type":"Culture","img":"https://images.unsplash.com/photo-1590595906931-81f04f0ccebb?w=500&q=85&auto=format&fit=crop"},{"name":"Sahara Desert","city":"Merzouga","type":"Nature","img":"https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=500&q=85&auto=format&fit=crop"},{"name":"Majorelle Garden","city":"Marrakech","type":"Garden","img":"https://images.unsplash.com/photo-1597212618440-806262de4f2b?w=500&q=85&auto=format&fit=crop"}],
        "Australia":   [{"name":"Sydney Opera House","city":"Sydney","type":"Landmark","img":"https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=500&q=85&auto=format&fit=crop"},{"name":"Great Barrier Reef","city":"Queensland","type":"Nature","img":"https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=500&q=85&auto=format&fit=crop"},{"name":"Uluru","city":"NT","type":"Nature","img":"https://images.unsplash.com/photo-1529987810545-3d8c0fc7e386?w=500&q=85&auto=format&fit=crop"}],
        "India":       [{"name":"Taj Mahal","city":"Agra","type":"Landmark","img":"https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=500&q=85&auto=format&fit=crop"},{"name":"Kerala Backwaters","city":"Kerala","type":"Nature","img":"https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=500&q=85&auto=format&fit=crop"},{"name":"Jaipur Pink City","city":"Jaipur","type":"Culture","img":"https://images.unsplash.com/photo-1477587458883-47145ed31cf0?w=500&q=85&auto=format&fit=crop"}],
        "Turkey":      [{"name":"Hagia Sophia","city":"Istanbul","type":"Architecture","img":"https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=500&q=85&auto=format&fit=crop"},{"name":"Cappadocia","city":"Göreme","type":"Nature","img":"https://images.unsplash.com/photo-1570939274717-7eda259b50ed?w=500&q=85&auto=format&fit=crop"},{"name":"Ephesus","city":"Selçuk","type":"Ancient Ruins","img":"https://images.unsplash.com/photo-1589308078059-be1415eab4c3?w=500&q=85&auto=format&fit=crop"}],
        "Brazil":      [{"name":"Christ the Redeemer","city":"Rio de Janeiro","type":"Landmark","img":"https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=500&q=85&auto=format&fit=crop"},{"name":"Iguazu Falls","city":"Foz do Iguaçu","type":"Nature","img":"https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=500&q=85&auto=format&fit=crop"},{"name":"Amazon Rainforest","city":"Manaus","type":"Nature","img":"https://images.unsplash.com/photo-1440581572325-0bea30075d9d?w=500&q=85&auto=format&fit=crop"}],
        "Peru":        [{"name":"Machu Picchu","city":"Cusco","type":"Ancient Ruins","img":"https://images.unsplash.com/photo-1526392060635-9d6019884377?w=500&q=85&auto=format&fit=crop"},{"name":"Lake Titicaca","city":"Puno","type":"Nature","img":"https://images.unsplash.com/photo-1558618047-f4e60cee2555?w=500&q=85&auto=format&fit=crop"},{"name":"Colca Canyon","city":"Arequipa","type":"Nature","img":"https://images.unsplash.com/photo-1531761535209-180857e963b9?w=500&q=85&auto=format&fit=crop"}],
    }
    # Default fallback attractions
    default = [
        {"name":"City Center","city":country_name,"type":"Landmark","img":"https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=400&q=80&auto=format&fit=crop"},
        {"name":"National Museum","city":country_name,"type":"Museum","img":"https://images.unsplash.com/photo-1565799557186-3ea2e82e6a40?w=400&q=80&auto=format&fit=crop"},
        {"name":"Natural Reserve","city":country_name,"type":"Nature","img":"https://images.unsplash.com/photo-1501854140801-50d01698950b?w=400&q=80&auto=format&fit=crop"},
    ]
    return attractions_db.get(country_name, default)

# ─────────────────────────────────────────
# TEMPLATE ENGINE  (tiny Jinja2-compatible)
# ─────────────────────────────────────────
_BASE = os.path.dirname(os.path.abspath(__file__))
_TMPL = os.path.join(_BASE, "templates")

def _load(name):
    path = os.path.join(_TMPL, name)
    with open(path, encoding="utf-8") as f:
        return f.read()

def _render(name, ctx):
    t = _load(name)

    # {% if expr %} ... {% elif expr %} ... {% else %} ... {% endif %}
    def _eval_if(m):
        cond = m.group(1).strip()
        body = m.group(2)
        elif_parts = re.findall(r'{%[-\s]*elif\s+(.*?)\s*[-]?%}(.*?)(?={%[-\s]*elif|{%[-\s]*else|{%[-\s]*endif)', body, re.DOTALL)
        else_m = re.search(r'{%[-\s]*else[-\s]*%}(.*?)$', body, re.DOTALL)
        try:
            if eval(cond, {}, ctx):
                main_body = re.split(r'{%[-\s]*(?:elif|else)', body)[0]
                return _render_str(main_body, ctx)
            for ec, eb in elif_parts:
                if eval(ec.strip(), {}, ctx):
                    return _render_str(eb, ctx)
            if else_m:
                return _render_str(else_m.group(1), ctx)
        except Exception:
            pass
        return ""

    def _render_str(s, c):
        # {% for x in lst %} ... {% endfor %}
        def do_for(m):
            var, lst_expr = m.group(1), m.group(2)
            body = m.group(3)
            try:
                items = eval(lst_expr, {}, c)
            except Exception:
                return ""
            out = []
            for i, item in enumerate(items):
                inner = dict(c)
                inner[var] = item
                inner["loop"] = type("L", (), {"index0": i, "index": i+1})()
                out.append(_render_str(body, inner))
            return "".join(out)

        s = re.sub(r'{%[-\s]*for\s+(\w+)\s+in\s+(.*?)\s*[-]?%}(.*?){%[-\s]*endfor[-\s]*%}', do_for, s, flags=re.DOTALL)

        # {% if %} blocks
        def do_if(m):
            cond = m.group(1).strip()
            rest = m.group(2)
            try:
                result = eval(cond, {}, c)
            except Exception:
                result = False
            else_m = re.search(r'{%[-\s]*else[-\s]*%}(.*?)$', rest, re.DOTALL)
            if result:
                main = re.split(r'{%[-\s]*else[-\s]*%}', rest)[0]
                return _render_str(main, c)
            elif else_m:
                return _render_str(else_m.group(1), c)
            return ""

        s = re.sub(r'{%[-\s]*if\s+(.*?)\s*[-]?%}(.*?){%[-\s]*endif[-\s]*%}', do_if, s, flags=re.DOTALL)

        # {{ expr }} — safe eval
        def do_expr(m):
            expr = m.group(1).strip()
            # Handle .get() calls, filters like |join, |length
            expr = re.sub(r"\|join\('([^']+)'\)", r".join(\1)", expr)
            expr = re.sub(r"\|length", "..__len__()", expr)
            try:
                val = eval(expr, {"__builtins__": {}}, c)
                return str(val) if val is not None else ""
            except Exception:
                return ""

        s = re.sub(r'\{\{\s*(.*?)\s*\}\}', do_expr, s)
        # Remove leftover {% %} tags
        s = re.sub(r'{%.*?%}', "", s)
        return s

    t = _render_str(t, ctx)
    return t

def _html_resp(start_response, html, status="200 OK"):
    body = html.encode("utf-8")
    start_response(status, [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(body)))
    ])
    return [body]

def _redirect(start_response, location):
    start_response("302 Found", [("Location", location)])
    return [b""]

# ─────────────────────────────────────────
# ROUTE HANDLERS
# ─────────────────────────────────────────
def _handle_index(environ, start_response):
    html = _render("index.html", dict(
        regions=REGIONS,
        popular=POPULAR_COUNTRIES,
        climates=CLIMATE_TYPES,
        attractions=ATTRACTION_TYPES,
        query="", search_type="country",
        results=[], error=None
    ))
    return _html_resp(start_response, html)

def _handle_search(environ, start_response):
    qs = urllib.parse.parse_qs(environ.get("QUERY_STRING", ""))
    q = qs.get("q", [""])[0].strip()
    search_type = qs.get("type", ["country"])[0]
    results = []
    error = None
    if not q:
        return _redirect(start_response, "/")
    if search_type == "country":
        data = fetch_list(f"{RESTCOUNTRIES}/name/{urllib.parse.quote(q)}?fields=name,flags,capital,region,population,area,latlng,cca2")
        if isinstance(data, list): results = data[:12]
        else: error = f'No destinations found for "{q}"'
    elif search_type == "region":
        data = fetch_list(f"{RESTCOUNTRIES}/region/{urllib.parse.quote(q)}?fields=name,flags,capital,region,population,cca2")
        if isinstance(data, list): results = data[:12]
        else: error = f'No countries found in "{q}"'
    html = _render("index.html", dict(
        regions=REGIONS, popular=POPULAR_COUNTRIES,
        climates=CLIMATE_TYPES, attractions=ATTRACTION_TYPES,
        results=results, query=q, search_type=search_type, error=error
    ))
    return _html_resp(start_response, html)

def _handle_destination(cca2, environ, start_response):
    data = fetch_list(f"{RESTCOUNTRIES}/alpha/{cca2}")
    if not data or isinstance(data, dict):
        return _redirect(start_response, "/")
    c = data[0]
    name     = c.get("name", {}).get("common", "")
    capital  = (c.get("capital") or [""])[0]
    latlng   = c.get("latlng", [0, 0])
    lat, lon = (latlng[0], latlng[1]) if len(latlng) >= 2 else (0, 0)

    weather_raw = get_weather(lat, lon)
    current     = weather_raw.get("current", {})
    daily       = weather_raw.get("daily", {})
    weather = {
        "temp":     current.get("temperature_2m", "—"),
        "code":     current.get("weathercode", 0),
        "icon":     WMO_ICONS.get(current.get("weathercode", 0), "🌡️"),
        "desc":     WMO_CODES.get(current.get("weathercode", 0), "—"),
        "wind":     current.get("windspeed_10m", "—"),
        "humidity": current.get("relative_humidity_2m", "—"),
        "forecast": []
    }
    days   = daily.get("time", [])
    maxts  = daily.get("temperature_2m_max", [])
    mints  = daily.get("temperature_2m_min", [])
    wcodes = daily.get("weathercode", [])
    DAYS   = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    from datetime import datetime
    for i in range(min(5, len(days))):
        try: dow = DAYS[datetime.strptime(days[i], "%Y-%m-%d").weekday()]
        except: dow = days[i]
        weather["forecast"].append({
            "day":  dow,
            "icon": WMO_ICONS.get(wcodes[i] if i < len(wcodes) else 0, "🌡️"),
            "max":  round(maxts[i]) if i < len(maxts) else "—",
            "min":  round(mints[i]) if i < len(mints) else "—",
        })

    summary     = get_wiki_summary(name)
    attractions = get_attractions(name)

    currencies  = c.get("currencies", {})
    currency_str = ", ".join([f"{v.get('name',k)} ({v.get('symbol','')})" for k,v in currencies.items()]) if currencies else "—"
    languages   = c.get("languages", {})
    lang_str    = ", ".join(languages.values()) if languages else "—"
    timezones   = c.get("timezones", [])
    tz_str      = timezones[0] if timezones else "—"
    pop         = c.get("population", 0)
    pop_str     = f"{pop/1_000_000:.1f}M" if pop >= 1_000_000 else f"{pop:,}"
    area        = c.get("area", 0)
    area_str    = f"{area:,.0f} km²" if area else "—"

    covers = {
        "France":"https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1400&q=90&auto=format&fit=crop",
        "Japan":"https://images.unsplash.com/photo-1513407030348-c983a97b98d8?w=1400&q=90&auto=format&fit=crop",
        "Italy":"https://images.unsplash.com/photo-1534445967719-8ae7b972b1a5?w=1400&q=90&auto=format&fit=crop",
        "UAE":"https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1400&q=90&auto=format&fit=crop",
        "Thailand":"https://images.unsplash.com/photo-1528181304800-259b08848526?w=1400&q=90&auto=format&fit=crop",
        "Greece":"https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1400&q=90&auto=format&fit=crop",
        "Morocco":"https://images.unsplash.com/photo-1590595906931-81f04f0ccebb?w=1400&q=90&auto=format&fit=crop",
        "Australia":"https://images.unsplash.com/photo-1523482580672-f109ba8cb9be?w=1400&q=90&auto=format&fit=crop",
        "India":"https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1400&q=90&auto=format&fit=crop",
        "Turkey":"https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1400&q=90&auto=format&fit=crop",
        "Brazil":"https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1400&q=90&auto=format&fit=crop",
        "Peru":"https://images.unsplash.com/photo-1526392060635-9d6019884377?w=1400&q=90&auto=format&fit=crop",
    }
    cover_img = covers.get(name, "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1400&q=90&auto=format&fit=crop")

    html = _render("destination.html", dict(
        c=c, name=name, capital=capital,
        weather=weather, summary=summary,
        attractions=attractions,
        currency=currency_str, languages=lang_str,
        timezone=tz_str, population=pop_str, area=area_str,
        cover_img=cover_img
    ))
    return _html_resp(start_response, html)

# ─────────────────────────────────────────
# WSGI ENTRY POINT  (what Vercel calls)
# ─────────────────────────────────────────
def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    # Route: /destination/<cca2>
    m = re.match(r'^/destination/([A-Za-z0-9]+)$', path)
    if m:
        return _handle_destination(m.group(1).upper(), environ, start_response)
    if path == "/search":
        return _handle_search(environ, start_response)
    if path in ("/", ""):
        return _handle_index(environ, start_response)
    # 404
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not Found"]

# Local dev server
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    print("Running on http://localhost:5000")
    make_server("", 5000, app).serve_forever()