import math, base64, os
from PIL import ImageFont
W, H, FPS = 1920, 1080, 30
BG = '#0B0D12'; PANEL = '#141720'; PANEL2 = '#1B1F2A'; LINE = '#2A2F3B'
TXT = '#F3F1EC'; MUT = '#9AA0AC'; DIM = '#5E6573'; RED = '#E5484D'; GRN = '#4CC38A'; AMB = '#E2A33B'
FD = '/workspace/work/septum/'
_F = {('Inter', 400): FD + 'Inter-Regular.ttf', ('Inter', 600): FD + 'Inter-SemiBold.ttf', ('Inter', 700): FD + 'Inter-Bold.ttf',
      ('JetBrains Mono', 400): FD + 'JetBrainsMono-Regular.ttf', ('JetBrains Mono', 500): FD + 'JetBrainsMono-Medium.ttf'}
_fc = {}
def tw(s, size, fam='Inter', wt=400):
    k = (fam, wt, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(_F[(fam, wt)], size)
    return _fc[k].getlength(s)
MARK = base64.b64encode(open(FD + 'mark512.png', 'rb').read()).decode()

def cl(x, a=0., b=1.): return max(a, min(b, x))
def seg(t, a, b): return cl((t - a) / (b - a)) if b > a else float(t >= a)
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x, s=1.6): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
def lerp(a, b, x): return a + (b - a) * x

def text(x, y, s, size=32, wt=400, fill=TXT, op=1, anchor='start', fam='Inter', ls=0):
    if op <= 0.003 or not s: return ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-weight="{wt}" font-size="{size}" fill="{fill}" '
            f'opacity="{op:.3f}" text-anchor="{anchor}" letter-spacing="{ls}" xml:space="preserve">{esc(s)}</text>')
def mono(x, y, s, size=26, fill=TXT, op=1, wt=400, anchor='start'):
    return text(x, y, s, size, wt, fill, op, anchor, 'JetBrains Mono')
def rr(x, y, w, h, r=18, fill=PANEL, stroke=None, sw=2, op=1, extra=''):
    if op <= 0.003: return ''
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" rx="{r}" fill="{fill}"{st} opacity="{op:.3f}" {extra}/>'
def circ(x, y, r, fill, op=1, stroke=None, sw=2):
    if op <= 0.003: return ''
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(r,0):.1f}" fill="{fill}"{st} opacity="{op:.3f}"/>'
def line(x1, y1, x2, y2, col=LINE, sw=3, op=1, dash=None):
    if op <= 0.003: return ''
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" opacity="{op:.3f}"{d}/>'
def arrow(x1, y1, x2, y2, col=DIM, sw=3, op=1, p=1):
    if op <= 0.003 or p <= 0: return ''
    x2 = lerp(x1, x2, p); y2 = lerp(y1, y2, p)
    a = math.atan2(y2 - y1, x2 - x1); L = 14
    h1 = (x2 - L * math.cos(a - .45), y2 - L * math.sin(a - .45)); h2 = (x2 - L * math.cos(a + .45), y2 - L * math.sin(a + .45))
    return line(x1, y1, x2, y2, col, sw, op) + f'<path d="M{h1[0]:.1f},{h1[1]:.1f} L{x2:.1f},{y2:.1f} L{h2[0]:.1f},{h2[1]:.1f}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" opacity="{op:.3f}"/>'
def mark(cx, cy, size, op=1, rot=0):
    if op <= 0.003: return ''
    return (f'<g opacity="{op:.3f}" transform="rotate({rot:.2f} {cx:.1f} {cy:.1f})"><image x="{cx-size/2:.1f}" y="{cy-size/2:.1f}" width="{size:.1f}" height="{size:.1f}" '
            f'xlink:href="data:image/png;base64,{MARK}"/></g>')
def g(content, op=1, dx=0, dy=0, sc=1, cx=0, cy=0):
    if op <= 0.003 or not content: return ''
    tr = f'translate({dx:.1f},{dy:.1f})'
    if sc != 1: tr += f' translate({cx:.1f},{cy:.1f}) scale({sc:.4f}) translate({-cx:.1f},{-cy:.1f})'
    return f'<g opacity="{op:.3f}" transform="{tr}">{content}</g>'
def typed(s, t, a, cps=40):
    n = int(cl((t - a) * cps, 0, len(s))); return s[:n]
def chip(x, y, s, col, size=22, op=1, fillop=.16, anchor='start', fam='Inter', wt=600):
    w = tw(s, size, fam, wt) + size * 1.2; h = size * 1.75
    if anchor == 'middle': x -= w / 2
    return rr(x, y - h * .7, w, h, h / 2, col, op=op * fillop) + rr(x, y - h * .7, w, h, h / 2, 'none', col, 1.5, op * .7) + text(x + size * .6, y + size * .02, s, size, wt, col, op, fam=fam)
def chapter(n, title, t, dur):
    o = cl(seg(t, 0, .5)) * (1 - seg(t, dur - .4, dur))
    return text(96, 92, f'{n}', 22, 700, RED, o, ls=3) + text(140, 92, title.upper(), 22, 600, MUT, o, ls=3)
def caption(s, t, a, b, y=980, size=34, col=TXT):
    o = seg(t, a, a + .4) * (1 - seg(t, b - .3, b))
    return text(W / 2, y + 10 * (1 - eo(seg(t, a, a + .4))), s, size, 400, col, o, 'middle')
def frame(body, scene_op=1):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>'
            f'<defs><radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>'
            f'<radialGradient id="rg"><stop offset="0" stop-color="{RED}" stop-opacity=".5"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient></defs>'
            f'<g opacity="{scene_op:.3f}">{body}</g><rect width="{W}" height="{H}" fill="url(#vig)"/>'
            + text(W - 96, H - 48, 'DESIGN PREVIEW · v0.1 SPEC', 16, 600, DIM, .8, 'end', ls=2) + '</svg>')
def cursor(x, y, op=1, down=0):
    if op <= 0.003: return ''
    s = 1 - .15 * down
    return (f'<g opacity="{op:.3f}" transform="translate({x:.1f},{y:.1f}) scale({s:.3f})"><path d="M0,0 L0,30 L8,23 L14,36 L19,34 L13,21 L24,21 Z" fill="#fff" stroke="#000" stroke-width="1.5" stroke-linejoin="round"/></g>'
            + (circ(x, y, 26 * down, RED, .35 * down) if down else ''))

def render(scenes, outdir, start=0, step=1):
    """scenes: list of (dur, fn(t,dur)->svg body). renders frames start::step"""
    import cairosvg
    os.makedirs(outdir, exist_ok=True)
    total = sum(d for d, _ in scenes); n = int(round(total * FPS))
    for i in range(start, n, step):
        T = i / FPS; acc = 0
        for d, fn in scenes:
            if T < acc + d or (d, fn) == scenes[-1]:
                t = T - acc; break
            acc += d
        op = seg(t, 0, .35) * (1 - seg(t, d - .35, d))
        if (d, fn) == scenes[0]: op = 1 - seg(t, d - .35, d)
        if (d, fn) == scenes[-1]: op = seg(t, 0, .35)
        svg = frame(fn(t, d), op)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=f'{outdir}/f{i:05d}.png')
    return n
