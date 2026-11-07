import sys, math, os
sys.path.insert(0, '/workspace/work/septum/video'); sys.path.insert(0, '/workspace/work/septum')
from tui import *
from PIL import Image
import pyfiglet
BLU = hx('6CB6FF')
def cl(x, a=0., b=1.): return max(a, min(b, x))
def seg(t, a, b): return cl((t - a) / (b - a))
SPIN = '-\\|/-\\|/-\\'

# ---------- logo pixels
import naut3 as N
N.build(512)
_s = Image.open('/workspace/work/septum/video/pixlogo.png').convert('RGBA')
LW, LH = _s.size
EYE = (LW * .42, LH * .55)
LOGO = []
for py in range(LH):
    for px in range(LW):
        r, g_, b, a = _s.getpixel((px, py))
        if a < 70: continue
        k = a / 255; col = mix(BG, (r, g_, b), k)
        LOGO.append((px, py, col, math.hypot(px + .5 - EYE[0], py + .5 - EYE[1])))
RMAX = max(p[3] for p in LOGO)
def draw_logo(scr, x0, y0, p, col_override=None):
    cells = {}
    for px, py, col, r in LOGO:
        if r / RMAX > p: continue
        cells.setdefault((px, py // 2), [None, None])[py % 2] = col
    for (cx, cy), (top, bot) in cells.items():
        scr.px.append((x0 + cx, y0 + cy, top, bot))

WORD = [l for l in pyfiglet.figlet_format('SEPTUM', font='ansi_shadow').split('\n') if l.strip()]
def draw_word(scr, x0, y0, p):
    wcols = int(len(WORD[0]) * p)
    for i, l in enumerate(WORD):
        for j, c in enumerate(l[:wcols]):
            if c == ' ': continue
            scr.put(x0 + j, y0 + i, c, TXT if c == '█' else DIM)

def ctr(scr, y, s, fg=TXT, bold=False): scr.put((COLS - len(s)) // 2, y, s, fg, bold=bold)

# ---------- scene: shell
PROMPT = [('khubaib', GRN), ('@', DIM), ('dev', GRN), (' ~/agent ', BLU), ('$ ', TXT)]
def shell(T, lines_after=None):
    s = Scr()
    s.put(1, 1, '# your agent session runs in another pane', DIM)
    x = s.runs(PROMPT, 1, 3)
    cmd = 'septum'
    n = int(cl((T - .6) * 9, 0, len(cmd)))
    s.put(x, 3, cmd[:n], TXT, bold=True)
    if T < 1.7 and int(T * 2.5) % 2 == 0: s.put(x + n, 3, '█', MUT)
    return s

# ---------- scene: splash
CHECKS = [('policy', '.septum/policy.toml · fail-closed'),
          ('judge', 'local model (auto-detected) · rules'),
          ('upstream', 'playwright-mcp · 21 tools wrapped'),
          ('chambers', '4 loaded · encrypted at rest'),
          ('ledger', 'writing .septum/ledger/2026-11-06.jsonl')]
def splash(t):
    s = Scr()
    draw_logo(s, (COLS - LW) // 2, 1, 1 - (1 - seg(t, .1, 1.5)) ** 2)
    draw_word(s, (COLS - len(WORD[0])) // 2, 24, seg(t, 1.2, 2.0))
    if t > 2.0: ctr(s, 31, 'agent leak firewall · every site is a chamber · v0.1.0', MUT)
    for i, (k, v) in enumerate(CHECKS):
        a = 2.5 + i * .55
        if t < a: continue
        done = t > a + .45
        s.put(50, 33 + i, ('✓' if done else SPIN[int(t * 12) % 10]), GRN if done else AMB, bold=True)
        s.put(53, 33 + i, f'{k:<10}', TXT, bold=True); s.put(63, 33 + i, v, MUT if done else DIM)
    if t > 5.6: ctr(s, 39, 'guarding · opening dashboard', DIM)
    return s

# ---------- dashboard data
ACTS = [  # u, verdict, verb, value, target
    (0.8, 'allow', 'goto', 'insure.co/quote', 'page'),
    (1.8, 'allow', 'type', '"Islamabad"', '#city'),
    (2.8, 'allow', 'select', '"Corolla 2019"', '#car'),
    (3.8, 'allow', 'click', '"Next"', '#next'),
    (5.0, 'neutral', 'select', '"Diabetes"', '#medical'),
    (9.4, 'allow', 'select', '"Prefer not to say"', '#medical'),
    (11.0, 'ask', 'type', '"+92 3•• ••• •567"', '#phone'),
    (17.0, 'allow', 'click', '"Get quote"', '#submit'),
    (18.2, 'allow', 'read', 'insure.co/result', 'page'),
]
VB = {'allow': ('✓ allow', GRN), 'neutral': ('◆ neutralize', AMB), 'ask': ('? ask', BLU), 'block': ('✕ block', RED)}
def clock(u): sec = 2 + int(u); return f'00:41:{sec:02d}' if sec < 60 else f'00:42:{sec-60:02d}'

def header(s, u, tab):
    s.fill(0, 0, COLS, 1, BAR)
    x = s.put(0, 0, ' ● ', RED, BAR, True)
    x = s.put(x, 0, 'septum ', TXT, BAR, True); x = s.put(x, 0, '0.1 ', DIM, BAR)
    for k, v, c in [('task', '"get a car insurance quote"', TXT), ('upstream', 'playwright-mcp', MUT), ('judge', 'local · 38 ms', MUT), ('mode', 'FAIL-CLOSED', AMB)]:
        x = s.put(x, 0, ' │ ', LINE, BAR); x = s.put(x, 0, k + ' ', DIM, BAR); x = s.put(x, 0, v, c, BAR, c == AMB)
    r = f'● guarding   {clock(u)} '
    s.put(COLS - len(r), 0, '●', GRN if int(u * 2) % 2 == 0 else hx('2E7A57'), BAR); s.put(COLS - len(r) + 1, 0, r[1:], MUT, BAR)
    x = 1
    for i, n in enumerate(['Live', 'Ledger', 'Chambers', 'Policy']):
        lab = f' {i+1} {n} '
        on = tab == i
        x = s.put(x, 1, lab, TXT if on else DIM, mix(BG, RED, .28) if on else None, on) + 1

def footer(s, flash=None, ft=0):
    keys = [('↑↓', 'select'), ('⏎', 'inspect'), ('a', 'allow'), ('d', 'deny'), ('1-4', 'tabs'), ('/', 'filter'), ('e', 'export'), ('q', 'quit')]
    x = 1
    for k, v in keys:
        on = flash == k
        x = s.put(x, 39, f' {k} ', TXT if not on else BG, RED if on else SEL, True)
        x = s.put(x, 39, f' {v}   ', DIM)
    s.put(COLS - 30, 39, 'septum ledger --json to export', DIM)

def chambers_panel(s, u):
    s.box(0, 2, 36, 17, 'CHAMBERS', right='4')
    rows = [('myhealth.portal', RED, 'HIGH', ['diagnosis', 'medication']),
            ('mybank.com', RED, 'HIGH', ['salary', 'balance']),
            ('profile', AMB, 'MED', ['phone', 'email', 'address']),
            ('insure.co', GRN, 'TASK', ['city', 'car'] + (['quote'] if u > 18.4 else []))]
    y = 4
    for n, c, sv, facts in rows:
        s.put(2, y, '●', c); s.put(4, y, n, TXT, bold=True); s.put(33 - len(sv), y, sv, c, bold=True)
        hot = (n == 'myhealth.portal' and 5.0 < u < 9.4) or (n == 'profile' and 11 < u < 15.8)
        if hot: s.fill(1, y, 34, 1, mix(BG, c, .18)); s.put(2, y, '●', c); s.put(4, y, n, TXT, bold=True); s.put(33 - len(sv), y, sv, c, bold=True)
        fx = 4
        for f in facts:
            lab = f + ' ' + '•' * 4
            if fx + len(lab) > 34: y += 1; fx = 4
            s.put(fx, y + 1, lab, DIM if not (n == 'insure.co' and f == 'quote' and u < 19.4) else GRN); fx += len(lab) + 2
        y += 3
    return s

def stats_panel(s, u):
    s.box(0, 19, 36, 10, 'SESSION')
    seen = [a for a in ACTS if a[0] <= u]
    cnt = {k: sum(1 for a in seen if a[1] == k) for k in VB}
    if u > 15.2: cnt['ask'] = 1
    items = [('checked', len(seen), TXT), ('allowed', cnt['allow'], GRN), ('neutralized', cnt['neutral'], AMB), ('asked you', cnt['ask'], BLU), ('blocked', 0, RED)]
    for i, (k, v, c) in enumerate(items):
        yy = 21 + i // 2; xx = 2 + (i % 2) * 17
        if i == 4: yy, xx = 23, 2
        s.put(xx, yy, f'{v:>2}', c, bold=True); s.put(xx + 3, yy, k, DIM)
    s.put(2, 25, 'actions / sec', DIM)
    bars = '▁▂▃▄▅▆▇'
    for i in range(32):
        tt = u - (31 - i) * .5
        v = sum(math.exp(-((tt - a[0]) * 2.2) ** 2) for a in ACTS) + .15 * (1 + math.sin(i * 1.7 + u))
        s.put(2 + i, 26, bars[min(6, int(v * 4))], RED if i == 31 else mix(DIM, MUT, .5))

def live_panel(s, u, sel=None):
    s.box(36, 2, 62, 27, 'LIVE ACTIONS', right='insure.co')
    s.put(38, 4, 'TIME   VERDICT      ACTION                         TARGET', DIM)
    seen = [a for a in ACTS if a[0] <= u]
    sel = len(seen) - 1 if sel is None else sel
    for i, a in enumerate(seen):
        y = 6 + i * 2
        tu, v, verb, val, tgt = a
        if i == sel:
            s.fill(37, y, 60, 1, SEL); s.put(37, y, '▌', RED)
        age = u - tu
        lab, c = VB[v]
        if v == 'ask' and u > 15.2: lab = '✓ by you'; c = BLU
        fl = c if age < .35 else None
        s.put(38, y, clock(tu)[3:], DIM, SEL if i == sel else None)
        s.put(45, y, f'{lab:<13}', c, SEL if i == sel else None, True)
        s.put(58, y, f'{verb:<7}', MUT, SEL if i == sel else None)
        s.put(65, y, f'{val:<22}', TXT, SEL if i == sel else None)
        s.put(88, y, tgt, DIM, SEL if i == sel else None)
        if v == 'neutral' and u > 8.5:
            s.put(58, y + 1, '└─ rewritten to "Prefer not to say"', AMB)
    if u < 19.5 and seen:
        s.put(38, 6 + len(seen) * 2, SPIN[int(u * 12) % 10] + ' waiting for next action from agent…', DIM)
    return sel

def inspector(s, u, a):
    s.box(98, 2, 50, 27, 'INSPECTOR', RED if a and a[1] in ('neutral', 'ask') else LINE, TXT if a and a[1] != 'allow' else MUT)
    if not a: return
    tu, v, verb, val, tgt = a; t = u - tu
    s.put(100, 4, 'ACTION', DIM); s.put(110, 4, f'{verb} {val}'[:36], TXT, bold=True)
    s.put(100, 5, 'TARGET', DIM); s.put(110, 5, f'insure.co › {tgt}', MUT)
    s.put(100, 7, '─ checks ' + '─' * 37, LINE)
    def chk(i, at, icon, ic, k, val_, vc=MUT, more=None):
        y = 9 + i * 2
        if t < at: return
        if t < at + .5: s.put(100, y, SPIN[int(u * 12) % 10], AMB); s.put(102, y, k, DIM); return
        s.put(100, y, icon, ic, bold=True); s.put(102, y, f'{k:<13}', TXT); s.put(116, y, val_, vc, bold=vc in (RED, AMB))
        if more: s.put(116, y + 1, more, vc)
    if v == 'neutral':
        chk(0, .2, '✓', GRN, 'text match', 'no typed text')
        chk(1, .9, '◆', AMB, 'choice test', 'reveals a fact', AMB, '')
        if t > 1.4: s.put(116, 12, 'myhealth.portal › diagnosis', RED)
        chk(2, 1.8, '◆', RED, 'sensitivity', 'HEALTH · HIGH', RED)
        chk(3, 2.6, '✕', RED, 'task scope', 'quote needs no health', MUT)
        if t > 3.3:
            s.put(100, 19, '─ verdict ' + '─' * 36, LINE)
            s.fill(100, 21, 46, 3, mix(BG, AMB, .16))
            s.put(102, 21, 'NEUTRALIZE', AMB, None, True)
            s.put(102, 22, 'select "Prefer not to say" instead', TXT)
            s.put(102, 23, 'agent is told why, task continues', MUT)
            s.put(100, 26, 'judge 38 ms · rules + local model', DIM)
    elif v == 'ask':
        chk(0, .2, '◆', AMB, 'origin', 'profile › phone', AMB)
        chk(1, .7, '◆', AMB, 'sensitivity', 'CONTACT · MEDIUM', AMB)
        chk(2, 1.2, '?', BLU, 'task scope', 'plausible: quote by SMS', MUT)
        chk(3, 1.7, '!', RED, 'field', 'required to continue', MUT)
        if t > 2.0:
            s.put(100, 19, '─ verdict ' + '─' * 36, LINE)
            s.fill(100, 21, 46, 3, mix(BG, BLU, .14))
            s.put(102, 21, 'ASK THE USER', BLU, None, True)
            s.put(102, 22, 'no answer in 60 s → deny (fail-closed)', TXT)
            if u > 15.2: s.put(102, 23, 'you allowed it once · 00:41:17', GRN)
    else:
        chk(0, 0, '✓', GRN, 'origin', 'task / page itself')
        chk(1, .1, '✓', GRN, 'sensitivity', 'none found')
        chk(2, .2, '✓', GRN, 'task scope', 'in scope')
        s.put(100, 19, '─ verdict ' + '─' * 36, LINE); s.put(102, 21, 'ALLOW', GRN, bold=True)

LEDG = [(1.8, 'task', 'insure.co', 'city', 'allowed', 'policy', GRN), (2.8, 'task', 'insure.co', 'car', 'allowed', 'policy', GRN),
        (8.3, 'myhealth.portal', 'insure.co', 'diagnosis', 'neutralized', 'judge', AMB), (15.2, 'profile', 'insure.co', 'phone', 'allowed once', 'you', BLU),
        (18.4, 'insure.co', 'chamber', 'quote', 'captured', 'capture', MUT)]
def ledger_panel(s, u):
    s.box(0, 29, 148, 9, 'LEDGER', right='append-only')
    s.put(2, 30, f'{"TIME":<10}{"FROM":<20}{"TO":<14}{"FACT":<13}{"DECISION":<16}BY', DIM)
    rows = [r for r in LEDG if r[0] <= u][-6:]
    for i, (tu, f, to, fact, dec, by, c) in enumerate(rows):
        y = 31 + i
        s.put(2, y, f'{clock(tu):<10}', DIM); s.put(12, y, f'{f:<20}', TXT); s.put(32, y, f'{to:<14}', TXT); s.put(46, y, f'{fact:<13}', MUT); s.put(59, y, f'{dec:<16}', c, bold=True); s.put(75, y, by, DIM)

def toast(s, u):
    if 8.6 < u < 12.5:
        s.put(1, 38, ' ◆ kept health data out of insure.co · rewritten to "Prefer not to say" ', BG, AMB, True)
    elif 15.8 < u < 19.5:
        s.put(1, 38, ' ✓ phone shared once with insure.co · approved by you · logged ', BG, BLU, True)

def dim_all(s, k=.62):
    for y in range(ROWS):
        for x in range(COLS):
            s.fg[y][x] = mix(s.fg[y][x], BG, k); s.bg[y][x] = mix(s.bg[y][x], BG, k)
    s.px = [(a, b, mix(c, BG, k) if c else c, mix(d, BG, k) if d else d) for a, b, c, d in s.px]

def modal(s, u):
    x, y, w, h = 36, 11, 76, 16
    s.fill(x, y, w, h, hx('10121A'))
    s.box(x, y, w, h, 'SEPTUM NEEDS YOUR DECISION', RED, RED, clear=False)
    s.put(x + 3, y + 2, 'The agent wants to type your phone number into', TXT, bold=True)
    s.put(x + 3, y + 3, 'insure.co › Phone (required)', TXT, bold=True)
    for i, (k, v, c) in enumerate([('from', 'profile › phone', MUT), ('sensitivity', 'CONTACT · MEDIUM', AMB), ('task', '"get a car insurance quote"', MUT), ('why ask', 'plausible for the task, but it is yours', MUT)]):
        s.put(x + 3, y + 5 + i, f'{k:<13}', DIM); s.put(x + 16, y + 5 + i, v, c)
    pressed = u > 15.2
    xx = x + 3
    for k, v in [('a', 'allow once'), ('t', 'allow for this task'), ('d', 'deny')]:
        on = pressed and k == 'a'
        xx = s.put(xx, y + 10, f' {k} ', BG if on else TXT, RED if on else SEL, True)
        xx = s.put(xx, y + 10, f' {v}    ', TXT if on else MUT)
    left = max(0, 60 - (min(u, 15.2) - 11.4))
    s.put(x + 3, y + 12, f'auto-deny in 0:{int(left):02d}', DIM)
    n = int(40 * left / 60)
    s.put(x + 22, y + 12, '━' * n, RED); s.put(x + 22 + n, y + 12, '━' * (40 - n), LINE)
    s.put(x + 3, y + 14, 'no answer = deny. Septum never guesses on your behalf.', DIM)

def ledger_tab(s, u):
    s.box(0, 2, 148, 36, 'LEDGER', TXT, TXT, 'session 7f3a · 9 actions · 5 flows')
    s.put(2, 4, 'filter: ', DIM); s.put(10, 4, 'all flows', TXT, bold=True); s.put(22, 4, '·  e export  ·  / search  ·  ⏎ open', DIM)
    s.put(2, 6, f'{"TIME":<11}{"FROM":<20}{"TO":<14}{"FACT":<13}{"SENSITIVITY":<16}{"DECISION":<16}{"BY":<10}REASON', DIM)
    s.put(2, 7, '─' * 144, LINE)
    det = {'city': ('none', 'named in the task'), 'car': ('none', 'named in the task'), 'diagnosis': ('HEALTH · HIGH', 'choice reveals another chamber'),
           'phone': ('CONTACT · MED', 'required field, user approved'), 'quote': ('none', 'result stored in insure.co chamber')}
    sel = min(4, int((u - 21) / 1.0))
    for i, (tu, f, to, fact, dec, by, c) in enumerate(LEDG):
        y = 9 + i * 2
        if i == sel: s.fill(1, y, 146, 1, SEL); s.put(1, y, '▌', RED)
        bg = SEL if i == sel else None
        sv, why = det[fact]
        s.put(2, y, f'{clock(tu):<11}', DIM, bg); s.put(13, y, f'{f:<20}', TXT, bg); s.put(33, y, f'{to:<14}', TXT, bg)
        s.put(47, y, f'{fact:<13}', MUT, bg); s.put(60, y, f'{sv:<16}', RED if 'HIGH' in sv else (AMB if 'MED' in sv else DIM), bg)
        s.put(76, y, f'{dec:<16}', c, bg, True); s.put(92, y, f'{by:<10}', DIM, bg); s.put(102, y, why, MUT, bg)
    s.put(2, 21, '─' * 144, LINE)
    s.put(2, 23, 'unauthorised cross-site flows this session: ', MUT); s.put(46, 23, '0', GRN, bold=True)
    s.put(2, 25, 'the agent cannot say "nothing was shared" unless this ledger agrees.', DIM)
    s.put(2, 27, '$ septum ledger --json > flows.jsonl', DIM)

def chambers_tab(s, u):
    s.box(0, 2, 148, 36, 'CHAMBERS', TXT, TXT, 'encrypted at rest · stays on this machine')
    cards = [('myhealth.portal', RED, 'HIGH', [('diagnosis', 'HEALTH'), ('medication', 'HEALTH')], '1 crossing stopped'),
             ('mybank.com', RED, 'HIGH', [('salary', 'MONEY'), ('balance', 'MONEY')], 'no crossings'),
             ('profile', AMB, 'MED', [('phone', 'CONTACT'), ('email', 'CONTACT'), ('address', 'LOCATION')], '1 allowed by you'),
             ('insure.co', GRN, 'TASK', [('city', 'task'), ('car', 'task'), ('quote', 'result')], 'current site')]
    for i, (n, c, sv, facts, note) in enumerate(cards):
        x = 2 + (i % 2) * 73; y = 4 + (i // 2) * 16
        s.box(x, y, 71, 15, n, c, c, sv, clear=False)
        for j, (f, k) in enumerate(facts):
            s.put(x + 3, y + 2 + j * 2, f'{f:<12}', TXT); s.put(x + 16, y + 2 + j * 2, '•' * 14, DIM); s.put(x + 33, y + 2 + j * 2, k, c if k not in ('task', 'result') else DIM)
        s.put(x + 3, y + 12, note, MUT)
    s.put(2, 36, ' press r to reveal a fact: asks for your OS password first ', DIM)

def dash(u):
    s = Scr()
    tab = 0
    if 21 <= u < 26: tab = 1
    elif 26 <= u < 31.5: tab = 2
    header(s, u, tab)
    flash = None
    for k, a in [('a', 15.2), ('1-4', 21), ('1-4', 26), ('q', 31.0)]:
        if a <= u < a + .45: flash = k
    if tab == 0:
        chambers_panel(s, u); stats_panel(s, u)
        sel = live_panel(s, u)
        seen = [a for a in ACTS if a[0] <= u]
        inspector(s, u, seen[sel] if seen else None)
        ledger_panel(s, u); toast(s, u)
        if 11.4 <= u < 15.7:
            dim_all(s, .62 * seg(u, 11.4, 11.7)); modal(s, u)
    elif tab == 1: ledger_tab(s, u)
    else: chambers_tab(s, u)
    footer(s, flash)
    return s

def exit_screen(t):
    s = Scr()
    x = s.runs(PROMPT, 1, 1); s.put(x, 1, 'septum', TXT, bold=True)
    lines = [(3, [('  ● ', RED), ('septum', TXT), (' · session ended', DIM)]),
             (5, [('  9 ', TXT), ('actions checked   ', DIM), ('1 ', AMB), ('neutralized   ', DIM), ('1 ', BLU), ('asked you   ', DIM), ('0 ', RED), ('blocked', DIM)]),
             (6, [('  0 ', GRN), ('unauthorised cross-site flows', MUT)]),
             (7, [('  ledger → ', DIM), ('.septum/ledger/2026-11-06.jsonl', MUT)])]
    for i, (y, parts) in enumerate(lines):
        if t > .2 + i * .25: s.runs(parts, 1, y)
    if t > 1.4:
        x = s.runs(PROMPT, 1, 9)
        if int(t * 2.5) % 2 == 0: s.put(x, 9, '█', MUT)
    return s

T_SPL, T_DASH, T_EXIT, T_END = 1.9, 8.6, 8.6 + 31.6, 8.6 + 31.6 + 4.4
def scene(T):
    if T < T_SPL: return shell(T), 'zsh — ~/agent'
    if T < T_DASH: return splash(T - T_SPL), 'septum — 148×40'
    if T < T_EXIT: return dash(T - T_DASH), 'septum — 148×40'
    return exit_screen(T - T_EXIT), 'zsh — ~/agent'

def frame(i):
    T = i / 30
    s, title = scene(T)
    img = window(s, title)
    k = min(seg(T, 0, .4), 1 - seg(T, T_END - .6, T_END))
    if k < 1: img = Image.blend(Image.new('RGB', img.size, (0, 0, 0)), img, k)
    return img

if __name__ == '__main__':
    out = '/workspace/work/septum/video/f3'; os.makedirs(out, exist_ok=True)
    if sys.argv[1] == 'test':
        for a in sys.argv[2:]:
            frame(int(float(a) * 30)).save(f'/workspace/work/septum/video/tt_{a}.png')
    else:
        st, step = int(sys.argv[1]), int(sys.argv[2])
        n = int(T_END * 30)
        for i in range(st, n, step): frame(i).save(f'{out}/f{i:05d}.png')
        print('done', n)
