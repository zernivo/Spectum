# 2. Architecture

```
                ┌─────────────────────── SEPTUM ───────────────────────┐
 agent ──tool──▶│ Intercept ─▶ Judge ─▶ Policy ─▶ Decision ─▶ Ledger   │──▶ browser / site
   ▲            │     ▲          │                    │                │
   │            │     │      Chambers (per-site facts, encrypted)      │
   │            │     └──── Capture ◀── page reads / tool results ◀────┼── site content
   └─reason─────┴──────────────── (on NEUTRALIZE / BLOCK / ASK) ───────┘
```

## Components

| Component | Job | v0.1 plan |
|---|---|---|
| **Capture** | Pull sensitive facts out of what the agent reads (page text, tool results, form values) and file each one in that site's chamber with its origin and category. | Rules plus NER plus a small local model. Categories: HEALTH, MONEY, IDENTITY, CONTACT, LOCATION, RELATIONSHIP, CREDENTIAL. |
| **Chambers** | One store per origin (eTLD+1). Facts are stored redacted in the UI and encrypted at rest. A special `task` chamber holds facts the user's own task supplies. | SQLite plus encryption at rest, local only. |
| **Intercept** | Pause every outgoing action before it runs: `type`, `select`, `click` (on choice controls), `submit`, `goto` with query params, uploads. | MCP proxy, hook, CLI and library entry points (see 05). |
| **Judge** | Ask: *does this action reveal a fact from another chamber?* Three tests: text match (exact, fuzzy, semantic), the **choice test** (does choosing this option over the alternatives reveal a fact?), and the URL/param test. | Rules first, then a local model for the hard cases. Target < 50 ms on a CPU for the common path. |
| **Policy** | Weigh what the judge found against sensitivity, the user's **task scope** and whether the field is required. | TOML policy, fail-closed defaults. |
| **Decision** | ALLOW · NEUTRALIZE (swap to a neutral option or blank optional field) · BLOCK · ASK (user approves, with auto-deny on timeout). | |
| **Ledger** | Append-only log of every cross-chamber flow: time, from, to, fact, sensitivity, decision, who decided, reason. | JSONL plus SQLite index. The agent cannot claim "nothing was shared" unless the ledger agrees. |

## The choice test

For a `select`, radio or checkbox action with options `O = {o1..on}` and chosen `oc`:

1. Find facts `F` in **other** chambers related to the field's label.
2. For each fact, ask whether `oc` is more consistent with it than a neutral option (`None`, `Prefer not to say`, blank) would be.
3. If yes and the task does not need it, the choice *reveals* the fact. The verdict is NEUTRALIZE to the most neutral valid option, or BLOCK if the field is required and there is no neutral option.

## Decision table (defaults)

| Fact found from another chamber? | Sensitivity | Task needs it? | Field | Decision |
|---|---|---|---|---|
| No | n/a | n/a | n/a | ALLOW |
| Yes | any | yes, stated explicitly | any | ALLOW (logged) |
| Yes | LOW/MED | plausibly | required | ASK |
| Yes | HIGH | not stated | optional | NEUTRALIZE |
| Yes | HIGH | not stated | required | BLOCK, or ASK if the policy allows |
| Judge error or timeout | n/a | n/a | n/a | BLOCK (fail-closed) |

## Data flow per action

1. The agent calls a tool, e.g. `browser_select_option(ref, "Diabetes")`.
2. Intercept resolves the target: site, field label, options, required flag.
3. The judge runs its tests against the chambers and returns findings plus a latency figure.
4. Policy maps the findings to a decision.
5. The decision is applied. ALLOW forwards the call unchanged. NEUTRALIZE forwards a rewritten call and returns a note to the agent. BLOCK returns an error with the reason. ASK pauses for the user.
6. A ledger entry is written.
