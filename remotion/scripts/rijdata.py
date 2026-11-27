# Car route for "Zo rijd je erin": the last stretch to a garage entrance, plus a styled OSM map.
# Usage: rijdata.py <scratch> <slug> <dest lon> <dest lat> <start lon> <start lat> <keep metres>
import json, math, sys, time, urllib.parse, urllib.request, os
S, slug = sys.argv[1], sys.argv[2]
dlon, dlat, slon, slat, keep = map(float, sys.argv[3:8])
UA = {'User-Agent': 'remotion-asset-build/1.0'}
def get(url, data=None):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA, data=data), timeout=180))
        except Exception as e: err = e; time.sleep(5 + 5 * i)
    raise err
kx = math.cos(math.radians(dlat)) * 111320; ky = 110540
m = lambda lon, lat: ((lon - dlon) * kx, (lat - dlat) * ky)
r = get(f'https://routing.openstreetmap.de/routed-car/route/v1/driving/{slon},{slat};{dlon},{dlat}?overview=full&geometries=geojson&steps=true')['routes'][0]
pts = [m(*c) for c in r['geometry']['coordinates']]
# cumulative distance from the end; keep the last `keep` metres
cum = [0.0]
for a, b in zip(pts, pts[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
tot = cum[-1]; startd = max(0, tot - keep)
kept = []
for i, p in enumerate(pts):
    if cum[i] >= startd:
        if not kept and i > 0:
            a, b = pts[i - 1], p; f = (startd - cum[i - 1]) / max(1e-6, cum[i] - cum[i - 1])
            kept.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
        kept.append(p)
stappen = []
for s in r['legs'][0]['steps']:
    mm = s['maneuver']; x, y = m(*mm['location'])
    stappen.append({'type': mm['type'], 'modifier': mm.get('modifier', ''), 'naam': s.get('name', ''), 'x': round(x), 'y': round(y), 'lengte': round(s['distance'])})
out = {'route': [[round(x), round(y)] for x, y in kept], 'lengte': round(min(keep, tot)), 'stappen': stappen}
xs = [p[0] for p in kept] + [0]; ys = [p[1] for p in kept] + [0]
cxm, cym = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
half_w = max(900, (max(xs) - min(xs)) / 2 + 700); half_h = max(800, (max(ys) - min(ys)) / 2 + 600)
x0, x1, y0, y1 = cxm - half_w, cxm + half_w, cym - half_h, cym + half_h
out['kaart'] = {'x0': round(x0), 'y0': round(y1), 'w': round(x1 - x0), 'h': round(y1 - y0)}
bb = f'{dlat + y0 / ky:.6f},{dlon + x0 / kx:.6f},{dlat + y1 / ky:.6f},{dlon + x1 / kx:.6f}'
q = f'''[out:json][timeout:170];(way["highway"]({bb});way["building"]({bb});way["natural"="water"]({bb});relation["natural"="water"]({bb});
way["waterway"~"^(river|canal|stream)$"]({bb});way["leisure"~"^(park|garden|pitch|playground)$"]({bb});
way["landuse"~"^(grass|forest|recreation_ground|meadow|village_green|cemetery)$"]({bb});way["railway"="rail"]({bb}););out geom;'''
osm_f = f'{S}/osm_rij_{slug}.json'
if not os.path.exists(osm_f):
    json.dump(get('https://maps.mail.ru/osm/tools/overpass/api/interpreter', data=urllib.parse.urlencode({'data': q}).encode()), open(osm_f, 'w'))
d = json.load(open(osm_f))
PX = 1.6
W, H = (x1 - x0) * PX, (y1 - y0) * PX
def path(geom, close=False):
    p = [m(g['lon'], g['lat']) for g in geom]
    return 'M' + ' L'.join(f'{(x - x0) * PX:.1f},{(y1 - y) * PX:.1f}' for x, y in p) + (' Z' if close else '')
ROAD = {'motorway': 24, 'trunk': 22, 'primary': 20, 'secondary': 17, 'tertiary': 14, 'unclassified': 10, 'residential': 10, 'living_street': 9,
        'pedestrian': 9, 'service': 6, 'motorway_link': 12, 'trunk_link': 12, 'primary_link': 12, 'secondary_link': 11, 'tertiary_link': 10,
        'footway': 3.5, 'cycleway': 3.5, 'path': 3, 'steps': 3}
L = {'green': [], 'water': [], 'building': [], 'rail': [], 'waterline': []}; roads = []
for e in d['elements']:
    t = e.get('tags', {})
    geoms = [e['geometry']] if e['type'] == 'way' and 'geometry' in e else [mm['geometry'] for mm in e.get('members', []) if mm.get('role') == 'outer' and 'geometry' in mm]
    for g in geoms:
        if len(g) < 2: continue
        if 'highway' in t:
            w = ROAD.get(t['highway'])
            if w: roads.append((w, path(g)))
        elif 'building' in t: L['building'].append(path(g, True))
        elif t.get('natural') == 'water': L['water'].append(path(g, True))
        elif 'waterway' in t: L['waterline'].append((14 if t['waterway'] in ('river', 'canal') else 5, path(g)))
        elif 'railway' in t: L['rail'].append(path(g))
        else: L['green'].append(path(g, True))
roads.sort(key=lambda x: x[0])
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">', f'<rect width="{W:.0f}" height="{H:.0f}" fill="#E7EBF3"/>',
       '<g fill="#CDEBDF">' + ''.join(f'<path d="{p}"/>' for p in L['green']) + '</g>', '<g fill="#BFE5EE">' + ''.join(f'<path d="{p}"/>' for p in L['water']) + '</g>',
       ''.join(f'<path d="{p}" fill="none" stroke="#BFE5EE" stroke-width="{w * PX:.1f}" stroke-linecap="round"/>' for w, p in L['waterline']),
       '<g fill="#D8DEEA">' + ''.join(f'<path d="{p}"/>' for p in L['building']) + '</g>',
       ''.join(f'<path d="{p}" fill="none" stroke="#C3CAD8" stroke-width="{3 * PX:.1f}" stroke-dasharray="{8 * PX:.0f} {6 * PX:.0f}"/>' for p in L['rail']),
       ''.join(f'<path d="{p}" fill="none" stroke="#FFFFFF" stroke-width="{w * PX:.1f}" stroke-linecap="round" stroke-linejoin="round"/>' for w, p in roads), '</svg>']
open(f'{S}/rij_{slug}.svg', 'w').write(''.join(svg))
json.dump(out, open(f'{S}/rij_{slug}.json', 'w'))
print(json.dumps(out['kaart']), out['lengte'], [(s['type'], s['modifier'], s['naam'], s['lengte']) for s in stappen][-4:])
