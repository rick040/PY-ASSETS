# Note: reads the geocoding cache (geocache.json) and the measured places (poi.json) from the scratch folder given as first argument.
# Builds the real map for one kaartje: walking routes (OSRM, foot) and a styled map image from OpenStreetMap data (Overpass).
# Usage: kaartdata.py <scratch> <slug> <poi label in poi.json> <parking slug>=<geocache start query> ...
import json, math, sys, time, urllib.parse, urllib.request, os
S, slug, poi_label = sys.argv[1], sys.argv[2], sys.argv[3]
parks = [a.split('=', 1) for a in sys.argv[4:]]
UA = {'User-Agent': 'remotion-asset-build/1.0'}
def get(url, data=None):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers=UA, data=data)
            return json.load(urllib.request.urlopen(req, timeout=180))
        except Exception as e: err = e; time.sleep(3 + 3 * i)
    raise err
cache = json.load(open(S + '/geocache.json'))
poi = json.load(open(S + '/poi.json'))[poi_label]['geo']
lon0, lat0 = poi[0], poi[1]
kx = math.cos(math.radians(lat0)) * 111320; ky = 110540
m = lambda lon, lat: (round((lon - lon0) * kx, 1), round((lat - lat0) * ky, 1))

def rdp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy) or 1
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / L
        if d > dmax: dmax, idx = d, i
    if dmax > eps: return rdp(pts[:idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]

out = {'parkings': []}
for pslug, q in parks:
    s = cache[q]
    r = get(f'https://routing.openstreetmap.de/routed-foot/route/v1/foot/{s[0]},{s[1]};{lon0},{lat0}?overview=full&geometries=geojson')
    rt = r['routes'][0]
    pts = rdp([m(*c) for c in rt['geometry']['coordinates']], 2.0)
    out['parkings'].append({'locatie': pslug, 'm': round(rt['distance']), 'min': round(rt['duration'] / 60, 1), 'dx': round(m(s[0], s[1])[0]), 'dy': round(m(s[0], s[1])[1]), 'route': [[round(x), round(y)] for x, y in pts]})
    time.sleep(0.5)

# Region: all points with a wide margin, enough to fill the map card in both formats.
xs = [0] + [p['dx'] for p in out['parkings']] + [x for p in out['parkings'] for x, _ in p['route']]
ys = [0] + [p['dy'] for p in out['parkings']] + [y for p in out['parkings'] for _, y in p['route']]
cxm, cym = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
half_w = max(1300, (max(xs) - min(xs)) / 2 + 1100); half_h = max(1100, (max(ys) - min(ys)) / 2 + 900)
x0, x1, y0, y1 = cxm - half_w, cxm + half_w, cym - half_h, cym + half_h
out['kaart'] = {'x0': round(x0), 'y0': round(y1), 'w': round(x1 - x0), 'h': round(y1 - y0)}  # y0 = north edge
south, north = lat0 + y0 / ky, lat0 + y1 / ky
west, east = lon0 + x0 / kx, lon0 + x1 / kx
bb = f'{south:.6f},{west:.6f},{north:.6f},{east:.6f}'
q = f'''[out:json][timeout:170];(
way["highway"]({bb});
way["building"]({bb});
way["natural"="water"]({bb}); relation["natural"="water"]({bb});
way["waterway"~"^(river|canal|stream)$"]({bb});
way["leisure"~"^(park|garden|pitch|playground)$"]({bb});
way["landuse"~"^(grass|forest|recreation_ground|meadow|village_green|cemetery)$"]({bb});
way["railway"="rail"]({bb});
);out geom;'''
osm_f = f'{S}/osm_{slug}.json'
if not os.path.exists(osm_f):
    d = get('https://maps.mail.ru/osm/tools/overpass/api/interpreter', data=urllib.parse.urlencode({'data': q}).encode())
    json.dump(d, open(osm_f, 'w'))
d = json.load(open(osm_f))
print('elements', len(d['elements']))

# SVG in metres: x east, y south (so north is up).
PX = 1.25  # pixels per metre in the image
W, H = (x1 - x0) * PX, (y1 - y0) * PX
def path(geom, close=False):
    pts = [((lon0 + 0) , 0)]  # placeholder
    p = [m(g['lon'], g['lat']) for g in geom]
    p = rdp(p, 0.6)
    s = 'M' + ' L'.join(f'{(x - x0) * PX:.1f},{(y1 - y) * PX:.1f}' for x, y in p)
    return s + (' Z' if close else '')
ROAD = {'motorway': 24, 'trunk': 22, 'primary': 20, 'secondary': 17, 'tertiary': 14, 'unclassified': 10, 'residential': 10,
        'living_street': 9, 'pedestrian': 9, 'service': 6, 'motorway_link': 12, 'trunk_link': 12, 'primary_link': 12,
        'secondary_link': 11, 'tertiary_link': 10, 'footway': 3.5, 'cycleway': 3.5, 'path': 3, 'steps': 3}
layers = {'green': [], 'water': [], 'building': [], 'rail': [], 'waterline': []}
roads = []
for e in d['elements']:
    t = e.get('tags', {})
    geoms = []
    if e['type'] == 'way' and 'geometry' in e: geoms = [e['geometry']]
    elif e['type'] == 'relation':
        geoms = [mm['geometry'] for mm in e.get('members', []) if mm.get('role') == 'outer' and 'geometry' in mm]
    for g in geoms:
        if len(g) < 2: continue
        if 'highway' in t:
            w = ROAD.get(t['highway'])
            if w: roads.append((w, path(g)))
        elif 'building' in t: layers['building'].append(path(g, True))
        elif t.get('natural') == 'water': layers['water'].append(path(g, True))
        elif 'waterway' in t: layers['waterline'].append((14 if t['waterway'] in ('river', 'canal') else 5, path(g)))
        elif 'railway' in t: layers['rail'].append(path(g))
        else: layers['green'].append(path(g, True))
roads.sort(key=lambda r: r[0])
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">',
       f'<rect width="{W:.0f}" height="{H:.0f}" fill="#E7EBF3"/>',
       '<g fill="#CDEBDF">' + ''.join(f'<path d="{p}"/>' for p in layers['green']) + '</g>',
       '<g fill="#BFE5EE">' + ''.join(f'<path d="{p}"/>' for p in layers['water']) + '</g>',
       ''.join(f'<path d="{p}" fill="none" stroke="#BFE5EE" stroke-width="{w * PX:.1f}" stroke-linecap="round" stroke-linejoin="round"/>' for w, p in layers['waterline']),
       '<g fill="#D8DEEA">' + ''.join(f'<path d="{p}"/>' for p in layers['building']) + '</g>',
       ''.join(f'<path d="{p}" fill="none" stroke="#C3CAD8" stroke-width="{3 * PX:.1f}" stroke-dasharray="{8 * PX:.0f} {6 * PX:.0f}"/>' for p in layers['rail']),
       ''.join(f'<path d="{p}" fill="none" stroke="#FFFFFF" stroke-width="{w * PX:.1f}" stroke-linecap="round" stroke-linejoin="round"/>' for w, p in roads),
       '</svg>']
svg_f = f'{S}/kaart_{slug}.svg'
open(svg_f, 'w').write(''.join(svg))
out['png'] = {'w': round(W), 'h': round(H)}
json.dump(out, open(f'{S}/kaart_{slug}.json', 'w'))
print(json.dumps({k: v for k, v in out.items() if k != 'parkings'}), [(p['locatie'], p['m'], p['min'], len(p['route'])) for p in out['parkings']], os.path.getsize(svg_f))
