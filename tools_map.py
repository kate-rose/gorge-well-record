"""Build assets/_map.svg: the six Gorge counties and every oil/gas test well on record there."""
import geopandas as gpd, math
from shapely.geometry import box
c = gpd.read_file('assets/_counties.geojson'); nsa = gpd.read_file('assets/_nsa.geojson')
GORGE = {'53011','53059','53039','41051','41027','41065'}
minx, miny, maxx, maxy = -122.95, 45.30, -119.95, 46.42
k = math.cos(math.radians((miny+maxy)/2)); W = 1000; sx = W/((maxx-minx)*k); H = round((maxy-miny)*sx)
def P(x, y): return (round((x-minx)*k*sx, 1), round((maxy-y)*sx, 1))
def path(g):
    out = []
    for p in ([g] if g.geom_type == 'Polygon' else [q for q in getattr(g, 'geoms', []) if q.geom_type == 'Polygon']):
        for ring in [p.exterior] + list(p.interiors):
            out.append('M' + ' L'.join(f'{a},{b}' for a, b in (P(x, y) for x, y in ring.coords)) + 'Z')
    return ' '.join(out)
clip = box(minx, miny, maxx, maxy)
# (label, lon, lat, status: open|closed, approx: bool, label dx, dy, anchor)
wells = [
 ('Kady-Olsen, 1949', -122.028984, 45.621607, 'open', False, -14, -16, 'end'),
 ('Gas-Ice ×3, 1931', -121.124, 45.8225, 'open', False, 0, -18, 'middle'),
 ('Aldercreek, 1937', -120.10136, 45.917436, 'open', False, -14, 26, 'end'),
 ('Gray 31-23, 2008', -120.107635, 45.95973, 'closed', False, -14, -12, 'end'),
 ('Benedict, 1959', -122.688823, 45.816707, 'open', False, 14, -12, 'start'),
 ('Barber, 1946', -122.767822, 45.554958, 'closed', False, 14, 22, 'start'),
 ('Kappler, 1957', -122.884903, 45.673191, 'closed', False, 14, -12, 'start'),
 ('Water well that hit gas, 1949', -122.51209, 45.46465, 'open', False, 14, 22, 'start'),
 ('Lambert, 1952', -121.32, 45.382, 'closed', False, 14, 22, 'start'),
 ('Beavis May ×2, 1907, 1919', -121.33, 45.45, 'open', True, -20, -16, 'end'),
 ('Dufur Oil Co. ×5, before 1907', -121.23, 45.445, 'open', True, 16, 24, 'start'),
]
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="map-title map-desc">',
 '<title id="map-title">Oil and gas test wells on record in the six Columbia River Gorge counties</title>',
 '<desc id="map-desc">Map of Clark, Skamania and Klickitat counties in Washington and Multnomah, Hood River and Wasco counties in Oregon, with the National Scenic Area outlined along the river. Only the 1949 Kady-Olsen well near Beacon Rock falls inside the Scenic Area. Others sit near Klickitat, Alderdale, north Clark County, Portland, and west of Dufur.</desc>']
for _, r in c.iterrows():
    g = r.geometry.intersection(clip)
    if g.is_empty: continue
    svg.append(f'<path class="cty{" focus" if r.GEOID in GORGE else ""}" d="{path(g)}"/>')
svg.append(f'<path class="nsa" d="{path(nsa.geometry.iloc[0].intersection(clip))}"/>')
for name, x, y in [('CLARK', -122.50, 45.88), ('SKAMANIA', -121.95, 46.18), ('KLICKITAT', -120.72, 46.05),
                   ('MULTNOMAH', -122.20, 45.50), ('HOOD RIVER', -121.66, 45.345), ('WASCO', -120.98, 45.535)]:
    a, b = P(x, y); svg.append(f'<text class="cname" x="{a}" y="{b}">{name}</text>')
for lab, x, y, st, approx, dx, dy, anc in wells:
    a, b = P(x, y)
    if approx: svg.append(f'<circle class="approx" cx="{a}" cy="{b}" r="17"/>')
    svg.append(f'<circle class="well {st}" cx="{a}" cy="{b}" r="7.5"/>')
    svg.append(f'<text class="wl" x="{a+dx}" y="{b+dy}" text-anchor="{anc}">{lab}</text>')
svg.append(f'<g class="key" transform="translate(14,30)"><line x1="0" y1="-6" x2="28" y2="-6" class="nsa"/><text x="36" y="0">National Scenic Area</text></g>')
svg.append('</svg>')
open('assets/_map.svg', 'w').write('\n'.join(svg)); print(W, H)
