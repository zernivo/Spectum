import sys, math
sys.path.insert(0, '/workspace/work/septum/video')
from vlib import *
from v1 import term

def s_intro(t, d):
    p = back(seg(t, .1, 1.1))
    o = mark(W / 2, 400, 260 * max(p, .01), seg(t, .1, .5), -25 * (1 - eo(seg(t, .1, 1.3))))
    o += text(W / 2, 630, 'Plug it into any agent', 84, 700, TXT, seg(t, .8, 1.4), 'middle')
    o += text(W / 2, 700, 'One CLI. Runs wherever the agent runs, including its sandbox.', 36, 400, MUT, seg(t, 1.2, 1.8), 'middle')
    o += text(W / 2, 810, 'PART 2 · INTEGRATIONS', 22, 600, RED, seg(t, 1.8, 2.3), 'middle', ls=4)
    return o

def s_hub(t, d):
    o = chapter('01', 'Four ways in', t, d)
    cx, cy = W / 2, 520
    spokes = [('MCP proxy', 'Claude Code · Codex · Cursor', -1, -1),
              ('Hook', 'Claude Code PreToolUse', 1, -1),
              ('Sandbox CLI', 'septum check · septum run', -1, 1),
              ('Python library', 'Playwright · browser-use', 1, 1)]
    for i, (a, b, sx, sy) in enumerate(spokes):
        bx, by = cx + sx * 520, cy + sy * 190
        op = seg(t, 1 + i * .5, 1.5 + i * .5)
        o += line(cx + sx * 150, cy + sy * 40, bx - sx * 230, by, LINE, 3, op)
        o += g(rr(bx - 230, by - 70, 460, 140, 24, PANEL, LINE, 2) + text(bx, by - 8, a, 32, 700, TXT, 1, 'middle') + text(bx, by + 34, b, 22, 400, MUT, 1, 'middle'), op, dy=12 * (1 - eo(op)))
    o += g(rr(cx - 150, cy - 70, 300, 140, 70, '#0E1016', RED, 2.5) + mark(cx - 70, cy, 90) + mono(cx - 10, cy + 12, 'septum', 34, TXT, 1, 500), seg(t, .3, .8), sc=.9 + .1 * back(seg(t, .3, .9)), cx=cx, cy=cy)
    o += caption('Judge backends: EigenCore · Ollama · llama.cpp · any local OpenAI-compatible server · rules only', t, 3.4, d, 900, 28, MUT)
    return o

def code(x, y, w, title, lines, op=1, size=22, lh=36):
    h = 70 + len(lines) * lh
    b = rr(x, y, w, h, 18, '#0D0F14', LINE, 2) + text(x + 24, y + 38, title, 18, 600, DIM, ls=2)
    for i, ln in enumerate(lines):
        xx = x + 24
        for s, c in (ln if isinstance(ln, list) else [(ln, TXT)]):
            b += mono(xx, y + 82 + i * lh, s, size, c); xx += tw(s, size, 'JetBrains Mono')
    return g(b, op, dy=12 * (1 - eo(op)))

def flow(y, nodes, t, a0, hlk=None):
    o = ''; n = len(nodes); bw = 300; gap = (W - 192 - n * bw) / (n - 1)
    for i, (a, b) in enumerate(nodes):
        x = 96 + i * (bw + gap); op = seg(t, a0 + i * .35, a0 + .4 + i * .35)
        isr = a.startswith('septum')
        o += g(rr(x, y, bw, 110, 20, PANEL if not isr else '#1A1013', RED if isr else LINE, 2) + text(x + bw / 2, y + 50, a, 28, 700, TXT, 1, 'middle', 'JetBrains Mono' if isr else 'Inter') + text(x + bw / 2, y + 84, b, 20, 400, MUT, 1, 'middle'), op)
        if i < n - 1: o += arrow(x + bw + 8, y + 55, x + bw + gap - 8, y + 55, DIM, 3, 1, eo(seg(t, a0 + .3 + i * .35, a0 + .7 + i * .35)))
    if t > a0 + 2:
        p = ((t - a0 - 2) % 2) / 2; px = lerp(96 + bw, W - 96 - bw, p)
        o = circ(px, y + 55, 28, 'url(#rg)') + circ(px, y + 55, 7, RED) + o
    return o

