# 3. CLI spec (v0.1, proposed)

Single binary/entry point: `septum`. Running it with no subcommand opens the TUI (see 04).

| Command | Purpose |
|---|---|
| `septum` | Open the TUI dashboard for the active session |
| `septum init` | Create `.septum/` with `septum.toml`, `policy.toml` and a local judge auto-detect |
| `septum mcp --upstream "<cmd>"` | Run as an MCP server that wraps an upstream MCP server (e.g. Playwright MCP) and checks every tool call |
| `septum check [--json] [--hook claude]` | Judge one action read from stdin. Exit 0 allow, exit 2 deny (hook mode), JSON decision on stdout |
| `septum run -- <cmd…>` | Launch an agent process with its browser wrapped over CDP, with no code changes |
| `septum ledger [--last N] [--json]` | Show or export ledger entries |
| `septum chambers [--reveal <fact>]` | List chambers. Reveal asks for OS authentication first |
| `septum policy [edit\|test]` | Show, edit or dry-run the policy |
| `septum judge [bench]` | Show the judge backend; benchmark latency |

## `septum check --json`

Input:
```json
{"site":"insure.co","action":"select","field":"Pre-existing conditions",
 "required":false,"value":"Diabetes",
 "options":["None","Prefer not to say","Diabetes"],
 "task":"car insurance quote"}
```
Output:
```json
{"decision":"neutralize","replace":"Prefer not to say",
 "fact":"myhealth.portal/diagnosis","category":"HEALTH","severity":"high",
 "reason":"choice reveals a health fact the task does not need","judge_ms":38}
```
Decisions: `allow | neutralize | block | ask`. Exit codes: `0` allow or neutralize (with a rewrite), `2` block or deny, `3` ask pending (non-interactive callers should treat this as deny), `1` internal error (callers must treat it as deny).

## Config: `.septum/septum.toml`

```toml
[judge]
backend = "auto"      # "ollama" | "llamacpp" | "openai-compatible" | "eigencore" | "rules"
model   = "auto"
cloud   = false       # facts never leave the machine

[ask]
timeout_s = 60        # no answer = deny
```

## Python API

```python
from septum import guard
page = guard(await browser.new_page(), task="car insurance quote")
```
