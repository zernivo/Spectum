import math, os, sys, subprocess, cairosvg
from shapely.geometry import Polygon
from shapely.ops import unary_union
import naut3 as N

S = 512
shapes, NCH = N.build(S)
EYE = N.EYE
KEYS = [k for k, _ in shapes]           # 'core', 0..n-1
RED = NCH - 3
raws = {}
# silhouette pieces per chamber (no gaps) for partial unions
_sh, _ = N.raw_shapes()
pts = [p for _, s in _sh for p in s]; xs, ys = zip(*pts)
sc = 360 / max(max(xs) - min(xs), max(ys) - min(ys)); cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
for key, s in _sh:
    raws[key] = Polygon([((x - cx) * sc + S / 2, (y - cy) * sc + S / 2) for x, y in s]).buffer(0.6)
def sil(keys):
    u = unary_union([raws[k] for k in keys])
    return u.buffer(-10, join_style=1).buffer(10, join_style=1, quad_segs=12)
FULL_SIL = sil(KEYS)
D = N.d_of
TEXT = None
try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    f = TTFont('/workspace/work/eigen/Inter-Bold.ttf'); gs = f.getGlyphSet(); cmap = f.getBestCmap(); hm = f['hmtx']
    def tp(txt, size, x, y, spacing=0, anchor='middle'):
        scl = size / f['head'].unitsPerEm
        w = sum(hm[cmap[ord(c)]][0] * scl + spacing for c in txt) - spacing
        if anchor == 'middle': x -= w / 2
        pen = SVGPathPen(gs); cx_ = x
        for c in txt:
            g = cmap[ord(c)]; gs[g].draw(TransformPen(pen, (scl, 0, 0, -scl, cx_, y))); cx_ += hm[g][0] * scl + spacing
        return pen.getCommands()
    TEXT = tp
except Exception as e:
    print('no text', e)

DEFS = (f'<defs><radialGradient id="face" gradientUnits="userSpaceOnUse" cx="{EYE[0]:.1f}" cy="{EYE[1]:.1f}" r="230"><stop offset="0" stop-color="#C9C2B6"/><stop offset=".45" stop-color="#E4DFD6"/><stop offset="1" stop-color="#FBF8F3"/></radialGradient>'
        '<linearGradient id="red" x1="0" y1="0" x2=".4" y2="1"><stop offset="0" stop-color="#FF7C80"/><stop offset="1" stop-color="#D23840"/></linearGradient>'
        '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<radialGradient id="rglow"><stop offset="0" stop-color="#E5484D" stop-opacity=".5"/><stop offset="1" stop-color="#E5484D" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="shadow"><stop offset="0" stop-color="#000" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>')

def ease_out(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def ease_io(t): t = max(0, min(1, t)); return 3 * t * t - 2 * t * t * t
def back_out(t, s=1.7): t = max(0, min(1, t)) - 1; return 1 + (s + 1) * t ** 3 + s * t ** 2

def frame(vis=None, red=None, depth=13, rot=0.0, scale=1.0, glow=None, shadow=1.0, word=0.0, H=S, W=S, ox=0, oy=0):
    """vis: key -> (alpha, scale). red: key -> 0..1 crimson amount."""
    vis = vis or {k: (1, 1) for k in KEYS}
    red = red if red is not None else {RED: 1}
    shown = [k for k in KEYS if vis.get(k, (0, 0))[0] > 0.55]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', DEFS, f'<rect width="{W}" height="{H}" fill="#0B0D12"/>']
    o.append(f'<g transform="translate({ox},{oy})">')
    if shadow > 0:
        o.append(f'<ellipse cx="{S/2}" cy="{S/2+188}" rx="{170*scale}" ry="{20*scale}" fill="url(#shadow)" opacity="{shadow:.2f}"/>')
    o.append(f'<g transform="translate({EYE[0]:.1f},{EYE[1]:.1f}) rotate({rot:.2f}) scale({scale:.4f}) translate({-EYE[0]:.1f},{-EYE[1]:.1f})">')
    if shown:
        sl = FULL_SIL if len(shown) == len(KEYS) else sil(shown)
        dd = D(sl)
        for i in range(int(round(depth)), 0, -1):
            col = '#6F6A62' if i > depth * 0.6 else '#8D877E'
            o.append(f'<path d="{dd}" fill="{col}" transform="translate(0,{i})"/>')
        o.append(f'<path d="{dd}" fill="#A39C91"/>')
    gl = glow if glow is not None else {RED: 1}
    for key, g in shapes:
        a, s = vis.get(key, (0, 0))
        if a <= 0.01: continue
        c = g.centroid
        tr = f'translate({c.x:.1f},{c.y:.1f}) scale({s:.3f}) translate({-c.x:.1f},{-c.y:.1f})'
        if gl.get(key, 0) > 0.01:
            o.append(f'<circle cx="{c.x:.1f}" cy="{c.y:.1f}" r="85" fill="url(#rglow)" opacity="{gl[key]*a:.2f}"/>')
        o.append(f'<g transform="{tr}" opacity="{a:.3f}"><path d="{D(g)}" fill="url(#face)"/>')
        r = red.get(key, 0)
        if r > 0.01: o.append(f'<path d="{D(g)}" fill="url(#red)" opacity="{r:.3f}"/>')
        o.append('</g>')
    if shown:
        o.append(f'<path d="{D(sl)}" fill="url(#sheen)"/><path d="{D(sl)}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.6"/>')
    o.append('</g></g>')
    if word > 0.01 and TEXT:
        y = H - 70 + (1 - ease_out(word)) * 14
        o.append(f'<path d="{TEXT("Septum", 64, W/2, y)}" fill="#F3F1EC" opacity="{ease_out(word):.3f}"/>')
    o.append('</svg>')
    return ''.join(o)

def render(name, frames, fps=30, size=512):
    d = f'/workspace/work/septum/frames_{name}'; os.makedirs(d, exist_ok=True)
    for f_ in os.listdir(d): os.remove(os.path.join(d, f_))
    for i, svg in enumerate(frames):
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f'{d}/{i:04d}.png', output_width=size)
    out = '/workspace/projects/8b93207f-c8f7-4b8e-9664-f106dd0c8bea/files/outputs/septum/anim'
    os.makedirs(out, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{d}/%04d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', f'{out}/septum-{name}.mp4'], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{d}/%04d.png', '-vf', 'scale=360:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=sierra2_4a', '-loop', '0', f'{out}/septum-{name}.gif'], check=True)
    return d

