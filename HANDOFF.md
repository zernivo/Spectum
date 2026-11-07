# Septum: handoff for the new project session

Use this file as the first thing a new session reads.

## What Septum is
A standalone, agent-agnostic **agent leak firewall** CLI and library. Before every browser action, it checks whether the action would carry a private fact from one site's chamber to another without the user's task asking for it. It then decides ALLOW / NEUTRALIZE / BLOCK / ASK and records the decision in an append-only ledger.

## Decisions already made (do not reopen without Khubaib)
- Name: **Septum**.
- Logo: the v3 stone nautilus with one crimson chamber. Approved.
- Animations: intro, regular and loading. Approved.
- Standalone CLI usable by any agent, including from a sandbox. **Not tied to EigenCore**; EigenCore is just one optional judge backend.
- Principle: in sensitive cases, **security and data integrity come before comfort**. Fail closed. No answer = deny.
- Framing confirmed by Khubaib: an evaluator acting for the user, so sensitive data is never picked or used by the browsing agent unless the user's task asks for it.
- Septum has a full terminal UI (splash, dashboard, modal, tabs). It is not only commands.

## What exists
- Docs: `README.md` and `docs/01–09`
- Brand: logo SVG/PNG, flat mark, favicons, banner, terminal pixel logo, wordmark, animations, history
- Videos (silent, on-screen text): Part 1 how it works (1:43), Part 2 integrations (1:00), TUI (0:45). MP4s are assets on the v0.0 design release, never in git. Storyboards in `design/storyboards/`
- Generators: `design/source/` (Python, cairosvg, PIL, pyfiglet, ffmpeg)

## What is NOT real yet
No code exists. Every command, the Python `guard()` API, all TUI screens, all output and the ledger are a **design spec**. All demo data is fictional.

## Open items
1. The pixel logo in the TUI looked blurry. Redraw it as hand-made pixel art during the build (Khubaib: "we can take care of it when building").
2. Policy tab: not designed.
3. Not made: animated README banner, Lottie/CSS motion, voiceover for the videos.
4. ~~Re-verify the AgentTell figures against the paper.~~ Done 2026-11-06: 61.1% and 34.5% confirmed; the 56.7% denominator is the 18.1% of sessions where the agent noted in memory it must not share, so the old README wording was corrected. See docs/01.
5. Unverified: whether Codex hooks fire on MCP calls; the Windows `PreToolUse` MCP bug.
6. License choice; whether to reserve `septum` on PyPI now.
7. Repo: https://github.com/zernivo/Spectum (note: the repo is spelled *Spectum*, the product is *Septum*; rename pending Khubaib). Commits as **Khubaib Nazeer / Khubaib7-del**.

## Suggested first steps
1. Create the repo, then add the README, docs and brand files.
2. Week 1–2 milestone: reproduce the AgentTell baseline.
3. Scaffold `septum check --json` and the rules judge first; it is the core every door uses.
