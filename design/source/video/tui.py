import math, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/workspace/work/septum/video')
FD = '/workspace/work/septum/'
CW, CH = 12, 24
COLS, ROWS = 148, 40
FS = 20
FONT = ImageFont.truetype(FD + 'JetBrainsMono-Regular.ttf', FS)
FONTB = ImageFont.truetype(FD + 'JetBrainsMono-Medium.ttf', FS)
FONTI = ImageFont.truetype(FD + 'Inter-SemiBold.ttf', 16)

def hx(c): c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
BG = hx('0B0D12'); BAR = hx('141720'); SEL = hx('1B1F2A'); LINE = hx('2A2F3B')
TXT = hx('F3F1EC'); MUT = hx('9AA0AC'); DIM = hx('5E6573'); RED = hx('E5484D'); GRN = hx('4CC38A'); AMB = hx('E2A33B')
def mix(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))

# single: (u,d,l,r)
SINGLE = {'─': (0, 0, 1, 1), '│': (1, 1, 0, 0), '├': (1, 1, 0, 1), '┤': (1, 1, 1, 0), '┬': (0, 1, 1, 1), '┴': (1, 0, 1, 1), '┼': (1, 1, 1, 1),
          '┌': (0, 1, 0, 1), '┐': (0, 1, 1, 0), '└': (1, 0, 0, 1), '┘': (1, 0, 1, 0)}
DOUBLE = {'═': (0, 0, 1, 1), '║': (1, 1, 0, 0), '╔': (0, 1, 0, 1), '╗': (0, 1, 1, 0), '╚': (1, 0, 0, 1), '╝': (1, 0, 1, 0)}
ROUND = {'╭': (0, 1, 0, 1), '╮': (0, 1, 1, 0), '╰': (1, 0, 0, 1), '╯': (1, 0, 1, 0)}

class Scr:
    def __init__(s):
        s.ch = [[' '] * COLS for _ in range(ROWS)]
        s.fg = [[TXT] * COLS for _ in range(ROWS)]
        s.bg = [[BG] * COLS for _ in range(ROWS)]
        s.b = [[False] * COLS for _ in range(ROWS)]
        s.px = []  # half-block pixels: (col,row,topcol,botcol)
    def put(s, x, y, txt, fg=TXT, bg=None, bold=False):
        for i, c in enumerate(txt):
            xx = x + i
            if 0 <= xx < COLS and 0 <= y < ROWS:
                s.ch[y][xx] = c; s.fg[y][xx] = fg; s.b[y][xx] = bold
                if bg is not None: s.bg[y][xx] = bg
        return x + len(txt)
    def fill(s, x, y, w, h, bg, ch=' '):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if 0 <= xx < COLS and 0 <= yy < ROWS: s.bg[yy][xx] = bg; s.ch[yy][xx] = ch
    def box(s, x, y, w, h, title='', col=LINE, tcol=MUT, right='', clear=True):
        if clear: s.fill(x, y, w, h, BG)
        for xx in range(x + 1, x + w - 1): s.put(xx, y, '─', col); s.put(xx, y + h - 1, '─', col)
        for yy in range(y + 1, y + h - 1): s.put(x, yy, '│', col); s.put(x + w - 1, yy, '│', col)
        s.put(x, y, '╭', col); s.put(x + w - 1, y, '╮', col); s.put(x, y + h - 1, '╰', col); s.put(x + w - 1, y + h - 1, '╯', col)
        if title: s.put(x + 2, y, f' {title} ', tcol, bold=True)
        if right: s.put(x + w - 3 - len(right), y, f' {right} ', DIM)
    def runs(s, segs, x, y):
        for txt, fg, *rest in segs:
            x = s.put(x, y, txt, fg, rest[0] if rest else None, rest[1] if len(rest) > 1 else False)
        return x

