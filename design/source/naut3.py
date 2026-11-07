import math, cairosvg
from shapely.geometry import Polygon
from shapely.ops import unary_union

GROW = 2.5; TURNS = 1.6; NPER = 10; BULGE = 0.26
b = math.log(GROW) / (2 * math.pi)
R = lambda t: math.exp(b * t)
T_END = 6 * math.pi
T0 = T_END - TURNS * 2 * math.pi
STEP = 2 * math.pi / NPER

def P(t, r): return (r * math.cos(t), r * math.sin(t))
def septum(T, n=12):  # from outer (R(T)) to inner (R(T-2pi)), bulging forward
    return [P(T + BULGE * math.sin(math.pi * u), R(T) * (1 - u) + R(T - 2 * math.pi) * u) for u in [i / n for i in range(n + 1)]]
def arc(ta, tb, off=0, n=30):
    return [P(t, R(t - off)) for t in [ta + (tb - ta) * i / n for i in range(n + 1)]]

def raw_shapes():
    shapes = []
    core = arc(T0 - 2 * math.pi, T0, 0, 90) + septum(T0)[1:-1]
    shapes.append(('core', core))
    n = int(round(TURNS * NPER))
    for k in range(n):
        ta, tb = T0 + k * STEP, T0 + (k + 1) * STEP
        outer = arc(ta, tb)
        sb = septum(tb)[1:]
        inner = arc(tb, ta, 2 * math.pi)[1:]
        sa = septum(ta)[::-1][1:-1]
        shapes.append((k, outer + sb + inner + sa))
    return shapes, n

def build(size=512, box=360, gap=3.2, rnd=2.5):
    shapes, n = raw_shapes()
    pts = [p for _, s in shapes for p in s]
    xs, ys = zip(*pts)
    sc = box / max(max(xs) - min(xs), max(ys) - min(ys))
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    global SIL
    raws = [Polygon([((x - cx) * sc + size / 2, (y - cy) * sc + size / 2) for x, y in s]).buffer(0) for _, s in shapes]
    SIL = unary_union([r.buffer(0.6) for r in raws]).buffer(-10, join_style=1).buffer(10, join_style=1, quad_segs=16)
    out = []
    for key, s in shapes:
        poly = Polygon([((x - cx) * sc + size / 2, (y - cy) * sc + size / 2) for x, y in s]).buffer(0)
        g = poly.buffer(-(gap / 2 + rnd), join_style=1).buffer(rnd, join_style=1, quad_segs=16)
        if g.is_empty: continue
        out.append((key, g))
    global EYE
    EYE = ((0 - cx) * sc + size / 2, (0 - cy) * sc + size / 2)
    return out, n

def d_of(g):
    geoms = getattr(g, 'geoms', [g])
    d = ''
    for p in geoms:
        c = list(p.exterior.coords)
        d += 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in c) + 'Z'
    return d

def mark_svg(bg=None, size=512, depth=13, red_k=None, flat=False):
    shapes, n = build(size)
    red = n - 3 if red_k is None else red_k
    union = unary_union([g for _, g in shapes])
    defs = ('<defs>'
            f'<radialGradient id="face" gradientUnits="userSpaceOnUse" cx="{EYE[0]:.1f}" cy="{EYE[1]:.1f}" r="{230*size/512:.1f}"><stop offset="0" stop-color="#C9C2B6"/><stop offset="0.45" stop-color="#E4DFD6"/><stop offset="1" stop-color="#FBF8F3"/></radialGradient>'
            '<linearGradient id="red" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#FF7C80"/><stop offset="1" stop-color="#D23840"/></linearGradient>'
            '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="rglow"><stop offset="0" stop-color="#E5484D" stop-opacity=".45"/><stop offset="1" stop-color="#E5484D" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="shadow"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
            '</defs>')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">', defs]
    if bg: o.append(f'<rect width="{size}" height="{size}" fill="{bg}"/>')
    k = size / 512
    if not flat:
        o.append(f'<ellipse cx="{size/2}" cy="{size/2+188*k}" rx="{170*k}" ry="{20*k}" fill="url(#shadow)"/>')
        # extruded sides: stacked offsets per piece
        for i in range(int(depth * k), 0, -1):
            col = '#6F6A62' if i > depth * k * 0.6 else '#8D877E'
            o.append(f'<path d="{d_of(SIL)}" fill="{col}" transform="translate(0,{i})"/>')
        o.append(f'<path d="{d_of(SIL)}" fill="#A39C91"/>')
        rc = shapes[[s[0] for s in shapes].index(red)][1].centroid
        o.append(f'<circle cx="{rc.x:.1f}" cy="{rc.y:.1f}" r="{85*k:.1f}" fill="url(#rglow)"/>')
    for key, g in shapes:
        o.append(f'<path d="{d_of(g)}" fill="{"url(#red)" if key == red else ("#EDEAE4" if flat else "url(#face)")}"/>')
    if not flat:
        o.append(f'<path d="{d_of(union)}" fill="url(#sheen)"/>')
        # thin top-edge highlight per piece
        for key, g in shapes:
            pass
        o.append(f'<path d="{d_of(SIL)}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{1.6*k:.1f}"/>')
    o.append('</svg>')
    return ''.join(o)

if __name__ == '__main__':
    import os
    os.chdir('/workspace/work/septum')
    for name, bg in [('n3_dark', '#0B0D12'), ('n3_light', '#F3F1EC')]:
        s = mark_svg(bg)
        open(name + '.svg', 'w').write(s)
        cairosvg.svg2png(bytestring=s.encode(), write_to=name + '.png', output_width=1024, output_height=1024)
    print('ok')
