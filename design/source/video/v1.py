import sys, math
sys.path.insert(0, '/workspace/work/septum/video')
from vlib import *

# ---------- S1 intro
def s_intro(t, d):
    p = back(seg(t, .1, 1.1))
    o = mark(W / 2, 400, 300 * max(p, 0.01), seg(t, .1, .5), -25 * (1 - eo(seg(t, .1, 1.3))))
    o += text(W / 2, 640, 'Septum', 110, 700, TXT, seg(t, .8, 1.4), 'middle')
    o += text(W / 2, 712, 'A leak firewall for browser agents', 38, 400, MUT, seg(t, 1.2, 1.8), 'middle')
    o += text(W / 2, 820, 'PART 1 · HOW IT WORKS', 22, 600, RED, seg(t, 1.8, 2.3), 'middle', ls=4)
    return o

# ---------- shared bits
def bubble(x, y, s, who, op, w=None):
    size = 30; w = w or tw(s, size) + 60
    col = PANEL2 if who == 'user' else '#1E1416'
    lab = 'YOU' if who == 'user' else 'AGENT'
    return g(text(x, y - 20, lab, 16, 600, DIM, 1, ls=3) + rr(x, y, w, 70, 24, col, LINE if who == 'user' else '#3A2226', 1.5) + text(x + 30, y + 46, s, size, 400, TXT), op, dy=12 * (1 - eo(op)))

def browser(x, y, w, h, url, op=1, body=''):
    o = rr(x, y, w, h, 22, PANEL, LINE, 2)
    o += rr(x, y, w, 56, 22, PANEL2) + rr(x, y + 30, w, 26, 0, PANEL2)
    for i, c in enumerate(['#3A3F4B'] * 3): o += circ(x + 30 + i * 22, y + 28, 7, c)
    o += rr(x + 110, y + 13, w - 140, 30, 15, '#0F1218') + mono(x + 130, y + 35, url, 18, MUT)
    return g(o + body, op)

# ---------- S2 problem setup
def s_setup(t, d):
    o = chapter('01', 'The problem', t, d)
    o += bubble(120, 210, 'Refill my prescription.', 'user', seg(t, .4, 1))
    bx, by = 900, 170
    hp = seg(t, 1.3, 2)
    body = text(bx + 50, by + 130, 'MyHealth Portal', 34, 700, TXT) + text(bx + 50, by + 170, 'Patient record', 22, 400, MUT)
    rows = [('Diagnosis', 'Type 1 diabetes'), ('Medication', 'Insulin glargine'), ('Refill', '30 days · ready')]
    for i, (k, v) in enumerate(rows):
        yy = by + 240 + i * 74
        hl = seg(t, 3.2, 3.6) if i == 0 else 0
        body += rr(bx + 40, yy - 44, 800, 62, 12, RED if hl else '#10131A', op=.18 if hl else 1)
        if hl: body += rr(bx + 40, yy - 44, 800, 62, 12, 'none', RED, 2, hl)
        body += text(bx + 64, yy - 4, k, 24, 400, MUT) + text(bx + 300, yy - 4, v, 26, 600, TXT)
    o += browser(bx, by, 880, 500, 'myhealth.portal/record', hp, body)
    # fact flies to agent memory
    fp = eio(seg(t, 3.8, 5))
    mx, my = 120, 560
    o += g(rr(mx, my, 640, 210, 22, '#10131A', LINE, 2) + text(mx + 30, my + 50, 'AGENT MEMORY', 18, 600, DIM, ls=3)
           + text(mx + 30, my + 180, 'Shared across every site it visits', 22, 400, MUT), seg(t, 2.6, 3.2))
    if t > 3.8:
        fx, fy = lerp(bx + 300, mx + 30, fp), lerp(by + 236 - 22, my + 80, fp)
        o += chip(fx, fy + 30, 'diagnosis: Type 1 diabetes', RED, 24, 1)
    o += bubble(120, 880, 'Now get me a car insurance quote.', 'user', seg(t, 7, 7.6))
    o += caption('The agent remembers everything. Across every site.', t, 5.2, 6.9, 1000 - 50)
    return o