def s_mcp(t, d):
    o = chapter('02', 'Option A · MCP proxy', t, d)
    o += text(96, 180, 'Septum stands in front of the browser tools.', 48, 700, TXT, seg(t, .2, .7))
    o += text(96, 232, 'The agent sees the same Playwright tools. Every call crosses the wall first.', 28, 400, MUT, seg(t, .5, 1))
    o += flow(290, [('Claude Code', 'or Codex, Cursor'), ('septum mcp', 'checks each call'), ('Playwright MCP', 'upstream server'), ('Chromium', 'the real browser')], t, 1)
    up = '"npx @playwright/mcp@latest"'
    o += code(96, 470, 1728, 'CLAUDE CODE', [[('$ ', RED), ('claude mcp add septum -- septum mcp --upstream ' + up, TXT)]], seg(t, 3.5, 4))
    o += code(96, 620, 1728, 'CODEX', [[('$ ', RED), ('codex mcp add septum -- septum mcp --upstream ' + up, TXT)]], seg(t, 4.8, 5.3))
    o += code(96, 770, 840, 'OR ~/.codex/config.toml', [[('[mcp_servers.septum]', AMB)], [('command = ', MUT), ('"septum"', TXT)], [('args = ', MUT), ('["mcp", "--upstream",', TXT)], [('        ', MUT), (up + ']', TXT)]], seg(t, 6, 6.5), 20, 30)
    o += g(text(1000, 830, 'Best default.', 30, 700, TXT) + text(1000, 872, 'Works on every OS, and Septum can', 26, 400, MUT)
           + text(1000, 908, 'rewrite a choice, not just block it.', 26, 400, MUT), seg(t, 7.2, 7.7))
    return o

def s_hook(t, d):
    o = chapter('03', 'Option B · Claude Code hook', t, d)
    o += text(96, 180, 'A second wall inside Claude Code itself.', 48, 700, TXT, seg(t, .2, .7))
    o += text(96, 232, 'A PreToolUse hook runs septum check before any browser tool call.', 28, 400, MUT, seg(t, .5, 1))
    js = [[('{ ', MUT), ('"hooks"', AMB), (': { ', MUT), ('"PreToolUse"', AMB), (': [{', MUT)],
          [('    "matcher"', AMB), (': ', MUT), ('"mcp__playwright__.*"', TXT), (',', MUT)],
          [('    "hooks"', AMB), (': [{ ', MUT), ('"type"', AMB), (': ', MUT), ('"command"', TXT), (',', MUT)],
          [('               "command"', AMB), (': ', MUT), ('"septum check --hook claude"', TXT), (' }]', MUT)],
          [('}] } }', MUT)]]
    o += code(96, 290, 1000, '.claude/settings.json', js, seg(t, 1, 1.5), 22, 40)
    res = [('exit 0', 'allowed: the call goes ahead', GRN, 2.6), ('exit 2', 'blocked: the reason goes back to Claude', RED, 3.4)]
    for i, (a, b, c, a0) in enumerate(res):
        op = seg(t, a0, a0 + .4)
        o += g(rr(1160, 300 + i * 150, 664, 120, 20, PANEL, LINE, 2) + mono(1190, 352 + i * 150, a, 30, c, 1, 500) + text(1190, 392 + i * 150, b, 24, 400, MUT), op)
    o += g(rr(96, 640, 1728, 130, 20, '#0D0F14', LINE, 2) + text(126, 690, 'WHAT CLAUDE SEES', 18, 600, DIM, ls=2)
           + mono(126, 738, 'Septum: "Diabetes" would reveal health data from myhealth.portal. Pick "Prefer not to say".', 22, AMB), seg(t, 4.4, 4.9))
    o += caption('Use it with the proxy as belt and braces. On Windows, a reported bug can skip this hook for MCP tools, so rely on the proxy there.', t, 6, d, 880, 26, MUT)
    return o

def s_sandbox(t, d):
    o = chapter('04', 'Option C · Sandbox CLI & library', t, d)
    o += text(96, 180, 'Any agent that can run a shell can ask Septum.', 48, 700, TXT, seg(t, .2, .7))
    L = []
    def cmd(yy, s, a):
        ty = typed(s, t, a, 60)
        if t >= a: L.append((yy, [('$ ', RED, 500), (ty, TXT, 500)]))
    def out(yy, a, parts):
        if t >= a: L.append((yy, parts))
    cmd(46, "echo '{\"site\":\"insure.co\",\"action\":\"select\",\"value\":\"Diabetes\",", .8)
    out(80, 1.9, [("        \"options\":[\"None\",\"Prefer not to say\",\"Diabetes\"],\"task\":\"car insurance quote\"}' \\", TXT, 500)])
    out(114, 2.4, [('  | septum check --json', TXT, 500)])
    out(162, 3.2, [('{"decision":"neutralize", "replace":"Prefer not to say",', AMB, 400)])
    out(196, 3.4, [(' "fact":"myhealth.portal/diagnosis", "severity":"high"}', AMB, 400)])
    cmd(256, 'septum run -- python my_agent.py', 4.4)
    out(290, 5.2, [('  wraps the browser over CDP · no code changes · same rules', DIM, 400)])
    o += term(96, 230, 1728, 380, 'agent sandbox', L, seg(t, .4, .8))
    py = [[('from ', RED), ('septum ', TXT), ('import ', RED), ('guard', TXT)],
          [('page = guard(', TXT), ('await ', RED), ('browser.new_page(), task=', TXT), ('"car insurance quote"', AMB), (')', TXT)]]
    o += code(96, 650, 1728, 'PYTHON · PLAYWRIGHT OR BROWSER-USE', py, seg(t, 6.2, 6.7))
    o += caption('Same chambers, same judge, same ledger, whichever door the agent uses.', t, 7.6, d, 940, 30)
    return o

