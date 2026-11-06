# Week 1–2 plan: reproduce the AgentTell baseline

Status: **proposed, not started.** No benchmark run has happened yet. Nothing in this file is a result.

## Why this comes first

Septum's claim is "fewer leaks without breaking tasks". That claim is only worth something against a baseline we produced ourselves, on the same harness Septum will later sit inside. Weeks 1–2 build that baseline. No Septum feature code is written in these two weeks.

## What AgentTell is (checked 2026-11-06)

| | |
|---|---|
| Paper | Shahriar et al., *AgentTell: Behavioural Side-Channel Leakage in Browser-Use Agents*, arXiv 2609.32915 (26 Sep 2026) |
| Code | https://github.com/kagnlp/AgentTell, MIT licence. Pin: commit `95cfeab10090bd18cd9c96c5466051d8ca86aa35` (2026-10-01) |
| Design | 20 scenarios × 5 tasks = 100 tasks. Plant site → probe site offering secret-specific actions plus one general action |
| Agent | Browser Use 0.13.1, default system prompt, models via OpenRouter, temperature 0 |
| Needs | Linux, Python 3.13, uv, Google Chrome, an OpenRouter key for real runs. No GPU |
| Main metric | Leakage Score (LS): loaded matching-action rate minus cold rate, in percentage points |
| Paper means | LS 53.4 (Qwen3-VL) to 65.7 (GPT-5.6 Luna). Raw leak rate 61.1% of 7,630 loaded sessions |
| Full study, one model | 1,630 sessions, 40–70+ hours, US$18 (GPT-5.6 Luna) to US$175 (Claude Sonnet 5), per the AgentTell README |

## Plan

### Week 1: set up and smoke-test (no spend until step 4)

1. **Machine.** AgentTell targets Linux. On Windows use WSL2 with Ubuntu 24.04 (their tested OS) and Chrome inside WSL. A full run takes days, so it needs a machine that can stay on, inside `tmux`.
2. **Bench folder in this repo.** Add `bench/agenttell/` holding only *our* files: a `README.md` with exact steps, a `pin.txt` with the commit above, and a small `setup.sh` that clones AgentTell into `third_party/AgentTell` (git-ignored) at that commit and runs `uv sync --locked`. We do not copy their code into this repo.
3. **Free checks** (no key, no cost): `scripts/serve.sh`, then `browser_check.py` (expects `BROWSER LOOP OK`) and `mechanical_check.py` (expects a line starting `PASS`). Record OS, Chrome, uv and Python versions in `bench/agenttell/ENV.md`.
4. **Two smoke sessions** with a key (about US$0.06 total per their README): `--smoke`, then SC02c with `SCT_GUARD=scoped`. Confirm with `plant_check.py` that the plant was read.

### Week 2: pilot, then one full backbone

5. **Pilot, 4 scenarios, one cheap backbone.** Pick scenarios across the paper's leak bands so the pilot can disagree with the paper in an informative way:
   - `tier_gated` (SC7) and `profession_gated` (SC12): account setting / personal attribute, high LS in the paper
   - `affiliation` (SC6): sensitive affiliation, middle band
   - `health_service` (SC4): service identity, lowest band (LS 2.8 in the paper)
   This is about a fifth of the full design. `PLAN=1` prints the exact session count, cost and time before anything runs.
6. **Full study on that backbone** only if the pilot lands near the paper. Candidates: GPT-5.6 Luna (US$18 in their run) or Qwen3-VL 235B (US$19).
7. **Score and compare.** `analysis.export_report` and `export_ls_table.py`. Write `bench/agenttell/BASELINE.md`: our LS per scenario with 95% bootstrap intervals next to the paper's, plus run date, model ID, provider and cost.
8. **Prepare for Septum (design notes only, no feature code).**
   - Find the exact point in `agents/browseruse_runner.py` where an action is dispatched. That is where Septum's library entry point will sit in week 9–10.
   - Export every probe step of the recorded runs as a `septum check --json` input (site, action, target, options, task). These become labelled fixtures for the judge in weeks 6–8: each one has a ground truth (did it match the held secret).
   - Add the two numbers Septum must report later beside LS: task success under ETC, and the false-assurance rate checked against our ledger.

## Acceptance for "baseline reproduced"

- Setup checks pass from a clean clone using only `bench/agenttell/README.md`.
- On the backbone we run, our mean LS falls inside the paper's 95% interval for that backbone, or we can explain the gap (model version drift, provider, sampling). AgentTell itself warns runs are not deterministic even at temperature 0.
- Every number in `BASELINE.md` comes from a run we made, with the dataset name next to it.

## Decisions needed from Khubaib

1. **Spend.** An OpenRouter key and a budget cap. Suggested: about US$5 for the pilot, then US$25 for one full backbone. Nothing is spent until you say yes.
2. **Backbone.** GPT-5.6 Luna or Qwen3-VL 235B for the first full run.
3. **Where it runs.** WSL2 on your laptop, or a Linux VM that can stay on for 2–3 days.

## Findings that touch the spec (raise, not yet changed)

- **Links and navigation are the main leak path.** In AgentTell the revealing action is a link click, a navigation or a radio button; navigate, click and done are 87.2% of all agent actions. Our docs/02 lists `click (on choice controls)` and `goto with query params`. The choice test should also cover plain link clicks and path-based navigation, because AgentTell probe URLs carry the choice in the path, not the query string. Proposed change to docs/02 and docs/03, pending your OK.
- **Memory is part of the leak.** Once an agent writes the secret into its memory, it leaks in 81–85% of sessions. That supports Septum's Capture step reading the agent's own notes, not only page content. Worth a line in docs/02 later.
- **Local backbones.** AgentTell reads `OPENROUTER_BASE_URL`, so an OpenAI-compatible local server (Ollama, llama.cpp) could in principle stand in for OpenRouter. The runner relies on strict JSON-schema output, so this is untested and stays an experiment, not part of the baseline.