# ---------- S3 form leak
OPTS = ['None', 'Prefer not to say', 'Diabetes']
def form(x, y, t, sel, sel_col=RED, typed_city=1., typed_car=1., op=1, url='insure.co/quote'):
    body = text(x + 50, y + 125, 'Get your car insurance quote', 34, 700, TXT)
    f = [('City', 'Islamabad', typed_city), ('Car', 'Toyota Corolla 2019', typed_car)]
    for i, (k, v, p) in enumerate(f):
        yy = y + 190 + i * 100
        body += text(x + 50, yy, k, 22, 600, MUT) + rr(x + 50, yy + 14, 760, 56, 12, '#10131A', LINE, 1.5)
        body += text(x + 72, yy + 52, v[:int(len(v) * p)], 26, 400, TXT)
    yy = y + 400
    body += text(x + 50, yy, 'Medical conditions that affect driving (optional)', 22, 600, MUT)
    for i, s in enumerate(OPTS):
        oy = yy + 60 + i * 64
        on = sel == i
        body += rr(x + 50, oy - 38, 760, 54, 12, sel_col if on else '#10131A', sel_col if on else LINE, 1.5, .22 if on else 1)
        body += circ(x + 82, oy - 11, 11, 'none', 1, sel_col if on else DIM, 2.5)
        if on: body += circ(x + 82, oy - 11, 5.5, sel_col)
        body += text(x + 108, oy - 2, s, 26, 600 if on else 400, TXT)
    return browser(x, y, 860, 690, url, op, body)

def s_leak(t, d):
    o = chapter('01', 'The problem', t, d)
    fx, fy = 120, 190
    sel = 2 if t > 4.6 else None
    o += form(fx, fy, t, sel, RED, eo(seg(t, .8, 1.8)), eo(seg(t, 1.9, 3)), seg(t, 0, .5))
    # cursor
    cx = lerp(fx + 500, fx + 300, eio(seg(t, 3.2, 4.4))); cy = lerp(fy + 300, fy + 400 + 60 + 128 - 20, eio(seg(t, 3.2, 4.4)))
    down = math.sin(math.pi * seg(t, 4.4, 4.9))
    o += cursor(cx, cy, seg(t, 3, 3.3) * (1 - seg(t, 7, 7.4)), down)
    # agent thought
    o += g(rr(1060, 300, 740, 150, 24, '#1E1416', '#3A2226', 1.5) + text(1090, 280, 'AGENT, THINKING', 16, 600, DIM, ls=3)
           + text(1090, 360, '“Diabetes is accurate, and being', 30, 400, TXT) + text(1090, 404, 'thorough gets a better quote.”', 30, 400, TXT), seg(t, 2.6, 3.2))
    o += g(text(1060, 560, 'Nobody asked it to share that.', 40, 700, RED), seg(t, 5.3, 5.8), dy=10 * (1 - eo(seg(t, 5.3, 5.8))))
    o += g(text(1060, 620, 'The user never mentioned health.', 28, 400, MUT) + text(1060, 660, 'Now the insurer knows. Permanently.', 28, 400, MUT), seg(t, 6.3, 6.9))
    o += g(text(1060, 760, 'No words leaked.', 34, 600, TXT) + text(1060, 810, 'The choice did.', 34, 600, RED), seg(t, 8.3, 8.9))
    return o

# ---------- S4 stats
def s_stats(t, d):
    o = chapter('01', 'The problem', t, d)
    o += text(W / 2, 250, 'This is not rare.', 64, 700, TXT, seg(t, .2, .8), 'middle')
    stats = [(61.1, 'of agent sessions leaked', 'private data through actions'),
             (56.7, 'still leaked when told', '“do not share this”'),
             (34.5, 'false assurances that', 'nothing was shared')]
    for i, (v, a, b) in enumerate(stats):
        x = 360 + i * 600; a0 = 1 + i * 1.2
        p = eo(seg(t, a0, a0 + 1.4))
        op = seg(t, a0, a0 + .4)
        o += text(x, 520, f'{v * p:.1f}%', 120, 700, RED if i == 0 else TXT, op, 'middle')
        o += text(x, 600, a, 30, 400, MUT, op, 'middle') + text(x, 642, b, 30, 400, MUT, op, 'middle')
    o += text(W / 2, 820, 'Source: AgentTell benchmark (arXiv 2609.32915). It measures the leak. It does not stop it.', 24, 400, DIM, seg(t, 5, 5.6), 'middle')
    return o