def s_judge(t, d):
    o = chapter('05', 'The judge · EigenCore or any local model', t, d)
    o += text(96, 180, 'Septum brings no model of its own.', 48, 700, TXT, seg(t, .2, .7))
    o += text(96, 232, 'Point it at whatever runs locally. EigenCore is one option, not a requirement.', 28, 400, MUT, seg(t, .5, 1))
    toml = [[('[judge]', AMB)],
            [('backend = ', MUT), ('"eigencore"', TXT), ('   # or "ollama", "llamacpp",', DIM)],
            [('                       ', MUT), ('# "openai-compatible", "rules"', DIM)],
            [('model   = ', MUT), ('"auto"', TXT)],
            [('cloud   = ', MUT), ('false', RED), ('        # facts never leave the machine', DIM)]]
    o += code(96, 290, 1000, '.septum/septum.toml', toml, seg(t, 1, 1.5), 22, 40)
    opts = [('EigenCore', 'CPU-first runtime on your laptop', 2.2), ('Ollama / llama.cpp', 'popular local runners', 2.7), ('Rules only', 'no model: fastest, strictest', 3.2)]
    for i, (a, b, a0) in enumerate(opts):
        op = seg(t, a0, a0 + .4)
        o += g(rr(1160, 290 + i * 128, 664, 106, 20, PANEL, RED if i == 0 else LINE, 2) + text(1190, 335 + i * 128, a, 30, 700, TXT) + text(1190, 372 + i * 128, b, 24, 400, MUT), op)
    o += caption('The judge is small on purpose: one yes/no question per action, so it stays fast on a CPU.', t, 4.6, d, 840, 30)
    return o

def s_table(t, d):
    o = chapter('06', 'Which one to use', t, d)
    rows = [('Claude Code', 'MCP proxy', '+ hook as a second wall'),
            ('Codex', 'MCP proxy', 'config.toml or codex mcp add'),
            ('Your Playwright / browser-use agent', 'Python guard', 'or septum run, no code changes'),
            ('Any sandboxed agent with a shell', 'septum check --json', 'JSON in, decision out')]
    o += g(text(96, 210, 'AGENT', 20, 700, DIM, ls=3) + text(860, 210, 'USE', 20, 700, DIM, ls=3) + text(1300, 210, 'NOTE', 20, 700, DIM, ls=3), seg(t, .2, .6))
    for i, (a, b, c) in enumerate(rows):
        y = 250 + i * 130; op = seg(t, .6 + i * .5, 1 + i * .5)
        o += g(rr(96, y, 1728, 106, 20, PANEL, LINE, 2) + text(126, y + 64, a, 30, 700, TXT) + mono(860, y + 64, b, 26, RED, 1, 500) + text(1300, y + 64, c, 26, 400, MUT), op, dx=-14 * (1 - eo(op)))
    return o

def s_outro(t, d):
    o = mark(W / 2, 380, 240 * max(back(seg(t, .1, 1)), .01), seg(t, .1, .5))
    o += text(W / 2, 600, 'Septum', 84, 700, TXT, seg(t, .6, 1.1), 'middle')
    o += text(W / 2, 670, 'One wall between every site. Any agent. Your machine.', 36, 400, MUT, seg(t, 1, 1.5), 'middle')
    return o

SCENES = [(4.5, s_intro), (7, s_hub), (10, s_mcp), (10, s_hook), (10, s_sandbox), (8, s_judge), (6.5, s_table), (4.5, s_outro)]
if __name__ == '__main__':
    if sys.argv[1] == 'test':
        import cairosvg
        for a in sys.argv[2:]:
            n, i, tt = a.split(':'); d, fn = SCENES[int(i)]
            cairosvg.svg2png(bytestring=frame(fn(float(tt), d)).encode(), write_to=f'/workspace/work/septum/video/u_{n}.png')
    else:
        print(render(SCENES, '/workspace/work/septum/video/f2', int(sys.argv[1]), int(sys.argv[2])))
