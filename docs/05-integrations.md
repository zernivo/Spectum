# 5. Integrations

Septum is a standalone CLI and library. Every door goes through the same chambers, judge, policy and ledger.

## A. MCP proxy (recommended default)
`agent → septum mcp → Playwright MCP → Chromium`. The agent sees the same tools, but every call crosses Septum first. Septum can **rewrite** a choice, not only block it.

```bash
claude mcp add septum -- septum mcp --upstream "npx @playwright/mcp@latest"
codex  mcp add septum -- septum mcp --upstream "npx @playwright/mcp@latest"
```
```toml
# ~/.codex/config.toml  (or .codex/config.toml in a trusted project)
[mcp_servers.septum]
command = "septum"
args = ["mcp", "--upstream", "npx @playwright/mcp@latest"]
```

## B. Claude Code `PreToolUse` hook (second wall)
```json
{ "hooks": { "PreToolUse": [{
    "matcher": "mcp__playwright__.*",
    "hooks": [{ "type": "command", "command": "septum check --hook claude" }]
}] } }
```
- Exit 0 allows the call. Exit 2 blocks it, and stderr goes back to Claude as the reason. Exit 1 does **not** block, so Septum's hook mode must never exit 1 on error; it should exit 2.
- Deny/ask permission rules still apply on top of the hook.
- Windows caveat (unconfirmed): a GitHub issue (anthropics/claude-code #85479) reports `PreToolUse` not firing for MCP tools on Windows, and another report (#74203) conflicts with it. Rely on the proxy there.

## C. Sandbox CLI and library
```bash
echo '{…action json…}' | septum check --json
septum run -- python my_agent.py      # wraps the browser over CDP, no code changes
```
```python
from septum import guard
page = guard(await browser.new_page(), task="car insurance quote")
```

## Which to use

| Agent | Use | Note |
|---|---|---|
| Claude Code | MCP proxy | add the hook as belt and braces |
| Codex | MCP proxy | `codex mcp add` or config.toml. Whether Codex's hook events cover MCP calls is **unverified** |
| Playwright / browser-use agent | Python guard | or `septum run` |
| Any sandboxed agent with a shell | `septum check --json` | |

## Verified facts (2026-11-06)
- Claude Code hooks: `PreToolUse` runs before tool calls and matchers can target `mcp__<server>__.*`. Exit 2 blocks the call and feeds stderr back. Source: Claude Code hooks docs.
- Codex MCP: `codex mcp add`, `[mcp_servers.<name>]` in `~/.codex/config.toml`, project config only in trusted projects, remote servers via `--url`. Source: OpenAI Codex MCP docs.