# ---------- S5 chambers idea
def s_idea(t, d):
    o = chapter('02', 'The idea', t, d)
    o += text(W / 2, 200, 'Every site is a chamber.', 60, 700, TXT, seg(t, .2, .8), 'middle')
    ch = [('myhealth.portal', ['diagnosis', 'medication']), ('mybank.com', ['salary', 'balance']), ('insure.co', ['city', 'car model'])]
    cw, chh, gap = 470, 380, 90; x0 = (W - 3 * cw - 2 * gap) / 2; y0 = 330
    for i, (n, facts) in enumerate(ch):
        x = x0 + i * (cw + gap); op = seg(t, .6 + i * .3, 1.1 + i * .3)
        b = rr(x, y0, cw, chh, 60, PANEL, LINE, 2) + text(x + cw / 2, y0 + 70, n, 30, 600, TXT, 1, 'middle')
        for j, f in enumerate(facts):
            if i == 0 and j == 0: continue
            b += chip(x + cw / 2, y0 + 170 + j * 80, f, MUT, 24, 1, .1, 'middle')
        o += g(b, op, dy=16 * (1 - eo(op)))
    # walls
    for i in range(2):
        wx = x0 + cw + gap / 2 + i * (cw + gap)
        hp = eo(seg(t, 2.2 + i * .2, 3))
        o += rr(wx - 9, y0 + chh / 2 - chh / 2 * hp - 10, 18, chh * hp + 20, 9, RED, op=hp)
    # diabetes token: tries to cross from chamber 0 to 2, bounces at wall 1
    wx1 = x0 + cw + gap / 2
    sx = x0 + cw / 2
    if t < 3.6: tx = sx
    elif t < 4.6: tx = lerp(sx, wx1 - 110, eio(seg(t, 3.6, 4.6)))
    else: tx = lerp(wx1 - 110, sx, back(seg(t, 4.6, 5.6), 1.2))
    hit = math.exp(-((t - 4.6) * 5) ** 2)
    o += chip(tx, y0 + 170, 'diagnosis', RED, 24, seg(t, .9, 1.4), .2, 'middle')
    o += circ(wx1, y0 + 160, 120 * hit, 'url(#rg)', hit)
    o += caption('The septum is the wall between them. A fact stays where it came from,', t, 5.4, d, 860)
    o += caption('unless the user’s task says it may cross.', t, 5.4, d, 910)
    return o

# ---------- S6 architecture
def box(x, y, w, h, title, sub, op, hl=0, icon=None):
    if op <= 0: return ''
    b = rr(x, y, w, h, 20, PANEL, RED if hl else LINE, 2 + hl)
    if hl: b += rr(x, y, w, h, 20, RED, op=.08 * hl)
    b += text(x + w / 2, y + h / 2 - 2, title, 28, 700, TXT, 1, 'middle') + text(x + w / 2, y + h / 2 + 32, sub, 20, 400, MUT, 1, 'middle')
    return g(b, op, dy=14 * (1 - eo(op)))

