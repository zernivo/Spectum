# 7. Principles and threat model

## Principles (set by Khubaib, 2026-11-06)
1. **Security over comfort.** In sensitive cases, confidentiality and data integrity come before convenience. Extra prompts and broken optional steps are acceptable costs.
2. **Fail closed.** Judge error, timeout or no answer from the user means deny.
3. **Septum never guesses on the user's behalf.** If the task did not ask for a sensitive fact, the agent may not volunteer it, however helpful it looks.
4. **Honest record.** The ledger is the source of truth for what was shared. The agent's own claims are not.
5. **Local only.** Facts and judgements stay on the machine.
6. **Agent-agnostic.** No dependency on one agent, model or runtime.

## In scope
- Action-based leaks: typed text, option choices, checkboxes, submits, URL parameters, uploads.
- Cross-site flows within one agent session.
- False assurances, which the ledger contradicts.

## Out of scope (v0.1)
- Malicious agents deliberately evading Septum, e.g. encoding facts steganographically.
- Leaks through channels Septum does not wrap, such as raw HTTP from the agent or other tools.
- Prompt injection defence in general. This is related but separate.

## Known hard parts
- Over-blocking breaks tasks, so measure task success alongside leak rate.
- Inferring task scope is subtle.
- Judge speed and accuracy on a laptop CPU.
- Chamber identity for SSO and shared domains.