def render(scr, ox, oy, img):
    d = ImageDraw.Draw(img)
    for y in range(ROWS):
        x = 0
        while x < COLS:
            c = scr.bg[y][x]; x2 = x
            while x2 < COLS and scr.bg[y][x2] == c: x2 += 1
            if c != BG: d.rectangle([ox + x * CW, oy + y * CH, ox + x2 * CW - 1, oy + (y + 1) * CH - 1], fill=c)
            x = x2
    for (cx, cy, top, bot) in scr.px:
        X, Y = ox + cx * CW, oy + cy * CH
        if top: d.rectangle([X, Y, X + CW - 1, Y + CH // 2 - 1], fill=top)
        if bot: d.rectangle([X, Y + CH // 2, X + CW - 1, Y + CH - 1], fill=bot)
    for y in range(ROWS):
        x = 0
        while x < COLS:
            ch = scr.ch[y][x]
            X, Y = ox + x * CW, oy + y * CH; col = scr.fg[y][x]; mx, my = X + CW // 2, Y + CH // 2
            if ch == ' ': x += 1; continue
            if ch in SINGLE:
                u, dn, l, r = SINGLE[ch]
                if l: d.line([X, my, mx, my], col, 2)
                if r: d.line([mx, my, X + CW, my], col, 2)
                if u: d.line([mx, Y, mx, my], col, 2)
                if dn: d.line([mx, my, mx, Y + CH], col, 2)
                x += 1; continue
            if ch in ROUND:
                u, dn, l, r = ROUND[ch]; R = 6
                if r and dn: d.line([mx + R, my, X + CW, my], col, 2); d.line([mx, my + R, mx, Y + CH], col, 2); d.arc([mx, my, mx + 2 * R, my + 2 * R], 180, 270, col, 2)
                if l and dn: d.line([X, my, mx - R, my], col, 2); d.line([mx, my + R, mx, Y + CH], col, 2); d.arc([mx - 2 * R, my, mx, my + 2 * R], 270, 360, col, 2)
                if r and u: d.line([mx + R, my, X + CW, my], col, 2); d.line([mx, Y, mx, my - R], col, 2); d.arc([mx, my - 2 * R, mx + 2 * R, my], 90, 180, col, 2)
                if l and u: d.line([X, my, mx - R, my], col, 2); d.line([mx, Y, mx, my - R], col, 2); d.arc([mx - 2 * R, my - 2 * R, mx, my], 0, 90, col, 2)
                x += 1; continue
            if ch in DOUBLE:
                o = 3; L = X + CW; B = Y + CH
                P = {'═': [[(X, my - o), (L, my - o)], [(X, my + o), (L, my + o)]],
                     '║': [[(mx - o, Y), (mx - o, B)], [(mx + o, Y), (mx + o, B)]],
                     '╔': [[(L, my - o), (mx - o, my - o), (mx - o, B)], [(L, my + o), (mx + o, my + o), (mx + o, B)]],
                     '╗': [[(X, my - o), (mx + o, my - o), (mx + o, B)], [(X, my + o), (mx - o, my + o), (mx - o, B)]],
                     '╚': [[(mx - o, Y), (mx - o, my + o), (L, my + o)], [(mx + o, Y), (mx + o, my - o), (L, my - o)]],
                     '╝': [[(mx + o, Y), (mx + o, my + o), (X, my + o)], [(mx - o, Y), (mx - o, my - o), (X, my - o)]]}[ch]
                for pl in P: d.line(pl, col, 2)
                x += 1; continue
            if ch == '█': d.rectangle([X, Y, X + CW - 1, Y + CH - 1], fill=col); x += 1; continue
            if ch == '▀': d.rectangle([X, Y, X + CW - 1, Y + CH // 2 - 1], fill=col); x += 1; continue
            if ch == '▄': d.rectangle([X, Y + CH // 2, X + CW - 1, Y + CH - 1], fill=col); x += 1; continue
            if ch in '▁▂▃▄▅▆▇':
                hgt = ('▁▂▃▄▅▆▇'.index(ch) + 1) * CH // 8; d.rectangle([X + 1, Y + CH - hgt, X + CW - 2, Y + CH - 1], fill=col); x += 1; continue
            # text run with same fg/bold and no special chars
            x2 = x; bb = scr.b[y][x]
            while x2 < COLS and scr.fg[y][x2] == col and scr.b[y][x2] == bb and scr.ch[y][x2] not in SINGLE and scr.ch[y][x2] not in ROUND and scr.ch[y][x2] not in DOUBLE and scr.ch[y][x2] not in '█▀▄▁▂▃▅▆▇': x2 += 1
            txt = ''.join(scr.ch[y][x:x2])
            # draw char by char positions to keep grid exact (font is mono at 12px so run is fine)
            d.text((X, Y - 2), txt, fill=col, font=FONTB if bb else FONT)
            x = x2

W, H = 1920, 1080
WX, WY = (W - (COLS * CW + 24)) // 2, 28
def window(scr, title='septum — 148×40'):
    img = Image.new('RGB', (W, H), hx('07080B'))
    d = ImageDraw.Draw(img)
    ww, wh = COLS * CW + 24, ROWS * CH + 24 + 36
    d.rounded_rectangle([WX + 6, WY + 10, WX + ww + 6, WY + wh + 14], 16, fill=hx('030305'))
    d.rounded_rectangle([WX, WY, WX + ww, WY + wh], 14, fill=BG, outline=hx('22262F'), width=2)
    d.rounded_rectangle([WX + 1, WY + 1, WX + ww - 1, WY + 36], 14, fill=hx('12141A'))
    d.rectangle([WX + 1, WY + 20, WX + ww - 1, WY + 36], fill=hx('12141A'))
    for i, c in enumerate(['FF5F57', 'FEBC2E', '28C840']): d.ellipse([WX + 16 + i * 22, WY + 12, WX + 28 + i * 22, WY + 24], fill=hx(c))
    tw_ = d.textlength(title, font=FONTI); d.text((WX + ww / 2 - tw_ / 2, WY + 9), title, fill=DIM, font=FONTI)
    render(scr, WX + 12, WY + 36 + 12, img)
    d.text((WX + ww - 20 - d.textlength('DESIGN PREVIEW · v0.1 SPEC', font=FONTI), WY + 9), 'DESIGN PREVIEW · v0.1 SPEC', fill=hx('3A3F4B'), font=FONTI)
    return img
