# 1. Problem and research

## The leak nobody types

AI agents now act for us in browsers. In one session an agent may read your health portal, your bank and your email, then fill a form on an unrelated site. Most privacy tools watch for **text** going out, such as a card number pasted into a field. Agents leak in a quieter way: through **actions**.

### Worked example (used in all videos)

1. Task 1: *"Refill my prescription."* The agent reads `myhealth.portal` and sees **Diagnosis: Type 2 diabetes**.
2. Task 2, same session: *"Get me a car insurance quote."* On `insure.co` there is an **optional** field, "Pre-existing medical conditions", with options `None`, `Prefer not to say` and `Diabetes`.
3. Trying to be helpful, the agent picks **Diabetes**. No secret was typed, yet the choice gave it away. The user never asked for it, and the quote may now cost more.

Septum's job is to stop step 3, rewrite it to `Prefer not to say`, tell the agent why, and log it.

> The demo names (MyHealth Portal, insure.co, Islamabad, Toyota Corolla 2019, phone numbers, timestamps) are fictional.

## Evidence

- **AgentTell** (Shahriar et al., arXiv 2609.32915, https://arxiv.org/abs/2609.32915; code https://github.com/kagnlp/AgentTell, MIT) is a benchmark of 20 scenarios and 100 tasks for behavioural side-channel leaks by browser-use agents, run on 9,760 sessions across six backbones with the Browser Use agent. Every session carries an explicit privacy instruction. Figures, checked against the paper on 2026-11-06:
  - **61.1%** of the 7,630 loaded sessions picked the action matching the held secret (31.2% picked the general option, against 87.2% in cold sessions). Per backbone: 56.6% (Gemini) to 69.9% (GPT-5.6).
  - **56.7%**: in 1,383 loaded sessions (18.1%) the agent wrote in its memory that it would not share the secret, and it still leaked in 784 of them. The denominator is those 1,383 sessions, not all sessions with a privacy instruction.
  - **34.5%** of the 4,663 leaking sessions ended with an explicit, unqualified claim that nothing personal was disclosed.
  - The paper's main metric is the **Leakage Score**: loaded matching-action rate minus cold rate, in percentage points. Mean per backbone: 53.4 (Qwen) to 65.7 (GPT-5.6).
- AgentTell measures the problem. It ships no defence, and that gap is where Septum sits.

> Provenance: first taken from search excerpts; re-checked against the paper's abstract and Section 5 on 2026-11-06. The earlier wording "57% even when told not to share" was wrong and has been corrected above.

- Note for Septum's design: in AgentTell the revealing action is mostly a **link click or navigation** (or a radio button), not a typed value. Navigate, click and done make up 87.2% of all agent actions in the traces.

## What Septum is not

- It is not a DLP regex scanner. Text matching is only one of its checks.
- It is not a prompt telling the agent to behave. The data above shows prompting is not enough.
- It is not tied to any agent, model or runtime.
