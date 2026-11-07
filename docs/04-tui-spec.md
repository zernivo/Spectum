# 4. Terminal UI spec

See the [TUI video](https://github.com/zernivo/Spectum/releases/download/v0.0/septum-tui.mp4) (on the v0.0 design release) and `design/storyboards/tui-storyboard.png`. Target: Python **Textual** (built on Rich), on truecolor terminals. Reference grid: 148×40 cells.

## Boot splash (`septum`)
- Pixel nautilus drawn in truecolor half-blocks (`▀` with fg and bg colours, so 2 px per cell). Source: `brand/terminal/septum-pixel-44x37.png`. It reveals outward from the eye in about 1.4 s.
- Wordmark in figlet **ANSI Shadow** (`brand/terminal/wordmark-ansi-shadow.txt`): `█` in off-white, box-drawing shadow in dim grey.
- Tagline: `agent leak firewall · every site is a chamber · v0.1.0`
- Boot checks, each with a spinner and then ✓: policy, judge, upstream, chambers, ledger.
- Fallbacks: on a 256-colour terminal, quantise the pixel art. With no Unicode, show a plain `SEPTUM` text banner. `--no-splash` and the `SEPTUM_NO_SPLASH` env var skip the splash. Below 100×30 cells, skip the logo.
- Known issue: the pixel logo looked slightly blurry in the video. Redraw it by hand as true pixel art (not a downscale) during the build.

## Dashboard: Live tab
- **Header bar:** `● septum 0.1 │ task "…" │ upstream … │ judge local · 38 ms │ mode FAIL-CLOSED │ ● guarding  clock`
- **Tabs:** `1 Live  2 Ledger  3 Chambers  4 Policy`
- **Chambers panel:** one row per site with a sensitivity badge (HIGH red, MED amber, TASK green) and facts shown as `name ••••`. The row is highlighted while one of its facts is under judgement.
- **Session panel:** counts (checked, allowed, neutralized, asked you, blocked) and an actions/sec sparkline.
- **Live actions:** time, verdict badge, verb, value and target. The selected row has a red edge. A neutralized row shows `└─ rewritten to "…"`.
- **Inspector:** action, target, checks revealed one at a time (text match, choice test with source fact, sensitivity, task scope), then the verdict block and judge latency.
- **Ledger strip:** the last flows.
- **Toast line** and **key hints:** `↑↓ select · ⏎ inspect · a allow · d deny · 1-4 tabs · / filter · e export · q quit`

## ASK modal
The background dims. The modal has a red border titled *SEPTUM NEEDS YOUR DECISION* and shows what the agent wants to do, where, the source chamber, the sensitivity, the task and why Septum is asking. Keys: `a` allow once · `t` allow for this task · `d` deny. A countdown bar shows auto-deny (default 60 s). *No answer = deny.*

## Ledger tab
A full table: time, from, to, fact, sensitivity, decision, by, reason. It shows `unauthorised cross-site flows this session: N` and the export hint.

## Chambers tab
A 2×2 grid of chamber cards with redacted facts, categories and a crossing summary. `r` reveals a fact after OS authentication.

## Policy tab
Not designed yet.

## Exit
`q` prints a session summary to the shell: counts, unauthorised flows and the ledger path.

## Colours
Background `#0B0D12` · text `#F3F1EC` · muted `#9AA0AC` · dim `#5E6573` · lines `#2A2F3B` · allow `#4CC38A` · neutralize `#E2A33B` · ask `#6CB6FF` · block/accent `#E5484D`. Font in videos: JetBrains Mono.