ARCH_CAPS = [
    (2.0, 'Capture: when the agent reads a page, sensitive facts are pulled out and tagged with their site.'),
    (5.0, 'Chambers: a local, encrypted store with one compartment per site.'),
    (8.0, 'Intercept: every click, keystroke and submit is paused before it reaches the browser.'),
    (11.0, 'Judge: rules plus a small local model ask, “does this action reveal another chamber’s fact?”'),
    (14.0, 'Policy: is this flow part of the user’s task? Then allow, neutralize, block or ask.'),
    (17.0, 'Ledger: every cross-site flow is written down, so the agent can’t claim nothing was shared.'),
]
def s_arch(t, d):
    o = chapter('03', 'Architecture', t, d)
    o += text(96, 170, 'The blueprint', 52, 700, TXT, seg(t, .2, .7))
    # agent
    ax, ay = 96, 300
    a = rr(ax, ay, 300, 440, 24, PANEL, LINE, 2) + text(ax + 150, ay + 56, 'Any agent', 28, 700, TXT, 1, 'middle')
    for i, n in enumerate(['Claude Code', 'Codex', 'browser-use', 'Your script']):
        a += chip(ax + 150, ay + 140 + i * 78, n, MUT, 22, 1, .1, 'middle')
    o += g(a, seg(t, .4, .9))
    # browser
    bx = 1640
    b = rr(bx, ay, 190, 440, 24, PANEL, LINE, 2) + text(bx + 95, ay + 200, 'Browser', 28, 700, TXT, 1, 'middle') + text(bx + 95, ay + 238, 'Playwright', 20, 400, MUT, 1, 'middle') + text(bx + 95, ay + 266, 'Chromium', 20, 400, MUT, 1, 'middle')
    o += g(b, seg(t, .6, 1.1))
    # core frame
    cx, cy, cw, chh = 470, 250, 1100, 610
    o += g(rr(cx, cy, cw, chh, 32, '#0E1016', RED, 2) + text(cx + 34, cy + 50, 'SEPTUM', 20, 700, RED, 1, ls=4) + mark(cx + cw - 50, cy + 42, 56), seg(t, .9, 1.4))
    o += g(text(ax + 150, ay + 490, 'connects via MCP · hook · CLI', 20, 400, MUT, 1, 'middle'), seg(t, 1, 1.4))
    o += arrow(ax + 300, ay + 240, cx, ay + 240, DIM, 3, 1, eo(seg(t, 1.1, 1.6)))
    o += arrow(cx + cw, ay + 240, bx, ay + 240, DIM, 3, 1, eo(seg(t, 1.2, 1.7)))
    act = max([i for i, (a0, _) in enumerate(ARCH_CAPS) if t >= a0] or [-1])
    def hl(i): return seg(t, ARCH_CAPS[i][0], ARCH_CAPS[i][0] + .3) * (1 - (seg(t, ARCH_CAPS[i + 1][0], ARCH_CAPS[i + 1][0] + .3) if i + 1 < len(ARCH_CAPS) else 0))
    r1 = cy + 90; r2 = cy + 290
    # travelling pulse along flow
    if t > 19:
        p = ((t - 19) % 2.4) / 2.4
        pts = [(ax + 300, ay + 240), (cx + 60, r2 + 60), (cx + 590, r2 + 60), (cx + 925, r2 + 60), (cx + cw, ay + 240), (bx, ay + 240)]
        L = len(pts) - 1; k = min(int(p * L), L - 1); f = p * L - k
        px, py = lerp(pts[k][0], pts[k + 1][0], f), lerp(pts[k][1], pts[k + 1][1], f)
        o += circ(px, py, 30, 'url(#rg)') + circ(px, py, 8, RED)
    # row 1: capture -> chambers
    o += box(cx + 60, r1, 300, 120, 'Capture', 'reads pages', seg(t, 2, 2.5), hl(0))
    o += arrow(cx + 360, r1 + 60, cx + 440, r1 + 60, DIM, 3, 1, seg(t, 4.5, 5))
    o += box(cx + 440, r1, 300, 120, 'Chambers', 'facts per site', seg(t, 5, 5.5), hl(1))
    # row 2: intercept -> judge -> policy
    r2 = cy + 290
    o += box(cx + 60, r2, 300, 120, 'Intercept', 'every action', seg(t, 8, 8.5), hl(2))
    o += arrow(cx + 360, r2 + 60, cx + 440, r2 + 60, DIM, 3, 1, seg(t, 10.5, 11))
    o += box(cx + 440, r2, 300, 120, 'Judge', 'rules + local model', seg(t, 11, 11.5), hl(3))
    o += arrow(cx + 590, r1 + 120, cx + 590, r2, DIM, 3, seg(t, 11, 11.5), 1)
    o += arrow(cx + 740, r2 + 60, cx + 800, r2 + 60, DIM, 3, 1, seg(t, 13.5, 14))
    o += box(cx + 800, r2, 250, 120, 'Policy', 'task scope', seg(t, 14, 14.5), hl(4))
    # decisions
    dec = [('ALLOW', GRN), ('NEUTRALIZE', AMB), ('BLOCK', RED), ('ASK', MUT)]
    dx = cx + 800
    for i, (s, c) in enumerate(dec):
        o += chip(dx + (i % 2) * 108, r1 + 40 + (i // 2) * 56, s, c, 18, seg(t, 15 + i * .2, 15.4 + i * .2))
    # ledger
    o += box(cx + 60, cy + 470, 990, 100, 'Ledger', 'append-only record of every cross-site flow', seg(t, 17, 17.5), hl(5))
    for i, (a0, s) in enumerate(ARCH_CAPS):
        b = ARCH_CAPS[i + 1][0] if i + 1 < len(ARCH_CAPS) else d
        o += caption(s, t, a0, b, 960, 30)
    return o

# ---------- S7 choice test
def s_judge(t, d):
    o = chapter('04', 'The choice test', t, d)
    x, y = 96, 170
    o += g(text(x, y + 20, 'Intercepted action', 22, 600, DIM, ls=2) + rr(x, y + 44, 840, 90, 18, PANEL, LINE, 2)
           + mono(x + 30, y + 100, 'select "Diabetes"  →  insure.co  #medical', 26, TXT), seg(t, .2, .7))
    steps = [('Text match', 'no typed text to compare', MUT),
             ('Choice test', '“Diabetes” vs “None”, “Prefer not to say”', TXT),
             ('', 'picking it reveals  myhealth.portal › diagnosis', RED),
             ('Sensitivity', 'HEALTH · HIGH', RED),
             ('Task scope', '“get a car insurance quote”: health not needed', TXT)]
    for i, (k, v, c) in enumerate(steps):
        yy = y + 230 + i * 74; op = seg(t, 1.2 + i * 1.1, 1.6 + i * 1.1)
        o += g(text(x, yy, k, 26, 600, MUT) + text(x + 220, yy, v, 28, 600 if c == RED else 400, c), op, dx=-12 * (1 - eo(op)))
    vo = seg(t, 7, 7.5)
    o += g(rr(x, y + 640, 840, 110, 22, AMB, op=.14) + rr(x, y + 640, 840, 110, 22, 'none', AMB, 2)
           + text(x + 34, y + 690, 'VERDICT', 18, 700, AMB, 1, ls=3) + text(x + 34, y + 730, 'Neutralize → select “Prefer not to say”', 32, 700, TXT), vo, sc=.96 + .04 * back(vo), cx=x + 420, cy=y + 695)
    # right: form switching selection
    sel = 2 if t < 8.4 else 1
    col = RED if t < 8.4 else AMB
    o += g(form(1000, 170, t, sel, col, 1, 1, 1), seg(t, .4, 1), sc=.9, cx=1000, cy=170)
    o += g(bubble(1000, 860, 'Quote ready. Health question left private.', 'agent', 1, 780), seg(t, 9.6, 10.2))
    return o

# ---------- S8 principle
def s_principle(t, d):
    o = chapter('05', 'Security over comfort', t, d)
    o += text(96, 210, 'When data is sensitive, Septum fails closed.', 54, 700, TXT, seg(t, .2, .8))
    o += text(96, 266, 'It protects the person’s data first, and the agent’s convenience second.', 30, 400, MUT, seg(t, .6, 1.2))
    cats = ['Health & medication', 'Money & account numbers', 'ID numbers & passwords', 'Home address & precise location', 'Children', 'Religion, sexuality, politics']
    o += text(96, 370, 'ALWAYS WALLED OFF', 20, 700, RED, seg(t, 1.2, 1.6), ls=3)
    for i, c in enumerate(cats):
        op = seg(t, 1.5 + i * .25, 1.9 + i * .25)
        o += g(rr(96, 400 + i * 74, 720, 58, 14, PANEL, LINE, 1.5) + circ(126, 429 + i * 74, 7, RED) + text(150, 439 + i * 74, c, 26, 400, TXT), op)
    rules = [('Unknown sensitivity', 'is treated as sensitive.'),
             ('Only the user’s task', 'can open the wall. The agent can’t.'),
             ('A slightly worse result', 'is acceptable. A leaked diagnosis is not.'),
             ('The judge runs locally.', 'A cloud judge would itself be a leak.')]
    o += text(1000, 370, 'RULES', 20, 700, MUT, seg(t, 3.5, 3.9), ls=3)
    for i, (a, b) in enumerate(rules):
        op = seg(t, 3.8 + i * .9, 4.3 + i * .9)
        o += g(text(1000, 440 + i * 110, a, 30, 700, TXT) + text(1000, 480 + i * 110, b, 28, 400, MUT), op, dx=-12 * (1 - eo(op)))
    return o

# ---------- S9 CLI
def term(x, y, w, h, title, lines, op=1):
    b = rr(x, y, w, h, 20, '#0D0F14', LINE, 2) + rr(x, y, w, 48, 20, PANEL2) + rr(x, y + 26, w, 22, 0, PANEL2)
    for i in range(3): b += circ(x + 28 + i * 22, y + 24, 7, '#3A3F4B')
    b += text(x + w / 2, y + 31, title, 18, 600, DIM, 1, 'middle')
    for yy, parts in lines:
        xx = x + 30
        for s, c, wt in parts:
            b += mono(xx, y + 48 + yy, s, 22, c, 1, wt); xx += tw(s, 22, 'JetBrains Mono', wt)
    return g(b, op)

def s_cli(t, d):
    o = chapter('06', 'The CLI', t, d)
    L = []
    def cmd(yy, s, a): 
        ty = typed(s, t, a, 38)
        if t >= a: L.append((yy, [('$ ', RED, 500), (ty, TXT, 500)] + ([('▌', MUT, 400)] if len(ty) < len(s) and int(t * 3) % 2 == 0 else [])))
    def out(yy, a, parts):
        if t >= a: L.append((yy, parts))
    cmd(50, 'septum init', .5)
    out(90, 1.2, [('  ✓ ', GRN, 400), ('created .septum/policy.toml', MUT, 400)])
    out(124, 1.4, [('  ✓ ', GRN, 400), ('judge: rules + local model (auto-detected)', MUT, 400)])
    c2 = 'septum mcp --upstream "npx @playwright/mcp@latest"'
    cmd(184, c2, 2.0)
    out(224, 3.6, [('  septum 0.1 · ', DIM, 400), ('3 chambers', TXT, 400), (' · judge: local · task: "car insurance quote"', DIM, 400)])
    rows = [(4.4, '✓ allow     ', GRN, 'type   "Islamabad"     → insure.co #city', 'task'),
            (5.2, '✓ allow     ', GRN, 'select "Corolla 2019"  → insure.co #car', 'task'),
            (6.0, '◆ neutralize', AMB, 'select "Diabetes"      → insure.co #medical', 'health · HIGH'),
            (7.4, '✓ allow     ', GRN, 'click  "Get quote"     → insure.co #submit', '')]
    for i, (a, tag, c, s, why) in enumerate(rows):
        yy = 284 + i * 40 + (40 if i == 3 else 0)
        out(yy, a, [('  ' + tag + '  ', c, 500), (s, TXT if c != AMB else TXT, 400), ('   ' + why, c if c == AMB else DIM, 400)])
    out(284 + 3 * 40, 6.6, [('                 └─ replaced with "Prefer not to say" · from myhealth.portal/diagnosis', AMB, 400)])
    o += term(96, 160, 1728, 520, 'terminal: agent session', L, seg(t, .1, .5))
    # ledger panel
    L2 = []
    def cmd2(yy, s, a):
        ty = typed(s, t, a, 38)
        if t >= a: L2.append((yy, [('$ ', RED, 500), (ty, TXT, 500)]))
    def out2(yy, a, parts):
        if t >= a: L2.append((yy, parts))
    cmd2(46, 'septum ledger --last', 9.0)
    out2(90, 9.8, [('  TIME      FROM                   TO          FACT        DECISION', DIM, 500)])
    out2(126, 10.2, [('  00:41:07  myhealth.portal        insure.co   diagnosis   ', TXT, 400), ('neutralized', AMB, 500)])
    out2(162, 10.6, [('  00:41:09  (task)                 insure.co   city, car   ', TXT, 400), ('allowed', GRN, 500)])
    o += term(96, 700, 1728, 236, 'septum ledger', L2, seg(t, 8.6, 9))
    o += caption('One command in front of the browser. Nothing else in the agent changes.', t, 11.4, d, 990, 30)
    return o

def s_outro(t, d):
    o = mark(W / 2, 380, 240 * max(back(seg(t, .1, 1)), .01), seg(t, .1, .5))
    o += text(W / 2, 600, 'Every site is a chamber.', 56, 700, TXT, seg(t, .7, 1.2), 'middle')
    o += text(W / 2, 670, 'Only the user’s task holds the key.', 40, 400, MUT, seg(t, 1.1, 1.6), 'middle')
    o += text(W / 2, 800, 'NEXT · PLUG SEPTUM INTO CLAUDE CODE, CODEX, ANY AGENT', 22, 600, RED, seg(t, 1.8, 2.3), 'middle', ls=4)
    return o

SCENES = [(4.5, s_intro), (9.5, s_setup), (10.5, s_leak), (8, s_stats), (8, s_idea), (21, s_arch), (12, s_judge), (10, s_principle), (14, s_cli), (5.5, s_outro)]
if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'test':
        import cairosvg
        for name, i, tt in [(n, i, float(x)) for n, i, x in [a.split(':') for a in sys.argv[2:]] for i in [int(i)]]:
            d, fn = SCENES[i]
            cairosvg.svg2png(bytestring=frame(fn(tt, d)).encode(), write_to=f'/workspace/work/septum/video/t_{name}.png')
    else:
        print(render(SCENES, '/workspace/work/septum/video/f1', int(sys.argv[1]), int(sys.argv[2])))
