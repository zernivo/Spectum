"""Command-line entry point.

Only `--version` and `--help` work today. Every planned subcommand is
recognised but not implemented, and returns Exit.DENY with a message on
stderr, so a caller that wires Septum in early is denied rather than
silently allowed (fail closed, docs/07 principle 2).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from septum import __version__
from septum.exitcodes import Exit

# Subcommands from docs/03-cli-spec.md. Kept here so the surface is visible
# and tested before any of them is built.
PLANNED_COMMANDS: dict[str, str] = {
    "init": "create .septum/ with septum.toml and policy.toml",
    "mcp": "run as an MCP proxy in front of an upstream MCP server",
    "check": "judge one action read from stdin",
    "run": "launch an agent with its browser wrapped over CDP",
    "ledger": "show or export ledger entries",
    "chambers": "list chambers",
    "policy": "show, edit or dry-run the policy",
    "judge": "show the judge backend; benchmark latency",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="septum",
        description="Agent leak firewall (design stage: no checks are implemented yet).",
    )
    parser.add_argument("--version", action="version", version=f"septum {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    for name, help_text in PLANNED_COMMANDS.items():
        p = sub.add_parser(name, help=f"(not implemented) {help_text}")
        p.add_argument("args", nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    if ns.command is None:
        # The TUI opens here once it exists (docs/04-tui-spec.md).
        print(
            f"septum {__version__}: design stage, the terminal UI is not built yet.",
            file=sys.stderr,
        )
        return int(Exit.DENY)
    print(
        f"septum {ns.command}: not implemented yet. Denying (fail closed).",
        file=sys.stderr,
    )
    return int(Exit.DENY)
