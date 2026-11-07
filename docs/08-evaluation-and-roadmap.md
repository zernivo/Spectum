# 8. Evaluation and roadmap

## How to prove it works
Run the AgentTell suite **with and without** Septum and measure:
- leak rate (primary)
- task success rate, i.e. whether blocking broke useful work
- false-assurance rate, checked against the ledger
- added latency per action (p50/p95)
- ASK prompts per session, as a usability cost

## 12-week plan
| Weeks | Milestone |
|---|---|
| 1–2 | Reproduce the AgentTell baseline with a Playwright/browser-use agent |
| 3–5 | Chambers and fact capture |
| 6–8 | Judge: text, choice and URL tests; rules plus a local model |
| 9–10 | Policy engine, decisions, ledger. MCP proxy and `septum check` |
| 11 | TUI (Textual), Claude Code hook, `septum run` |
| 12 | Full evaluation and write-up (workshop paper target) |

## Deliverables
An open-source CLI and library, measured results on a public benchmark, and a paper draft.
