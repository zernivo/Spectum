"""Exit codes shared by every Septum entry point (docs/03-cli-spec.md).

Callers must treat anything other than ALLOW as a deny. ERROR is never
returned in hook mode: Claude Code does not block on exit 1, so hook mode
maps errors to DENY (docs/05-integrations.md, section B).
"""

from enum import IntEnum


class Exit(IntEnum):
    ALLOW = 0  # allow, or neutralize with a rewrite
    ERROR = 1  # internal error; callers must treat it as deny
    DENY = 2  # block or deny
    ASK_PENDING = 3  # ask pending; non-interactive callers treat it as deny