FPS = 30
CH = [k for k in KEYS if k != 'core']   # chamber order inner -> outer

def loading():
    # crimson "seal" travels chamber to chamber, inner -> outer, then the shell breathes; seamless loop
    n = 48; frames = []
    order = ['core'] + CH
    L = len(order)
    for i in range(n):
        p = i / n * L
        red, glow = {}, {}
        for j, k in enumerate(order):
            dist = (p - j) % L
            amt = max(0, 1 - dist / 2.2) if dist >= 0 else 0
            amt = amt ** 1.6
            red[k] = amt; glow[k] = amt * 0.8
        frames.append(frame(red=red, glow=glow))
    return frames

def intro():
    frames = []
    T = int(3.4 * FPS)
    order = ['core'] + CH
    L = len(order)
    for i in range(T):
        t = i / FPS
        vis = {}
        for j, k in enumerate(order):
            st = 0.15 + j * 0.075
            u = (t - st) / 0.35
            if u <= 0: continue
            vis[k] = (ease_out(u), 0.6 + 0.4 * back_out(u))
        depth = 13 * ease_out((t - 1.6) / 0.5)
        r = ease_io((t - 2.05) / 0.35)
        pulse = math.exp(-((t - 2.45) / 0.25) ** 2)
        red = {RED: r}
        glow = {RED: r * 0.8 + pulse * 0.9}
        scale = 0.92 + 0.08 * ease_out(t / 2.0)
        rot = -35 * (1 - ease_out(t / 2.2))
        frames.append(frame(vis=vis, red=red, depth=max(0, depth), rot=rot, scale=scale, glow=glow,
                            shadow=ease_out((t - 1.4) / 0.6), word=(t - 2.5) / 0.6, H=S + 90, oy=0))
    for _ in range(int(0.8 * FPS)): frames.append(frames[-1])
    return frames

def regular():
    frames = []
    T = int(1.4 * FPS)
    for i in range(T):
        t = i / FPS
        sc = 0.86 + 0.14 * back_out(t / 0.55, 1.3)
        rot = -18 * (1 - ease_out(t / 0.6))
        a = ease_out(t / 0.3)
        vis = {k: (a, 1) for k in KEYS}
        r = ease_io((t - 0.45) / 0.25)
        pulse = math.exp(-((t - 0.75) / 0.18) ** 2)
        frames.append(frame(vis=vis, red={RED: r}, glow={RED: r * 0.8 + pulse}, rot=rot, scale=sc, shadow=a))
    for _ in range(int(0.6 * FPS)): frames.append(frames[-1])
    return frames

if __name__ == '__main__':
    which = sys.argv[1:] or ['loading', 'intro', 'regular']
    for w in which:
        print(w, render(w, globals()[w]()))
