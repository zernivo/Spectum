# 6. Policy and judge

## Judge backends (pluggable, all local)
`rules` (no model: fastest and strictest) · `ollama` · `llamacpp` · `openai-compatible` (any local server) · `eigencore` (optional; Khubaib's own CPU-first runtime). `cloud = false` by default, so facts never leave the machine.

The judge answers one narrow question per action, so a small quantised model is enough. Rules handle the common path; the model handles semantic and choice cases.

## Policy file `.septum/policy.toml` (proposed)
```toml
mode = "fail-closed"

[sensitivity]
HEALTH = "high"
MONEY = "high"
CREDENTIAL = "high"
IDENTITY = "high"
CONTACT = "medium"
LOCATION = "medium"
RELATIONSHIP = "high"

[defaults]
high_optional  = "neutralize"
high_required  = "block"        # or "ask"
medium_needed  = "ask"
judge_error    = "block"

[ask]
timeout_s = 60
on_timeout = "deny"

[[allow]]                        # explicit user grants
fact = "profile/email"
to = "insure.co"
scope = "task"
```

## Task scope
The task string (e.g. "get a car insurance quote") is the contract. Facts the task names go into the `task` chamber and flow freely. Anything else must be justified by the policy or approved by the user.
